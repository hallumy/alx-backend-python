# Use official Python image as base
FROM python:3.10

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Set working directory
WORKDIR /app

# Copy requirements.txt (located in the same folder as this Dockerfile)
COPY requirements.txt /app/

# Install Python dependencies
RUN pip install --upgrade pip && \
    pip install -r requirements.txt

# Copy current folder (which includes settings.py etc.)
COPY . /app/myapp/

# Copy manage.py from parent directory (use build context properly!)
COPY ../manage.py /app/

# Expose port 8000 for Django
EXPOSE 8000

# Run Django dev server
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
