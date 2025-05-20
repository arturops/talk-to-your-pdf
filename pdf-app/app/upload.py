import os

import aiofiles
from aiofiles.os import makedirs
from fastapi import UploadFile

from app.constants import DEFAULT_CHUNK_SIZE
from app.constants import UPLOADED_DOCS_DIR


async def save_file(
	file: UploadFile, chunk_size: int = DEFAULT_CHUNK_SIZE
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
