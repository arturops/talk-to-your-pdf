import os

from langchain.prompts import ChatPromptTemplate
from langchain.prompts import PromptTemplate
from langchain.retrievers.multi_query import MultiQueryRetriever
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnablePassthrough
from langchain_ollama import ChatOllama
from loguru import logger

from app.vector_db import VectorDatabaseService


def process_question(question: str, selected_model: str) -> str:
	"""
	Process a user question using the vector database and selected language
	model.

	Args:
	    question (str): The user's question.
	    selected_model (str): The name of the selected language model.

	Returns:
	    str: The generated response to the user's question.
	"""
	logger.info(
		f"Processing question: {question} using model: {selected_model}"
	)

	# Initialize LLM
	ollama_base_url = os.getenv(
		"OLLAMA_SERVER_URL", "http://localhost:11434"
	)
	llm = ChatOllama(base_url=ollama_base_url, model=selected_model)

	# Query prompt template
	QUERY_PROMPT = PromptTemplate(
		input_variables=["question"],
		template="""You are an AI language model assistant. Your task is to generate 2
        different versions of the given user question to retrieve relevant documents from
        a vector database. By generating multiple perspectives on the user question, your
        goal is to help the user overcome some of the limitations of the distance-based
        similarity search. Provide these alternative questions separated by newlines.
        Original question: {question}""",
	)

	# Set up retriever
	vector_db = VectorDatabaseService().load_vector_db()
	retriever = MultiQueryRetriever.from_llm(
		vector_db.as_retriever(k=10), llm, prompt=QUERY_PROMPT
	)

	# RAG prompt template
	template = """Answer the question based ONLY on the following context:
    {context}
    Question: {question}
  """

	rag_prompt = ChatPromptTemplate.from_template(template)

	# Create chain
	chain = (
		{"context": retriever, "question": RunnablePassthrough()}
		| rag_prompt
		| llm
		| StrOutputParser()
	)

	response = chain.invoke(question)
	logger.info("Question processed and response generated")
	return response
