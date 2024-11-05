FROM python:3

ADD . /usr/src/app/
# set work directory
WORKDIR /usr/src/app

# set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# install dependencies
RUN pip install --upgrade pip
COPY requirements.txt /usr/src/app/requirements.txt
RUN pip install -r requirements.txt

# copy entrypoint.sh
COPY ./entrypoint.sh /usr/src/app/entrypoint.sh

# copy project

RUN chmod +x /usr/src/app/entrypoint.sh

# run entrypoint.sh
CMD ["/usr/src/app/entrypoint.sh"]