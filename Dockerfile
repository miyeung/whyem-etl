FROM python:3.7-slim-buster

COPY install-packages.sh .
RUN ./install-packages.sh

COPY dist/*.whl /tmp/
WORKDIR /tmp
RUN pip install *.whl
RUN rm -f *.whl

RUN useradd --create-home whyemetl
WORKDIR /home/whyemetl

COPY run.py .
RUN chmod 775 run.py
RUN chown whyemetl:whyemetl run.py
USER whyemetl

HEALTHCHECK CMD curl --fail http://localhost:5000/ || exit 1

CMD [ "python", "run.py" ]
