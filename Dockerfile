FROM python:3.12.4-slim AS base
FROM base AS builder

# Allows docker to cache installed dependencies between builds
RUN apt-get update && apt-get install -y libpq-dev gcc
COPY requirements/base.txt requirements.txt
RUN pip3 install --no-cache-dir --target=packages -r requirements.txt

FROM base AS runtime
COPY --from=builder packages /usr/lib/python3.12/site-packages
ENV PYTHONPATH=/usr/lib/python3.12/site-packages

# Security Context
RUN useradd -m nonroot
USER nonroot

WORKDIR /app
COPY . .

EXPOSE 8000
# Run the production server
CMD newrelic-admin run-program gunicorn --bind 0.0.0.0:$PORT --access-logfile - library_app.wsgi:application
