FROM python:3.12-slim

# Install SQLite
RUN apt-get update && apt-get install -y sqlite3

WORKDIR /app

# Install the application dependencies
COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

# Copy in the source code
COPY . /app/
EXPOSE 8000

# Setup an app user so the container doesn't run as the root user
 RUN useradd app
 USER app

CMD ["python", "app.py"]