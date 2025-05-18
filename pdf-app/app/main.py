# Tech stack is FAISS (vdb)
# streamlit (UI)
# fast api (backend API)
# LangChain, Ollama, pdfplumber
# llama3.2 and nomic models
import logging
from typing import Annotated
from typing import Any
from typing import Tuple

import ollama
from fastapi import FastAPI
from fastapi import File
from fastapi import HTTPException
from fastapi import UploadFile
from fastapi import status
from upload import save_file


# Logging configuration
logging.basicConfig(
	level=logging.INFO,
	format="%(asctime)s - %(levelname)s - %(message)s",
	datefmt="%Y-%m-%d %H:%M:%S",
)

logger = logging.getLogger(__name__)

app = FastAPI()


@app.get("/")
def root_controller():
	return {"message": "Hello World"}


@app.post("/upload")
async def file_upload_controller(
	file: Annotated[UploadFile, File(description="Upload PDF files.")],
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
		file_path = await save_file(file)
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


@app.post("/retrieve/pdf/pages")
def retrieve_pdf_pages_controller():
	return


def get_ollama_model_names(models_info: Any) -> Tuple[str, ...]:
	"""
	Extract model names from the provided models information.

	Args:
	    models_info: Response from ollama.list()

	Returns:
	    Tuple[str, ...]: A tuple of model names.
	"""
	logger.info("Get Ollama model names")
	try:
		# The new response format returns a list of Model objects
		if hasattr(models_info, "models"):
			# Extract model names from the Model objects
			models = tuple(model.model for model in models_info.models)
		else:
			# Fallback for any other format
			models = tuple()

		logger.info(f"Ollama models: {models}")
		return models
	except Exception as e:
		logger.error(f"Error extracting Ollama model names: {e}")
		return tuple()


@app.get("/list/models")
def list_models_controller():
	models_info = ollama.list()
	ollama_models = get_ollama_model_names(models_info)
	return {"models": ollama_models}
