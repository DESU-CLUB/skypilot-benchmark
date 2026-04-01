FROM ubuntu:22.04

LABEL Author="jj-task-builder"
LABEL description="jj task: restore working copy files - manage working-copy states and restore accidentally changed files"

ENV DEBIAN_FRONTEND=noninteractive

RUN apt-get update && apt-get install -y \
    curl \
    ca-certificates \
    git \
    python3 \
    python3-pip \
    bash \
    && rm -rf /var/lib/apt/lists/*

RUN pip3 install --no-cache-dir pytest

RUN curl -sSL https://github.com/jj-vcs/jj/releases/download/v0.38.0/jj-v0.38.0-x86_64-unknown-linux-musl.tar.gz \
    | tar -xz -C /usr/local/bin ./jj \
    && chmod +x /usr/local/bin/jj

RUN mkdir -p /home/user && chmod 0755 /home/user

# Configure jj global identity
RUN jj config set --user user.name "Dev User" \
    && jj config set --user user.email "dev@example.com"

RUN mkdir -p /home/user/webserver/src

COPY --chmod=644 <<'EOF' /home/user/webserver/Cargo.toml
[package]
name = "webserver"
version = "0.1.0"
edition = "2021"

[dependencies]
EOF

COPY --chmod=644 <<'EOF' /home/user/webserver/README.md
# Webserver

A simple web server implementation in Rust.

## Getting Started

Run with `cargo run`.

## Contributors

EOF

COPY --chmod=644 <<'EOF' /home/user/webserver/src/main.rs
fn main() {
    println!("Starting webserver...");
    println!("Listening on 0.0.0.0:8080");
}
EOF

COPY --chmod=644 <<'EOF' /home/user/webserver/src/config.rs
pub struct Config {
    pub host: String,
    pub port: u16,
}

impl Config {
    pub fn new(host: &str, port: u16) -> Self {
        Config {
            host: host.to_string(),
            port,
        }
    }
}
EOF

RUN cd /home/user/webserver \
    && jj git init \
    && jj config set --repo user.name "Dev User" \
    && jj config set --repo user.email "dev@example.com" \
    && jj describe -m "initial project scaffold" \
    && jj new -m "add rate limiting feature" \
    && printf 'TODO: placeholder - needs rewrite\n' > /home/user/webserver/src/main.rs \
    && rm /home/user/webserver/src/config.rs \
    && printf '- Dev User (contributor)\n' >> /home/user/webserver/README.md

CMD ["/bin/bash"]
