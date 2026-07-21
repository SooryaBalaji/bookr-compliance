# 1. The Base: Start with a highly optimized version of Python 3.12
FROM python:3.12-slim

# 2. The Workspace: Create a folder inside the container called /app
WORKDIR /app

# 3. Security & Performance: Prevent Python from writing temporary files and crashing logs
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# 4. Dependencies: Copy your grocery list into the container
COPY requirements.txt .

# 5. Installation: Tell the container to install FastAPI, SQLAlchemy, etc.
RUN pip install --no-cache-dir -r requirements.txt

# 6. The Code: Copy all your Python and HTML files into the container
COPY . .

# 7. Run as a non-root user — the app has no reason to run as root inside the container.
RUN useradd --create-home --shell /bin/bash appuser \
    && chown -R appuser:appuser /app
USER appuser

# 8. The Ignition: The exact command to boot the server when the container turns on
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]