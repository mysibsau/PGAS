FROM python:3.12 as builder

WORKDIR /app

RUN pip install --upgrade --no-cache-dir pip && pip install pdm
COPY pdm.lock pyproject.toml ./

RUN mkdir __pypackages__ && pdm sync --prod --no-editable

FROM python:3.12-slim

WORKDIR /app

ENV PYTHONPATH=/pkgs
COPY --from=builder /app/__pypackages__/3.12/lib /pkgs
COPY --from=builder /app/__pypackages__/3.12/bin/* /bin/

COPY ./src .

RUN python manage.py compilescss && python manage.py collectstatic --clear --no-input
CMD ["gunicorn", "-b", "0.0.0.0:80", "core.wsgi", "--reload"]
