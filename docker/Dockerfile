FROM python:3.8-alpine

WORKDIR /usr/src/reminder

# set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# install psycopg2 dependencies
RUN apk update \
    && apk add postgresql-dev gcc python3-dev musl-dev

# install dependencies
RUN pip install --upgrade pip
COPY ./requirements.txt .
RUN pip install -r requirements.txt

# copy entrypoint.sh
COPY ./docker/entrypoint.sh .
RUN sed -i 's/\r$//g' /usr/src/reminder/entrypoint.sh
RUN chmod +x /usr/src/reminder/entrypoint.sh

# copy project
COPY . .
# run entrypoint.sh
ENTRYPOINT ["/usr/src/reminder/entrypoint.sh"]