FROM ubuntu:22.04

RUN apt-get update && apt-get upgrade -y
RUN apt-get install -y curl && apt-get install -y python3.11
RUN echo 'alias python="python3.11"' >> ~/.bashrc
RUN curl https://bootstrap.pypa.io/get-pip.py | python3.11

# trick to skip installation even if Docker doesn't do nice caching
RUN if ! python -c "import torch; assert torch.__version__ == '2.4.1'" 2>/dev/null; then \
    pip install torch==2.4.1; \
    fi

RUN echo "torch==2.4.1" > constraints.txt

CMD bash
