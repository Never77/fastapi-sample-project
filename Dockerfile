from python:latest 

WORKDIR /opt/netcore/

COPY . .

RUN python -m venv .venv
RUN python -m pip install -U pip wheel
RUN python -m pip install .

CMD ["netcore", "run"]

EXPOSE 8000