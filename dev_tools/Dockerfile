FROM python:3.11-slim-buster

WORKDIR /app

# Скопируйте файлы зависимостей
COPY pyproject.toml poetry.lock /app/

# Установите зависимости
RUN pip install poetry
RUN poetry config virtualenvs.create false
RUN poetry install --no-dev

# Скопируйте проект в рабочую директорию
COPY . /app/

# Установка netcat
RUN apt-get update && apt-get install -y netcat-openbsd

# Копирование скрипта в контейнер
COPY ./scripts/automigrate.sh /automigrate.sh
RUN chmod +x /automigrate.sh

ENTRYPOINT ["/automigrate.sh"]
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]   
