FROM ubuntu:22.04

LABEL Author="jj-task-builder"
LABEL Description="jj task: apply templates and commit metadata fields - audit log extraction for data team"

ENV DEBIAN_FRONTEND=noninteractive

RUN apt-get update && apt-get install -y \
    curl \
    ca-certificates \
    git \
    python3 \
    python3-pip \
    bash \
    && rm -rf /var/lib/apt/lists/*

RUN pip3 install pytest

RUN curl -fsSL https://github.com/jj-vcs/jj/releases/download/v0.38.0/jj-v0.38.0-x86_64-unknown-linux-musl.tar.gz \
    | tar -xz -C /usr/local/bin ./jj

RUN mkdir -p /home/user && chmod 0755 /home/user

RUN git config --global user.email "setup@bootstrap" && \
    git config --global user.name "Bootstrap"

WORKDIR /home/user

RUN jj git init /home/user/audit-repo

RUN jj -R /home/user/audit-repo config set --repo user.name "data-bot" && \
    jj -R /home/user/audit-repo config set --repo user.email "data-bot@company.com"

RUN jj -R /home/user/audit-repo describe -m "$(printf 'ingest: load raw CSV files from landing zone\n\nReviewer: alice\nTicket: DATA-101')" && \
    jj -R /home/user/audit-repo metaedit --update-author && \
    jj -R /home/user/audit-repo new

RUN jj -R /home/user/audit-repo describe -m "$(printf 'transform: normalize column types and rename fields\n\nReviewer: bob\nTicket: DATA-102')" && \
    jj -R /home/user/audit-repo new

RUN jj -R /home/user/audit-repo describe -m "$(printf 'validate: run schema checks on transformed dataset\n\nReviewer: alice\nTicket: DATA-103')" && \
    jj -R /home/user/audit-repo new

RUN jj -R /home/user/audit-repo describe -m "$(printf 'enrich: join with reference table for geo lookups\n\nReviewer: carol\nTicket: DATA-104')" && \
    jj -R /home/user/audit-repo new

RUN jj -R /home/user/audit-repo describe -m "$(printf 'export: write final parquet files to output bucket\n\nReviewer: bob\nTicket: DATA-105')" && \
    jj -R /home/user/audit-repo new

CMD ["/bin/bash"]
