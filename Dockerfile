FROM python:3.11-slim

# Install system dependencies including MySQL client
RUN apt-get update && apt-get install -y \
    default-libmysqlclient-dev \
    build-essential \
    pkg-config \
    wait-for-it \
    && rm -rf /var/lib/apt/lists/*

# Set up game directory
WORKDIR /usr/src/game

# Install uv
COPY --from=ghcr.io/astral-sh/uv:latest /uv /uvx /bin/

# Copy dependency files
COPY pyproject.toml uv.lock ./

# Install dependencies system-wide using uv
RUN uv pip install --system .

# Copy the game files
COPY pixarimud /usr/src/game/pixarimud/
COPY README.md ./

# Install the game package in development mode
RUN uv pip install --system -e .

# Set the working directory to the game directory
WORKDIR /usr/src/game/pixarimud

CMD ["evennia", "start", "-l"]
