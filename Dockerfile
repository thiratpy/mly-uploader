# Dockerfile.uploader
FROM python:3.10-slim

WORKDIR /app

RUN pip install fastapi "uvicorn[standard]" python-multipart

COPY uploader_main.py .

# Expose port 8000
EXPOSE 8000

# Command to run the Uvicorn server
CMD ["uvicorn", "uploader_main:app", "--host", "0.0.0.0", "--port", "8000"]