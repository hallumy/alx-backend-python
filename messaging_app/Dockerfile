FROM python:3.10

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

WORKDIR /app

# Copy requirements from same folder as Dockerfile
COPY requirements.txt /app/

RUN pip install --upgrade pip && \
    pip install -r requirements.txt

# Copy Django project folder (settings.py, etc.)
COPY . /app/

# docker run -p 8000:8000
EXPOSE 8000

CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
