FROM python:3.6

WORKDIR /app

COPY ./requirements.txt requirements.txt
RUN pip install -r requirements.txt

COPY ./ccounter ccounter

ENV PYTHONPATH "${PYTHONPATH}:/app"
# Docker gets massively confused / breaks (docker-compose 1.19.0,
# docker-py 2.7.0) if we run pytest and store pycs.
ENV PYTHONDONTWRITEBYTECODE 1

ENTRYPOINT ["python", "ccounter/color_counter.py", "/tmp/__input-file.txt", "--output_file", "/tmp/__output-file.txt"]