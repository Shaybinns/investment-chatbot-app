FROM python:3.9-slim

WORKDIR /app

# Copy requirements first to leverage Docker cache
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy the application
COPY . .

# Set Python path correctly
ENV PYTHONPATH=/app

# Expose the port
EXPOSE 8000

# Run the application using the correct import string format
CMD ["uvicorn", "src.main:app", "--host", "0.0.0.0", "--port", "8000"]