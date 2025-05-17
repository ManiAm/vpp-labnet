FROM ubuntu:20.04

ENV DEBIAN_FRONTEND=noninteractive

RUN apt-get update && apt-get install -y \
    sudo \
    nano \
    curl \
    lsb-release \
    gnupg2 \
    iputils-ping \
    net-tools \
    iproute2

RUN echo deb [trusted=yes] https://packagecloud.io/fdio/release/ubuntu focal main > /etc/apt/sources.list.d/99fdio.list

RUN curl -L https://packagecloud.io/fdio/release/gpgkey | apt-key add -

RUN apt-get update && apt-get install -y \
    vpp \
    vpp-plugin-core \
    vpp-plugin-dpdk \
    vpp-dev \
    vpp-dbg \
    python3-vpp-api

# setting up FRR

# Add the GPG key
RUN curl -s https://deb.frrouting.org/frr/keys.gpg | tee /usr/share/keyrings/frrouting.gpg > /dev/null

# FRR version
ARG FRRVER="frr-10"

# Add the FRR repository
RUN echo "deb [signed-by=/usr/share/keyrings/frrouting.gpg] https://deb.frrouting.org/frr $(lsb_release -s -c) $FRRVER" | tee -a /etc/apt/sources.list.d/frr.list

RUN apt-get update && apt-get install -y \
    frr \
    frr-pythontools

# entry point

COPY startup-script.sh /usr/local/bin/

RUN chmod +x /usr/local/bin/startup-script.sh

ENTRYPOINT ["/usr/local/bin/startup-script.sh"]
