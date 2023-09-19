# использование образа python3
FROM python:3

# задаем рабочую директорию
WORKDIR /diploma_project

# копируем файл с зависимостями пректа в рабочую директорию
COPY ./requirements.txt /diploma_project/

# запускаем установку зависимостей
RUN pip install -r requirements.txt

# копируем все файлы из текущей директории в рабочую директорию
COPY . .