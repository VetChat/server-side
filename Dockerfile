# Dockerfile
FROM python:3.9

WORKDIR /anti-mage

# Add the root directory to the PYTHONPATH
ENV PYTHONPATH=/

COPY requirements.txt .

RUN pip install --no-cache-dir --upgrade -r requirements.txt

# Use ARG to get the build-args and ENV to set the environment variables
ARG DATABASE_URL
ARG AWS_ACCESS_KEY_ID
ARG AWS_SECRET_ACCESS_KEY
ARG AWS_DEFAULT_REGION

ENV DATABASE_URL=$DATABASE_URL
ENV AWS_ACCESS_KEY_ID=$AWS_ACCESS_KEY_ID
ENV AWS_SECRET_ACCESS_KEY=$AWS_SECRET_ACCESS_KEY
ENV AWS_DEFAULT_REGION=$AWS_DEFAULT_REGION

COPY ./app /app

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--reload", "--port", "80"]
