# Dockerfile
FROM python:3.9

WORKDIR /anti-mage

COPY requirements.txt .

RUN pip install --no-cache-dir --upgrade -r requirements.txt

COPY ./app /app

# Env
RUN --mount=type=secret,id=DATABASE_URL \
  --mount=type=secret,id=AWS_ACCESS_KEY_ID \
  --mount=type=secret,id=AWS_SECRET_ACCESS_KEY \
  --mount=type=secret,id=AWS_DEFAULT_REGION \
  export DATABASE_URL=$(cat /run/secrets/DATABASE_URL) && \
  export AWS_ACCESS_KEY_ID=$(cat /run/secrets/AWS_ACCESS_KEY_ID) && \
  export AWS_SECRET_ACCESS_KEY=$(cat /run/secrets/AWS_SECRET_ACCESS_KEY) && \
  export AWS_DEFAULT_REGION=$(cat /run/secrets/AWS_DEFAULT_REGION) && \

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--reload", "--port 8000"]
