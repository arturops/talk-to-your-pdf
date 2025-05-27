FROM python:3.11-alpine
# Set the working directory
WORKDIR /app
# Install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
# Copy the application code
COPY . .
# Expose streamlit app
EXPOSE 8501
# Run app
CMD ["streamlit", "run", "index.py", "--server.port=8501", "--server.address=0.0.0.0"]