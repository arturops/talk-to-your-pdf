from typing import Any
from typing import List

import ollama
import requests
import streamlit as st


# page layout
st.set_page_config(
	page_title="PDF RAG",
	page_icon="📄",
	layout="wide",
	initial_sidebar_state="collapsed",
)

# st.write("Upload a file to FastAPI")
# file = st.file_uploader("Choose a PDF file", type=["pdf"])

# if st.button("Submit"):
# 	if file is not None:
# 		files = {"file": (file.name, file, file.type)}
# 		response = requests.post("http://localhost:8000/upload", files=files)
# 		st.write(response.text)
# 	else:
# 		st.wrtite("No file uploaded.")


@st.cache_data
def extract_all_pages_as_images(file_uploaded) -> List[Any]:
	"""
	Extract all pages from a PDF file as images.

	Args:
	    file_upload (st.UploadedFile): Streamlit file upload object containing the PDF.

	Returns:
	    List[Any]: A list of image objects representing each page of the PDF.
	"""
	# logger.info(f"Extracting all pages as images from file: {file_upload.name}")
	pdf_pages = []
	# with pdfplumber.open(file_uploaded) as pdf:
	#     pdf_pages = [page.to_image().original for page in pdf.pages]
	# logger.info("PDF pages extracted as images")
	return pdf_pages


def create_vdb(file_uploaded) -> Any:
	"""Calls backend to create a vector database"""
	return None


def clean_session():
	"""
	Clean the session state.
	"""
	# logger.info("Cleaning session state")
	try:
		for key in st.session_state.keys():
			value = st.session_state.pop(key, None)
			# logger.info(f"Cleaned '{key}' value: {value}"")
		st.success("Collection and temporary files deleted successfully.")
		# logger.info("Session state cleaned")
		st.rerun()
	except Exception as e:
		st.error(f"Error cleaning session state: {str(e)}")
		# logger.error(f"Error cleaning session state: {str(e)}")


def enable_process_pdf_button(file_uploaded) -> bool:
	"""Enable process PDF button"""
	if file_uploaded is not None:
		st.session_state["pdf_process_button_disabled"] = False
	else:
		st.session_state["pdf_process_button_disabled"] = True


def main():
	"""Run the client"""
	st.subheader(
		"📜🔍 Talk privately to your PDF 🙂🤖", divider="gray", anchor=False
	)

	# list local models
	ollama_models = ollama.list()
	print(ollama_models)
	ollama_models_items = tuple()

	# setup layout

	col1, col2 = st.columns([1.5, 2])

	# Init session state
	keys = {
		"messages",
		"pdf_pages",
		"vector_db",
		"pdf_process_button_disabled",
	}
	for key in keys:
		if key not in st.session_state:
			st.session_state[key] = None
	# logger.info("Session state initialized")

	# Upload file
	file_uploaded = col1.file_uploader(
		"Upload a PDF file",
		type="pdf",
		accept_multiple_files=False,
		key="pdf_uploader",
		# on_change=enable_process_pdf_button,
		# label_visibility="collapsed",
	)

	pdf_proccess_button = col1.button(
		"Process",
		key="process_pdf_button",
		help="Process pdf to get it ready for querying",
		use_container_width=True,
		disable=st.session_state["pdf_process_button_disabled"],
	)

	# logger.info("File uploaded")
	if file_uploaded:
		with st.spinner("Generating preview of PDF ..."):
			st.session_state["pdf_pages"] = extract_all_pages_as_images(
				file_uploaded
			)
		st.session_state["pdf_process_button_disabled"] = True
	# else:
	# 	st.write("No file uploaded.")

	# if file_uploaded:
	# 	with st.spinner("⚙️ Processing PDF ..."):
	# 		st.session_state["vector_db"] = create_vdb(file_uploaded)
	# 		st.session_state["pdf_pages"] = extract_all_pages_as_images(
	# 			file_uploaded
	# 		)

	# Display PDF pages
	if st.session_state.get("pdf_pages"):
		with col1, st.container(height=400, border=True):
			st.subheader("PDF pages preview")
			for page in st.session_state["pdf_pages"]:
				st.image(page, use_column_width=True)

	if pdf_proccess_button:
		# logger.info("File submited to get processed")
		with st.spinner("⚙️ Processing PDF ..."):
			# logger.info("Storing PDF")
			files = {
				"file": (file_uploaded.name, file_uploaded, file_uploaded.type)
			}
			response = requests.post("http://localhost:8000/upload", files=files)
			st.write(response.text)
			# logger.info("Generating PDF embeddings and storing them in vdb")
			st.session_state["vector_db"] = create_vdb(file_uploaded)

			# logger.info("PDF stored and processed successfully")
			st.session_state["pdf_process_button_disabled"] = False

	# Delete all button (refresh)
	restart_all = col1.button(
		label="🚮 Restart all",
		type="secondary",
		key="restart_all",
		help="Deletes pdf and all associated data to start over",
		use_container_width=True,
	)

	if restart_all:
		clean_session()


if __name__ == "__main__":
	# run the app
	main()
