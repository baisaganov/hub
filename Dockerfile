FROM ubuntu:noble
WORKDIR /usr/workspace
EXPOSE 8080
COPY uv.lock pyproject.toml .

RUN apt-get update &&  \
    apt-get install -y --no-install-recommends curl ca-certificates openjdk-17-jre-headless wget &&  \
    apt-get clean &&  \
    rm -rf /var/lib/apt/lists/*

RUN wget -q https://github.com/allure-framework/allure2/releases/download/2.32.0/allure-2.32.0.tgz \
    && tar -zxf allure-2.32.0.tgz -C /opt/ \
    && ln -s /opt/allure-2.32.0/bin/allure /usr/bin/allure \
    && rm allure-2.32.0.tgz


# Install UV
ADD https://astral.sh/uv/install.sh /uv-installer.sh
RUN sh /uv-installer.sh && rm /uv-installer.sh
ENV PATH="/root/.local/bin/:$PATH"


# Install python packages
RUN uv sync
ENV PATH="/usr/workspace/.venv/bin:$PATH"

# Install playwright btowers
RUN playwright install --with-deps chromium

COPY . .

#uv run pytest
#FROM ubuntu:24.04
#
#WORKDIR /usr/workspace
#
## Сначала базовые пакеты + curl
#RUN apt-get update && \
#    apt-get install -y --no-install-recommends \
#    curl \
#    ca-certificates \
#    gnupg \
#    apt-transport-https && \
#    apt-get clean && \
#    rm -rf /var/lib/apt/lists/*
#
## Node.js 20
#RUN curl -fsSL https://deb.nodesource.com/setup_20.x | bash -
#
## Основные пакеты
#RUN apt-get install -y --no-install-recommends \
#    nodejs \
#    default-jre-headless \
#    python3 \
#    python3-pip \
#    python3-venv && \
#    apt-get clean && \
#    rm -rf /var/lib/apt/lists/*
#
## venv
#RUN python3 -m venv /opt/venv
#ENV PATH="/opt/venv/bin:$PATH"
#
## Allure CLI
#RUN npm install -g allure-commandline
#
#COPY requirements.txt .
#RUN pip install --upgrade pip && \
#    pip install --no-cache-dir -r requirements.txt
#
#RUN playwright install --with-deps chromium
#
#COPY . .
#
#ENV PYTHONUNBUFFERED=1
#
#CMD ["/bin/sh", "-c", "pytest -sv --alluredir=allure-results || true; allure generate allure-results --clean -o allure-report"]
