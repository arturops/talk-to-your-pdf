import os

from dotenv import load_dotenv
from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import CharacterTextSplitter


load_dotenv()

OPEN_API_KEY = os.getenv("OPENAI_API_KEY")
PDF_NAME = "ReAct-AI-agents.pdf"
PDF_DIR_NAME = "files"
PDF_DIR = os.path.join(PDF_DIR_NAME, PDF_NAME)
PDF_PATH = os.path.join(os.path.dirname(__file__), PDF_DIR)

if __name__ == "__main__":
	print(PDF_PATH)
	loader = PyPDFLoader(file_path=PDF_PATH)
	documents = loader.load()
	text_splitter = CharacterTextSplitter(
		chunk_size=1000, chunk_overlap=30, separator="\n"
	)
	docs = text_splitter.split_documents(documents=documents)
