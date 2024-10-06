FROM nvidia/cuda:12.1.1-runtime-ubuntu22.04

RUN apt-get update && apt-get install -y \
    python3-pip \
    portaudio19-dev \
    python3-pyaudio \
    python3-dev \
    wget \
    git \
    openssh-client \
    ffmpeg \
    libsm6 \
    libxext6 \
    zsh \
    vim \
    tmux \
    && rm -rf /var/lib/apt/lists/*

RUN pip3 install --upgrade pip setuptools

WORKDIR /workspace

COPY Makefile requirements.txt ./

RUN make install
RUN make ffmpeg-install
ENV FFMPEG_PATH=./ffmpeg-git-20240629-amd64-static/

EXPOSE 8080

CMD ["python3", "app.py"]

COPY . .