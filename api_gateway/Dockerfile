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
# Expose the port that the app runs on
EXPOSE 8000

# Command to run the application
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
