## Dockerfile for VSCode Dev Containers
FROM python:3.11-slim AS base
## Base layer. Install packages. This layer is large, cache it first

## Ignore benign warnings due to container environment
ENV DEBIAN_FRONTEND=noninteractive

RUN apt update -y && apt upgrade -y --no-install-recommends \
    && apt install -y --no-install-recommends \
    build-essential \
    ca-certificates \
    apt-utils \
    dialog \
    neovim \
    git \
    curl \
    wget \
    iputils-ping \
    && apt-get autoremove -y \
    && apt-get clean -y \
    && rm -rf /var/lib/apt/lists/*

FROM base AS setup
## Setup layer. Set ARGs

## Set DEBIAN_FRONTEND so apt can be used interactively when
#  inside container
ENV DEBIAN_FRONTEND=dialog

ARG USERNAME=vscode
ARG USER_UID=1000
ARG USER_GID=$USER_UID

FROM setup AS stage
## Staging layer. Create user account, copy files, setup sudo, etc

## Set DEBIAN_FRONTEND so apt can be used interactively when
#  inside container
ENV DEBIAN_FRONTEND=dialog

ARG USERNAME
ARG USER_UID
ARG USER_GID
ARG DEBIAN_FRONTEND=dialog

RUN groupadd --gid $USER_GID $USERNAME \
    && useradd --uid $USER_UID --gid $USER_GID -m $USERNAME \
    && mkdir -pv /etc/sudoers.d \
    && echo $USERNAME ALL=\(root\) NOPASSWD:ALL > /etc/sudoers.d/$USERNAME \
    && chmod 0440 /etc/sudoers.d/$USERNAME

USER $USERNAME

FROM stage AS dev
## Dev layer. Use "target": "dev" in .devcontainer.json
#  to run this layer.
ENV ENV=dev
ENV ENV_FOR_DYNACONF=dev
ARG USERNAME
ARG USER_UID
ARG USER_GID
ARG DEBIAN_FRONTEND

USER $USERNAME

## Set the container's default shell to the /bin/bash
ENV SHELL /bin/bash

ENTRYPOINT ["/bin/bash"]

## Prod environment
FROM stage AS prod
## Dev layer. Use "target": "dev" in .devcontainer.json
#  to run this layer.
ENV ENV=prod
ENV ENV_FOR_DYNACONF=prod
ARG USERNAME
ARG USER_UID
ARG USER_GID
ARG DEBIAN_FRONTEND

USER $USERNAME

## Set the container's default shell to the /bin/bash
ENV SHELL /bin/bash

ENTRYPOINT ["/bin/bash"]
