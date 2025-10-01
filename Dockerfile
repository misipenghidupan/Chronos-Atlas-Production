# --- STAGE 1: Builder (Optimized for Dependency Installation) ---
FROM python:3.11-slim AS builder

    # Set environment variables for Python optimization
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
    
    # Install system dependencies and build tools needed for psycopg2
    RUN apt-get update \
        && apt-get install --no-install-recommends -y \
        gcc \
        libpq-dev \
        # Install dependencies needed for static files (if any)
        # and clean up in a single layer
        && pip install --upgrade pip
    
    # Set the working directory
    WORKDIR /app
    
    # Copy requirements file and install Python dependencies
    COPY requirements.txt .
    
    # Install dependencies and then remove build tools to keep the layer lean
    RUN pip wheel --no-cache-dir --no-deps --wheel-dir /usr/src/app/wheels -r requirements.txt \
        && apt-get purge -y --auto-remove gcc libpq-dev
    
    # --- STAGE 2: Final (Minimal Runtime Image) ---
FROM python:3.11-slim AS final
    
    # Set environment variables
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
    
    # Set the working directory
    WORKDIR /app
    
    # Install runtime dependencies (libpq-dev dependencies without the dev headers)
    # FIX: Added 'postgresql-client' here, which provides the 'pg_isready' command
    RUN apt-get update \
        && apt-get install --no-install-recommends -y \
        libpq5 \
        postgresql-client \
        git \
        # Clean up APT cache to reduce image size
        && rm -rf /var/lib/apt/lists/*
    # Install pre-commit globally for code checks inside container
    RUN pip install pre-commit
    
    # Copy pre-built wheels from the builder stage
    COPY --from=builder /usr/src/app/wheels /wheels
    # Install packages from wheels
    RUN pip install --no-cache-dir /wheels/*
    
    # Copy the rest of the application code
    COPY . /app
    
    # Ensure entrypoint.sh is executable and copy it to the bin directory
    # Note: The entrypoint script path must match the ENTRYPOINT instruction below.
    COPY scripts/entrypoint.sh /usr/local/bin/entrypoint.sh
    RUN chmod +x /usr/local/bin/entrypoint.sh
    
    # Expose the application port
    EXPOSE 8000
    
    # Specify the default command to run the application
    # Use the correct path for the entrypoint script
    ENTRYPOINT ["/usr/local/bin/entrypoint.sh"]
    