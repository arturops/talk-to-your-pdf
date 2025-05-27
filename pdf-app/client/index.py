import os
from typing import Any
from typing import List

import pdfplumber
import requests
import streamlit as st
from loguru import logger


BACKEND_URL = os.getenv("BACKEND_URL", "http://localhost:8000")

# page setup
st.set_page_config(
	page_title="Tame Your PDF",
	page_icon="🦮",
	layout="wide",
	initial_sidebar_state="collapsed",
)


@st.cache_data
def extract_all_pages_as_images(file_uploaded) -> List[Any]:
	"""
	Extract all pages from a PDF file as images.

	Args:
	    file_upload (st.UploadedFile): Streamlit file upload object
			containing the PDF.

	Returns:
	    List[Any]: A list of image objects representing each page of the PDF.
	"""
	logger.info(
		f"Extracting all pages as images from file: {file_uploaded.name}"
	)
	pdf_pages = []
	with pdfplumber.open(file_uploaded) as pdf:
		pdf_pages = [page.to_image().original for page in pdf.pages]
	logger.info("PDF pages extracted as images")
	return pdf_pages


def clean_session():
	"""
	Clean the session state.
	"""
	logger.info("Cleaning session state")
	try:
		res = requests.delete(f"{BACKEND_URL}/vectorDatabase")
		res.raise_for_status()
		res = requests.delete(f"{BACKEND_URL}/pdf")
		res.raise_for_status()
		for key in st.session_state.keys():
			value = st.session_state.pop(key, None)
			# logger.info(f"Cleaned '{key}' value: {value}")
		# st.success("Restarted successfully.")
		logger.info("Session state cleaned")
	except Exception as e:
		st.error("Error cleaning up the app")
		logger.error(f"Error cleaning session state: {str(e)}")


def enable_process_pdf_button(file_uploaded) -> bool:
	"""Enable process PDF button"""
	if file_uploaded is not None:
		st.session_state["pdf_process_button_disabled"] = False
	else:
		st.session_state["pdf_process_button_disabled"] = True


def main():
	"""Run the client"""
	st.header("🦮 :blue[Tame Your PDF] 🙂🤖", divider="blue", anchor=False)

	# Init session state (only once)
	init_states_dict = {
		"messages": [],
		"pdf_pages": [],
		"vector_db_ready": False,
		"pdf_process_button_disabled": True,
		"model_selected": None,
	}
	for key, default_value in init_states_dict.items():
		if key not in st.session_state:
			st.session_state[key] = default_value
			logger.info(f"Session state: '{key}: {default_value}' initialized")

	# Upload file
	st.subheader("1️⃣ Upload PDF")

	file_uploaded = st.file_uploader(
		"1️⃣ Upload PDF",
		type=["pdf"],
		accept_multiple_files=False,
		key="pdf_uploader",
		help="Upload a PDF file to ask questions about it",
		# on_change=enable_process_pdf_button,
		label_visibility="collapsed",
	)

	if file_uploaded:
		st.session_state["pdf_process_button_disabled"] = False
	else:
		st.session_state["pdf_process_button_disabled"] = True

	# setup layout
	col1, col2 = st.columns([1.8, 2])

	col1.subheader("2️⃣ Prepare PDF for Chat")
	pdf_proccess_button = col1.button(
		"Submit PDF",
		icon="📲",
		type="secondary",
		key="process_pdf_button",
		help="Process pdf to get it ready for the chat",
		use_container_width=True,
		disabled=st.session_state["pdf_process_button_disabled"],
	)

	logger.info("File uploaded for preview")
	col1.subheader("PDF Preview")
	if file_uploaded:
		with st.spinner(":green[Generating PDF preview ...]"):
			st.session_state["pdf_pages"] = extract_all_pages_as_images(
				file_uploaded
			)
	else:
		st.session_state["pdf_pages"] = None
		with col1, st.container(height=None, border=True):
			st.write("*No file uploaded*")

	# Display PDF pages
	if st.session_state.get("pdf_pages"):
		with col1, st.container(height=400, border=True):
			for page in st.session_state["pdf_pages"]:
				st.image(page, use_container_width=True)

	# list local models
	models = tuple()
	if st.session_state.get("pdf_pages"):
		response = requests.get(f"{BACKEND_URL}/list/models")
		models = response.json()["models"]
		# ensure the order of the models for consistency
		# and to allow us to use indexing to maintian state on UI
		models.sort()

	if pdf_proccess_button:
		logger.info("File submited to create vector database")
		with st.spinner(":green[processing PDF...]"):
			files = {
				"file": (file_uploaded.name, file_uploaded, file_uploaded.type)
			}
			response = requests.post(f"{BACKEND_URL}/upload", files=files)
			logger.info("Generating PDF embeddings and storing them in vdb")
			st.session_state["vector_db_ready"] = True

			logger.info("PDF stored and processed successfully")
			st.session_state["pdf_process_button_disabled"] = True

	# Delete all button (refresh)
	st.button(
		icon="🔥",
		label="Delete All",
		type="secondary",
		key="delete_all",
		help="Deletes pdf and all associated data to start over",
		use_container_width=True,
		on_click=clean_session,
	)

	# Chat interface
	with col2:
		col2.subheader("3️⃣ Pick a Model")

		# recover the index of the current selected model
		# so that we can maintain the state of the selectbox
		selected_model_index = (
			models.index(st.session_state["model_selected"])
			if st.session_state["model_selected"]
			else None
		)

		col2.selectbox(
			"3️⃣ Pick a Model",
			models,
			index=selected_model_index,
			key="model_select",
			label_visibility="collapsed",
			# use the selected value to change session var state
			on_change=lambda: st.session_state.update(
				{"model_selected": st.session_state["model_select"]}
			),
		)

		col2.subheader("Chat")
		message_container = st.container(height=400, border=True)

		# Display chat history
		for i, message in enumerate(st.session_state["messages"]):
			avatar = "🤖" if message["role"] == "assistant" else "🤓"
			with message_container.chat_message(message["role"], avatar=avatar):
				st.markdown(message["content"])

		# Chat input and processing
		if prompt := st.chat_input(
			"Enter a prompt here...",
			key="chat_input",
			disabled=st.session_state["vector_db_ready"] != 1,
		):
			try:
				# Add user message to chat
				st.session_state["messages"].append(
					{"role": "user", "content": prompt}
				)
				with message_container.chat_message("user", avatar="🤓"):
					st.markdown(prompt)

				# Process and display assistant response
				with message_container.chat_message("assistant", avatar="🤖"):
					with st.spinner(":green[processing...]"):
						if st.session_state["vector_db_ready"] is not None:
							try:
								response = requests.post(
									f"{BACKEND_URL}/question",
									json={
										"prompt": prompt,
										"model": st.session_state["model_selected"],
									},
								)
								response.raise_for_status()
								response_json = response.json()
								response_data = response_json["response"]
								st.markdown(response_data)
							except requests.exceptions.HTTPError as e:
								logger.error(f"HTTP error: {e}")
								if st.session_state["model_selected"] is None:
									st.error(
										"😵 Error processing the request. "
										"Don't forget to select a model."
									)
								else:
									st.error(
										"😵 Error processing the request. Please try again."
									)
								response_data = None

				# Add assistant response to chat history
				if (
					st.session_state["vector_db_ready"] is not None and response_data
				):
					st.session_state["messages"].append(
						{"role": "assistant", "content": response_data}
					)

			except Exception as e:
				st.error(f"Error processing prompt:\n*{e}*", icon="😵")
				logger.error(f"Error processing prompt: {e}")


if __name__ == "__main__":
	# run the app
	main()
