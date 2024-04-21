#!/bin/sh
# automigrate.sh

# Ожидание доступности базы данных
while ! nc -z $DATABASE_HOST 5432; do
  sleep 1
done

echo "Database is up - executing command"

# Выполнение миграций
echo "Applying database migrations..."
python manage.py migrate --noinput

# Запуск команды, переданной в CMD
exec "$@"