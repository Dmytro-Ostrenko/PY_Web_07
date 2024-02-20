# Використання базового образу PostgreSQL
FROM postgres:latest

# Задання користувача та пароля для бази даних
ENV POSTGRES_USER=Dmytro
ENV POSTGRES_PASSWORD=1234
ENV POSTGRES_DB=database_HW7.db