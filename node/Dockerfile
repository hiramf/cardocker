FROM rust:1 as base

# Configure apt and install packages
RUN apt-get update \
    && apt-get install -y --no-install-recommends \
    git \
    build-essential \
    libsystemd-dev \
    libprotoc-dev \
    && apt-get autoremove -y \
    && apt-get clean -y \
    && rm -rf /var/lib/apt/lists/* \
    # Rust
    && rustup update \
    && rustup install stable \
    && rustup default stable

FROM base as build

ARG RELEASE
ENV RELEASE ${RELEASE:-v0.7.0}

WORKDIR /app/src

RUN git clone --recurse-submodules https://github.com/input-output-hk/jormungandr . \
    && git checkout tags/${RELEASE} \
    && git submodule update --recursive \
    && cargo install --path jormungandr --features systemd \
    && cargo install --path jcli \
    && curl -L https://github.com/input-output-hk/cardano-wallet/releases/download/v2019-12-23/cardano-wallet-jormungandr-linux64-v2019-12-23.tar.gz | tar xz

# Setup Testnet Node
FROM debian:buster-slim

# Tini
ENV TINI_VERSION v0.18.0
ADD https://github.com/krallin/tini/releases/download/${TINI_VERSION}/tini /tini
RUN chmod +x /tini

ARG PREFIX
ENV ENV_PREFIX=${PREFIX:-/app}
ENV PATH=${ENV_PREFIX}/bin:${PATH}

WORKDIR ${ENV_PREFIX}/bin

COPY --from=build /usr/local/cargo/bin/jormungandr .
COPY --from=build /usr/local/cargo/bin/jcli .
COPY --from=build /app/src/cardano-wallet .
COPY --from=build /app/src/scripts ./scripts

RUN apt-get update \
    && apt-get install -y --no-install-recommends \
    python3-pip \
    python3-setuptools \
    && pip3 install wheel \
    && apt-get autoremove -y \
    && apt-get clean -y \
    && rm -rf /var/lib/apt/lists/* \
    # Cardano Wallet
    && ln -s /usr/lib/x86_64-linux-gnu/libcrypto.so.1.1 /usr/lib/libcrypto.so.1.0.0


COPY . .
RUN chmod +x init.sh \
    && pip3 install -r requirements.txt


EXPOSE 8299

ENTRYPOINT ["/tini", "-g", "--", "init.sh"]
CMD jormungandr --genesis-block-hash $HASH --config config.yaml

#CMD ["jormungandr", "--genesis-block", "block-0.bin", "--config", "config.yaml", "--secret", "pool-secret1.yaml"]