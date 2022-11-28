FROM ubuntu

RUN apt-get update

RUN apt-get install -y git python3 python3-pip

COPY main.py /main.py

#COPY print_hello.py /bin/print_hello.py

RUN echo "print('Hello')" > /bin/print_hello

#RUN -python /bin/print_hello

#ENTRYPOINT ["/bin/print_hello", "/bin", "-python", "print_hello.py"]

COPY README.md /README.md

COPY requirements.txt /requirements.txt

RUN pip install -r requirements.txt

RUN useradd -ms /bin/bash deploy2022user

USER deploy2022user

CMD ["uvicorn", "--host", "0.0.0.0", "--port", "8898", "main:app"]