FROM python:3.11
MAINTAINER Arthur Khamidullin 'artyr-xamidullin@mail.ru'
WORKDIR /usr/apps/todo/
COPY ./ ./
EXPOSE 5000
ENV PIP_PROGRESS_BAR off
RUN pip install --no-cache-dir --disable-pip-version-check -r requirements.txt

# Создаем пользователя
RUN adduser --disabled-password --gecos '' myuser

# Становимся пользователем
USER myuser

WORKDIR /usr/apps/todo/src/

CMD python app.py


#ENV PIP_PROGRESS_BAR off
#RUN pip install --no-cache-dir --disable-pip-version-check -r requirements.txt
#WORKDIR /usr/apps/todo/src/
#CMD [ "python3", "-m" , "flask", "--app", "app", "run"]