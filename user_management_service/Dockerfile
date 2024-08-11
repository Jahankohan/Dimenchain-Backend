FROM python:3.9-slim

# List directory contents before copying
# RUN echo "Current directory:" && pwd
# RUN echo "Contents of current directory:" && ls -la /
# RUN echo "Contents of parent directory:" && ls -la /..

# Copy shared library
COPY ../shared /shared

COPY requirements.txt .

# Install the specified packages
RUN pip install -r requirements.txt

COPY ./app /app

ENV PYTHONPATH="/:/app"

WORKDIR /app

EXPOSE 8002

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8002"]