from langchain_community.vectorstores import FAISS
from langchain_core.documents import Document
from loguru import logger

from app.constants import VECTOR_DB_DIR
from app.embedding_models import OllamaEmbeddingsService

from .transform import load


DEFAULT_EMBEDDING_MODEL = "nomic-embed-text:v1.5"


class VectorDatabaseService:
	async def store_file_content_in_db(
		self,
		filepath: str,
		chunk_size: int = 8000,
		collection_name: str = VECTOR_DB_DIR,
	) -> None:
		logger.info(f"Inserting {filepath} content into vector database")
		vectordb = None
		ollama_embeddings = OllamaEmbeddingsService(
			model_name=DEFAULT_EMBEDDING_MODEL
		)
		async for chunk in load(filepath, chunk_size):
			# logger.info(f"Inserting '{chunk[0:20]}...' into database")
			# prepare docs
			docs = [Document(page_content=chunk)]
			if vectordb is None:
				# store in RAM
				vectordb = await FAISS.afrom_documents(
					docs, ollama_embeddings.model
				)
			else:
				# add more docs to vdb
				await vectordb.aadd_documents(docs)

		# store in disk
		vectordb.save_local(collection_name)
		logger.info(f"Saved {collection_name} to disk")

	def load_vector_db(self, collection_name: str = VECTOR_DB_DIR) -> FAISS:
		ollama_embeddings = OllamaEmbeddingsService(
			model_name=DEFAULT_EMBEDDING_MODEL
		)
		# Load the vector database from disk
		# faiss stores in pickle format, so allow the deserialization
		loaded_vectordb = FAISS.load_local(
			collection_name,
			ollama_embeddings.model,
			allow_dangerous_deserialization=True,
		)
		logger.info(f"Loaded {collection_name} from disk")
		return loaded_vectordb
