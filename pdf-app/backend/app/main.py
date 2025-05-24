import os
import shutil
from typing import Annotated
from typing import Any
from typing import Tuple

import ollama
from fastapi import BackgroundTasks
from fastapi import FastAPI
from fastapi import File
from fastapi import HTTPException
from fastapi import UploadFile
from fastapi import status
from loguru import logger
from pydantic import BaseModel

from app.constants import UPLOADED_DOCS_DIR
from app.constants import VECTOR_DB_DIR
from app.retriever import process_question
from app.upload import pdf_text_extractor
from app.upload import save_file
from app.vector_db import VectorDatabaseService


# This is a workaround for the duplicate liomp.dylib in macOS
# torch installs its own version of libomp.dylib
# and it conflicts with the one used by faiss-cpu
# We nedd to allow both to coexist
os.environ["KMP_DUPLICATE_LIB_OK"] = "TRUE"

OLLAMA_SERVER_URL = os.getenv(
	"OLLAMA_SERVER_URL", "http://localhost:11434"
)


app = FastAPI()


@app.get("/")
def root_controller():
	return {"message": "The app is running!"}


@app.post("/upload")
async def file_upload_controller(
	file: Annotated[UploadFile, File(description="Upload PDF files.")],
	background_task_processor: BackgroundTasks,
):
	"""
	Upload a file to the server.
	"""
	if file.content_type != "application/pdf":
		raise HTTPException(
			status_code=status.HTTP_400_BAD_REQUEST,
			detail="Only PDF files are supported.",
		)

	try:
		vdb_chunk_size = 8000
		file_path = await save_file(file)
		background_task_processor.add_task(
			pdf_text_extractor,
			file_path,
			chunk_size=vdb_chunk_size,
			chunk_overlap=150,
		)
		vector_db_serv = VectorDatabaseService()
		background_task_processor.add_task(
			vector_db_serv.store_file_content_in_db,
			file_path.replace("pdf", "txt"),
			chunk_size=vdb_chunk_size,
			collection_name=VECTOR_DB_DIR,
		)
	except Exception as e:
		raise HTTPException(
			status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
			detail=f"An error ocurred while uploading file: {str(e)}",
		)
	return {
		"filename": file.filename,
		"location": file_path,
		"message": "File uploaded successfully.",
	}


@app.get("/download/vectorDatabase")
def download_vector_db_controller():
	return


def delete_folder(folder: str):
	"""
	Deletes a folder and all its contents.

	Args:
	    folder (str): The folder to delete.
	"""
	folder_path = os.path.abspath(folder)
	if os.path.exists(folder_path):
		shutil.rmtree(folder_path)
		logger.info(
			f"Folder '{folder_path}' and its contents have been deleted."
		)
	else:
		logger.info(f"Folder '{folder_path}' does not exist.")


@app.delete("/vectorDatabase", status_code=204)
def delete_vector_db_controller():
	delete_folder(VECTOR_DB_DIR)


@app.delete("/pdf", status_code=204)
def delete_pdf_controller():
	delete_folder(UPLOADED_DOCS_DIR)


def get_ollama_model_names(models_info: Any) -> Tuple[str, ...]:
	"""
	Extract model names from the provided models information.

	Args:
	    models_info: Response from ollama.list()

	Returns:
	    Tuple[str, ...]: A tuple of model names.
	"""
	try:
		# Default fallback value
		models = tuple()
		# The new response format returns a list of Model objects
		if hasattr(models_info, "models"):
			# Extract model names from the Model objects
			models = tuple(model.model for model in models_info.models)
	except Exception as e:
		logger.error(f"Error extracting Ollama model names: {e}")

	return models


@app.get("/list/models")
def list_models_controller():
	ollama_client = ollama.Client(host=OLLAMA_SERVER_URL)
	models_info = ollama_client.list()
	ollama_models = get_ollama_model_names(models_info)
	return {"models": ollama_models}


class QuestionRequest(BaseModel):
	"""
	Request model for the question endpoint.
	"""

	prompt: str
	model: str = "llama3.2:3b"


@app.post("/question")
def question_controller(question_request: QuestionRequest):
	"""
	Ask a question to the model.
	"""
	logger.info(
		f"Received question: '{question_request.prompt}' for model: {question_request.model}"
	)
	try:
		response = process_question(
			question=question_request.prompt,
			selected_model=question_request.model,
		)
	except Exception as e:
		logger.error(f"Error asking question: {e}")
		raise HTTPException(
			status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
			detail=f"An error occurred while asking the question: {str(e)}",
		)
	return {"response": response}
