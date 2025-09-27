# Builder stage: Install python dependencies
FROM python:3.11-slim as builder

# Set environment variables for the build process
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1
ENV PATH="/home/django/.local/bin:$PATH"

# Create and set the working directory
WORKDIR /app

# Copy the requirements file early for better build caching
COPY requirements.txt .

# Install system dependencies (needed to build python packages like psycopg2),
# run pip install, and then remove the build dependencies and cleanup
# all in a single layer for maximum efficiency and minimum image size.
RUN apt-get update \
    && apt-get install --no-install-recommends -y \
    gcc \
    libpq-dev \
    musl-dev \
    libffi-dev \
    # postgresql-client is useful to keep for debugging/entrypoint in this stage
    postgresql-client \
    # Install Python packages
    && pip install --upgrade pip \
    && pip install --no-cache-dir -r requirements.txt \
    # Explicitly remove build-only dependencies
    && apt-get remove --purge -y gcc libpq-dev musl-dev libffi-dev \
    && apt-get autoremove -y \
    # Final cleanup of apt lists and temp files
    && rm -rf /var/lib/apt/lists/* /tmp/* /var/tmp/*

# Final stage: Minimal runtime image
FROM python:3.11-slim

# Install system dependencies needed for runtime (pg_isready and networking tools)
RUN apt-get update \
    && apt-get install --no-install-recommends -y \
    postgresql-client \
    # Clean up to keep image small
    && rm -rf /var/lib/apt/lists/*

# Create and set the working directory
WORKDIR /app

# Create a non-root user for security
RUN adduser --system --group django
ENV HOME /home/django

# Copy the entrypoint script and ensure it's executable
COPY --chmod=0755 entrypoint.sh /usr/local/bin/entrypoint.sh

# Copy dependencies from the builder stage
COPY --from=builder /usr/local/lib/python3.11/site-packages /usr/local/lib/python3.11/site-packages
COPY --from=builder /usr/local/bin/gunicorn /usr/local/bin/
COPY --from=builder /home/django/.local /home/django/.local

# Copy application code
COPY . /app

# Change ownership of the application directory to the non-root user
RUN chown -R django:django /app

# Use the non-root user
USER django

# Expose the Gunicorn port
EXPOSE 8000

# Set the entrypoint script as the command to run
ENTRYPOINT ["/usr/local/bin/entrypoint.sh"]

# Default command (used as argument to ENTRYPOINT)
CMD ["gunicorn", "--bind", "0.0.0.0:8000", "ChronosAtlas.wsgi:application"]
