FROM python:3.12

RUN apt-get install wkhtmltopdf

ENV VIRTUAL_ENV=/usr/local
WORKDIR /app

RUN pip install --upgrade --no-cache-dir pip && pip install uv

COPY ./requirements.txt .
RUN uv pip install --system --no-cache -r requirements.txt

COPY ./src .

RUN python manage.py collectstatic --clear --no-input
CMD ["gunicorn", "-b", "0.0.0.0:80", "core.wsgi", "--reload"]
