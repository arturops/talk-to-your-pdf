import os

from dotenv import load_dotenv
from langchain import hub
from langchain.chains.combine_documents import create_stuff_documents_chain
from langchain.chains.retrieval import create_retrieval_chain
from langchain_community.document_loaders import PyPDFLoader
from langchain_community.vectorstores import FAISS
from langchain_openai import OpenAI
from langchain_openai import OpenAIEmbeddings
from langchain_text_splitters import CharacterTextSplitter


load_dotenv()

PDF_NAME = "ReAct-AI-agents.pdf"
PDF_DIR_NAME = "files"
PDF_DIR = os.path.join(PDF_DIR_NAME, PDF_NAME)
PDF_PATH = os.path.join(os.path.dirname(__file__), PDF_DIR)


def run_simple_rag():
	print(f"Input pdf: {PDF_PATH}")
	loader = PyPDFLoader(file_path=PDF_PATH)
	documents = loader.load()
	text_splitter = CharacterTextSplitter(
		chunk_size=1000, chunk_overlap=30, separator="\n"
	)
	docs = text_splitter.split_documents(documents=documents)
	embeddings = OpenAIEmbeddings(model="text-embedding-ada-002")
	# store in RAM
	vectorstore = FAISS.from_documents(docs, embeddings)
	# store in disk
	vectorstore.save_local("faiss_index_react")
	# faiss stores in pickle format, so allow the deserialization
	new_vectorstore = FAISS.load_local(
		"faiss_index_react", embeddings, allow_dangerous_deserialization=True
	)

	retrieval_qa_chat_prompt = hub.pull("langchain-ai/retrieval-qa-chat")
	combine_docs_chain = create_stuff_documents_chain(
		OpenAI(model="gpt-4.1-nano"), retrieval_qa_chat_prompt
	)
	retrieval_chain = create_retrieval_chain(
		new_vectorstore.as_retriever(), combine_docs_chain
	)

	res = retrieval_chain.invoke(
		{"input": "Give me the gist of ReAct in 3 sentences"}
	)
	print("Question: Give me the gist of ReAct in 3 sentences")
	print(f"Answer: {res['answer']}")


if __name__ == "__main__":
	run_simple_rag()
