FROM ubuntu

RUN apt-get update

RUN apt-get install -y git python3 python3-pip

COPY main.py /main.py

#COPY print_hello.py /bin/print_hello.py

RUN echo "#!/usr/bin/env sh" > /bin/print_hello
RUN echo "''':'" >> /bin/print_hello
RUN echo "DOCKER_IMAGE=python:3" >> /bin/print_hello
RUN echo 'DOCKER_CMD="python -tt"' >> /bin/print_hello
RUN echo "DOCKER_EXTRA_ARGS='-w $(pwd) -u $(id -u):$(id -g) -v $(pwd):$(pwd):rw'" >> /bin/print_hello
RUN echo "s="$(cd "$(dirname "$0")" && pwd)/$(basename "$0")";docker run --rm -a stdin -a stdout -a stderr -i$([ -t 0 ] && echo t) --init -v "$s":"$s":ro ${DOCKER_EXTRA_ARGS} ${DOCKER_IMAGE} ${DOCKER_CMD} "$s" "$@";exit $?" >> /bin/print_hello
RUN echo "print('Hello')" >> /bin/print_hello

RUN chmod +x /bin/print_hello

#RUN -python /bin/print_hello

#ENTRYPOINT ["/bin/print_hello", "/bin", "-python", "print_hello.py"]

COPY README.md /README.md

COPY requirements.txt /requirements.txt

RUN pip install -r requirements.txt

RUN useradd -ms /bin/bash deploy2022user

USER deploy2022user

CMD ["uvicorn", "--host", "0.0.0.0", "--port", "8898", "main:app"]