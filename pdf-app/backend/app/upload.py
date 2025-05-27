import os

import aiofiles
import pdfplumber
from aiofiles.os import makedirs
from fastapi import UploadFile
from langchain_text_splitters import RecursiveCharacterTextSplitter

from app.constants import DEFAULT_DIGEST_PDF_CHUNK_SIZE
from app.constants import DEFAULT_UPLOADED_DOCS_DIR


UPLOADED_DOCS_DIR = os.getenv(
	"UPLOADED_DOCS_DIR", DEFAULT_UPLOADED_DOCS_DIR
)


async def save_file(
	file: UploadFile, chunk_size: int = DEFAULT_DIGEST_PDF_CHUNK_SIZE
) -> str:
	"""
	Save the uploaded file to the server.
	"""
	# Create directory if it doesn't exist
	await makedirs(UPLOADED_DOCS_DIR, exist_ok=True)
	filepath = os.path.join(UPLOADED_DOCS_DIR, file.filename)

	async with aiofiles.open(filepath, "wb") as out_file:
		while content_chunk := await file.read(chunk_size):
			await out_file.write(content_chunk)

	return filepath


def pdf_text_extractor(
	filepath: str, chunk_size: int, chunk_overlap: int = 150
) -> None:
	# Extract text from the PDF using pdfplumber
	with pdfplumber.open(filepath) as pdf:
		text = ""
		for page in pdf.pages:
			text += page.extract_text() or ""  # Extract text from each page

	# Split the text into chunks using RecursiveCharacterTextSplitter
	text_splitter = RecursiveCharacterTextSplitter(
		chunk_size=chunk_size, chunk_overlap=chunk_overlap
	)
	chunks = text_splitter.split_text(text)

	# Save the chunks to a .txt file
	txt_filepath = filepath.replace(".pdf", ".txt")
	with open(txt_filepath, "w", encoding="utf-8") as f:
		f.write(",".join(chunks))
