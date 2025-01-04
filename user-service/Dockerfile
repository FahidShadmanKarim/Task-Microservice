FROM python:3.10

# Set the working directory to /app
WORKDIR /app

# Copy the requirements file to install dependencies
COPY requirements.txt ./

# Install the Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the entire project folder
COPY . . 

# Ensure the Python module path includes /app
ENV PYTHONPATH=/app

EXPOSE 8000

# Run the FastAPI application
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
