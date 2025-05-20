from typing import Any
from typing import AsyncGenerator

import aiofiles

from app.constants import DEFAULT_CHUNK_SIZE


async def load(
	filepath: str, chunk_size: int = DEFAULT_CHUNK_SIZE
) -> AsyncGenerator[str, Any]:
	async with aiofiles.open(filepath, "r", encoding="utf-8") as f:
		while chunk := await f.read(chunk_size):
			yield chunk
