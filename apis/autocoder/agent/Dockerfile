FROM python:3.11-slim

WORKDIR /app

# Install required packages
RUN pip install pytest requests-mock pytest-mock requests

# Copy the entire agent directory
COPY . /app/

# Set environment variables
ENV PYTHONPATH=/app

# Run tests
CMD ["python", "-m", "pytest", "/app/test_generated.py", "-v"] 