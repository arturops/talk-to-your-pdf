# Must use slim-bullseye since alpine had issues installing faiss-cpu
FROM python:3.11-slim-bullseye

WORKDIR /backend

# Install dependencies
COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

# Copy the application code
COPY . .

# Expose fastapi port
EXPOSE 8000

# Run app
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000", "--reload"]
# --reload is for development only, remove it in production

