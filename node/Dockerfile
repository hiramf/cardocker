#-------------------------------------------------------------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License. See https://go.microsoft.com/fwlink/?linkid=2090316 for license information.
#-------------------------------------------------------------------------------------------------------------

FROM rust:1 as base

# Tini
ENV TINI_VERSION v0.18.0
ADD https://github.com/krallin/tini/releases/download/${TINI_VERSION}/tini /tini
RUN chmod +x /tini

# Avoid warnings by switching to noninteractive
ENV DEBIAN_FRONTEND=noninteractive

# Configure apt and install packages
RUN apt-get update \
    && apt-get -y install --no-install-recommends apt-utils dialog 2>&1 \
    && apt-get -y install git iproute2 procps lsb-release \
    # Rust
    && rustup update \
    && rustup install stable \
    && rustup default stable

FROM base as vscode

ARG USERNAME=vscode
ARG USER_UID=1000
ARG USER_GID=$USER_UID

RUN groupadd --gid $USER_GID $USERNAME \
    && useradd -s /bin/bash --uid $USER_UID --gid $USER_GID -m $USERNAME \
    # [Optional] Add sudo support for the non-root user
    && apt-get install -y sudo \
    && echo $USERNAME ALL=\(root\) NOPASSWD:ALL > /etc/sudoers.d/$USERNAME\
    && chmod 0440 /etc/sudoers.d/$USERNAME \
    # Install lldb, vadimcn.vscode-lldb VSCode extension dependencies
    && apt-get install -y lldb python3-minimal libpython3.7 \
    # Install Rust components
    && rustup component add rls rust-analysis rust-src rustfmt clippy \
    #
    # Clean up
    && apt-get autoremove -y \
    && apt-get clean -y \
    && rm -rf /var/lib/apt/lists/*

# Switch back to dialog for any ad-hoc use of apt-get
ENV DEBIAN_FRONTEND=dialog

# VSCode Remote-Containers Setup
FROM vscode as jormungandr
WORKDIR /workspaces/

ARG RELEASE
ENV RELEASE ${RELEASE:-v0.8.5}
RUN git clone --recurse-submodules https://github.com/input-output-hk/jormungandr

WORKDIR /workspaces/jormungandr
RUN git checkout tags/${RELEASE} \
    && git submodule update \
    && cargo install --path ./jormungandr \
    && cargo install --path ./jcli

# Setup Testnet Node
FROM jormungandr

ENV PATH "${PATH}:${CARGO_HOME}/bin"
WORKDIR /workspaces/jormungandr/scripts

RUN sudo chown -R 1000 ${CARGO_HOME} \
    && mv bootstrap bootstrap.sh \
    && sudo chmod +x bootstrap.sh \
    && mv create-account-and-delegate.shtempl create-account-and-delegate.sh \
    && mv faucet-send-certificate.shtempl faucet-send-certificate.sh \
    && mv faucet-send-money.shtempl faucet-send-money.sh \
    && mv send-transaction send-transaction.sh \
    && sudo chmod +x create-account-and-delegate.sh \
    && sudo chmod +x faucet-send-certificate.sh \
    && sudo chmod +x faucet-send-money.sh \
    && sudo chmod +x send-transaction.sh
    #&& ./bootstrap.sh

WORKDIR /workspaces
COPY . .
RUN sudo chown -R 1000 .

EXPOSE 8299

ENTRYPOINT ["/tini", "-g", "--"]
#CMD ["jormungandr", "--genesis-block", "block-0.bin", "--config", "config.yaml", "--secret", "pool-secret1.yaml"]