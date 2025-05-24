import os

from langchain_ollama import OllamaEmbeddings


class EmbeddingsService:
	def __init__(self, model_name: str):
		self.model_name = model_name
		self.model = None

	def get_embeddings(self, text: str) -> list[float]:
		"""
		Embed the text using the specified model.
		"""
		raise NotImplementedError("Subclasses should implement this method.")


class OllamaEmbeddingsService(EmbeddingsService):
	def __init__(self, model_name: str):
		super().__init__(model_name)
		self.base_url = os.getenv(
			"OLLAMA_SERVER_URL", "http://localhost:11434"
		)
		self.model = OllamaEmbeddings(base_url=self.base_url, model=model_name)

	def get_embeddings(self, docs_list: list[str]):
		embeddings = self.model.embed_documents(docs_list)
		return embeddings
