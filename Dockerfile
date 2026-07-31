FROM python:3.12-slim

# Prevent Python from creating .pyc files
ENV PYTHONDONTWRITEBYTECODE=1

# Print logs immediately
ENV PYTHONUNBUFFERED=1

WORKDIR /app

COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt
    
COPY . .

EXPOSE 8000

CMD ["gunicorn", "core.wsgi:application", "--bind","0.0.0.0:8000", "--access-logfile","-"]
#  --access-logfile - enables Gunicorn request/access logs and sends them to Docker stdout, instead of only seeing startup and error logs.
