# 🦮Tame Your PDF

`🦮Tame Your PDF is AI an app` that helps you leverage `AI to retrieve information about a PDF, and chat with the AI about the PDF.` The best part is that your data never leaves your computer. 🦮**Tame Your PDF** lets you `stay private!` 🤫🤐


> **Note for tech brains**
>
> 🦮**Tame Your PDF** is a local RAG system that retrieves information and helps answer questions about an uploaded PDF using open source LLMs. We use FastAPI to build a server that interacts with a streamlit UI and Ollama server. It all is containerized using docker, so that it can run in any system. Since the app runs locally in your computer, it never shares your data with any AI provider.

## 🎬🍿 How to Use Demo 

https://github.com/user-attachments/assets/91a4205d-4ae8-4577-9577-757438794c85

## 🔑 Prerequisites

The minimum requirements are:

- 🐳 Docker
- 🐳📝 Docker compose
- 🛜 Internet connection to install for the first time!

> You can install [docker desktop](https://docs.docker.com/desktop/) and that will include docker and docker compose.

If you are more tech savy and want to get advantage of your MacOS, Linux or Windows machine GPU.. install `Ollama` separately and run it locally or host it somewhere else you can access it.

> Ollama version supported is 0.7.0

## 🚀 Getting Started 🏎️

First clone this repo ⭐️

There are 2 ways to run the app:

### 1. Take it for a walk ASAP 🦮💨💨

The simplest and fastest way to get the app running (never said optimal) is to clone this repo, and in the directory of this repo in the terminal type:

`$ docker-compose up --build`

Wait for like 5 minutes max to fully use the app if your internet is not slow

> First time we download models for you to use, so bear with it second time around should be faster 🙇🏻🙇🏻.

You should be able to open the UI if you go to your browser and type:

`http://0.0.0.0:8501/`

Welcome and enjoy it!!!

### 2. I want to use my Ollama 🤓🦙🪮

The alternative way to start the app is by using your own `Ollama`.

> **NOTE:** We assume you run your Ollama on MacOS and we connect to `http://host.docker.internal:11434`. If that is not the case you can configure where to connect to `Ollama`, check the [Optional Setup](#-optional-setup) section.

In order to start the app `without Ollama` simply go to the root directory of the repo and type:

`$ docker-compose -f docker-compose-no-ollama.yaml up --build`

That's it! Wait for the app to start!

You should be able to open the UI if you go to your browser and type:

`http://0.0.0.0:8501/`

Welcome and enjoy it!!!

## 🎁 🎁
## Optional Setup

This section is only to describe some optional setup for more advanced users.

### Ollama server host and port configuration

If you are an enthusiast of Ollama or you have a machine with GPU then for god sake please ditch the regular way to run the app and use your own Ollama server!! You will speed up things beyond compare 🐢vs🐇! (Don't let your GPU be the rabbit and sleeps 😆)

#### Step 1: I have no Ollama in my computer

If you have Ollama installed, skip to the [next section](#step-2-i-have-my-own-ollama). Otherwise, please follow along.

There are options to install `Ollama`:

1. **Anyone level** - Simply go to [Ollama website](https://ollama.com/), download and install it just like any other app.
2. **Computer cooks** - Youuuu all know what follows 🍻 Use `brew` (mac), or `sudo-apt` (linux) or any other package manager of your choice. Maybe you figured out how to run docker Ollama with GPU ON.

#### Step 2: I have my own Ollama

Well! Start your `Ollama server`!

To do that:

1. If you have the `Ollama app` simply open it, you are all set 🙌
2. If you installed `ollama` using `brew` or any other package manager, go to your terminal and type: `$ ollama serve` and your ollama server should start.

In both cases, your default `Ollama server` runs in `http://localhost:11434` (`HOST_IP: HOST_PORT`).

So if that is your case, you need to do nothing but to [run the app without ollama](#2-i-want-to-use-my-ollama-).

However, if you have your `Ollama server` in a different `HOST_IP` or `HOST_PORT` you will need to specify them when you start the app:

`$ OLLAMA_SERVER_URL="HOST_IP:HOST_PORT" docker-compose -f docker-compose-no-ollama.yaml up --build`

That will get the app to know where to send requests to your `Ollama server` and things should work. Except you now are using your own hardware to run models! 📲🐳🦙⭐️

## 🔬📝 Future Work - Improvements

- [ ] Zoom into the pdf
- [ ] Selection of embedding model
- [ ] Download of vector database
- [ ] Use Hugging face models
- [ ] Select a chunking strategy
- [ ] Customize chunking params
- [ ] Capability to download Ollama models from UI
- [ ] Create a UI installer for less tech savy users, to auto clone the repo, install requirements and run! 🙏🙏🙏
- [ ] Visualize embeddings of PDF chunks

... suggestions welcome! 🆘📝🙏

## 🏅Credits and Thanks

- Thanks to Alireza Parandeh's book[Building Generative AI Services with FastAPI](https://learning.oreilly.com/library/view/building-generative-ai) to help me understand how to make async tasks and leverage FastAPI on LLM apps.

- Thanks to [tonykipkemboi](https://github.com/tonykipkemboi/ollama_pdf_rag) for the inspiration and some of the RAG and UI code to get started.

- Finally, thanks to all open source community: Ollama, MetaAI, Langchain, FastAPI, Streamlit, and more!

> For a simpler notebook version of this app, check my [rag notebook](https://github.com/arturops/ai-notebooks/blob/main/pdf-rag/local_pdf_rag.ipynb).
