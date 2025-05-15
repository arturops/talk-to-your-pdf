# Getting Started with talk-to-your-pdf

This is a simple repo to have a pdf being read, chunked and able to get questions using ChatGPT

## Setup

1. Use `pyenv` or any other virtualenv tool to create a python 3.11 environment

   > NOTE: this specific repo uses python 3.11.6

2. In the root folder and once you activate your environment run `pip install -r requirements.txt`
3. Create a `.env` file in the root level and add the following:
   1. `OPENAI_API_KEY=<YOUR_API_KEY_VALUE>`
4. In the `files` directory add one `.pdf` which you would want to use to ask questions about.
5. In the root folder run `python main.py`
