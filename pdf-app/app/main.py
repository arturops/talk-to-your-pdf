# Tech stack is FAISS (vdb)
# streamlit (UI)
# fast api (backend API)
# LangChain, Ollama, pdfplumber
# llama3.2 and nomic models
from typing import Annotated

from fastapi import FastAPI
from fastapi import File
from fastapi import HTTPException
from fastapi import UploadFile
from fastapi import status
from upload import save_file


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
