FROM python:3.8
ENV PYTHONUNBUFFERED 1
RUN pip3 install pipenv
WORKDIR /opt
ADD Pipfile /opt
ADD Pipfile.lock /opt
RUN pipenv install --deploy --system
COPY ./ /opt
