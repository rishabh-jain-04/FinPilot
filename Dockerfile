FROM python:3.12-slim

WORKDIR /app

# build-essential is a fallback in case pip can't find prebuilt wheels for
# spaCy's compiled deps (blis, thinc, cymem, ...) on this image's platform.
RUN apt-get update && apt-get install -y --no-install-recommends build-essential \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

ENV PORT=8080
EXPOSE 8080

CMD ["python", "serve.py"]
