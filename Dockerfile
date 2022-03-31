FROM python:3.9

WORKDIR /app

COPY . .

# dependencies
RUN python3 -m pip install --upgrade pip \
	&& python3 -m pip install poetry \
    && poetry config virtualenvs.create false \
    && poetry install

CMD ["uvicorn", "app:app", "--host", "0.0.0.0", "--port", "80"]