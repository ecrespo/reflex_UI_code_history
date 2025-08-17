# Dockerfile for self-hosting Reflex with Docker
# Based on: https://reflex.dev/blog/2024-10-8-self-hosting-reflex-with-docker

# 1) Base image with Python and Bun (for building and runtime where needed)
FROM python:3.12-slim AS base
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    REFLEX_ENV=prod \
    BUN_INSTALL=/root/.bun \
    PATH=/root/.local/bin:$PATH
WORKDIR /app
RUN apt-get update \
    && apt-get install -y --no-install-recommends bash curl ca-certificates xz-utils \
    && rm -rf /var/lib/apt/lists/* \
    && update-ca-certificates \
    && curl -fsSL https://bun.sh/install | bash \
    && ln -s /root/.bun/bin/bun /usr/local/bin/bun \
    && curl -LsSf https://astral.sh/uv/install.sh | sh
# Copy dependency files first to leverage Docker layer caching
COPY pyproject.toml uv.lock ./
# Use uv to install project dependencies into the system environment
RUN uv sync --frozen --no-dev --system

# 2) Builder: export the app (frontend assets and backend)
FROM base AS builder
COPY . .
# Produce exported artifacts into .web directory
RUN reflex export --no-zip

# 3) Frontend image: serve static site from export
FROM base AS frontend
# Only copy the exported static site to keep image smaller
COPY --from=builder /app/.web /app/.web
EXPOSE 3000
# Serve the exported frontend statically
# Note: bunx 'serve' serves static content from the given directory
CMD ["bunx", "--yes", "serve", "-s", "/app/.web", "-l", "3000"]

# 4) Backend image: run Reflex backend only (ASGI)
FROM base AS backend
COPY . .
EXPOSE 8000
# Run the Reflex backend only; the frontend is served separately by the frontend image
CMD ["sh", "-c", "reflex run --env prod --backend-only --port 8000"]
