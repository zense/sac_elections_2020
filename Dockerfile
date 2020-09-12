FROM python:3.8
ENV PYTHONUNBUFFERED 1
RUN mkdir /sac_elections_2020
WORKDIR /sac_elections_2020
COPY Pipfile.lock /sac_elections_2020/
COPY Pipfile /sac_elections_2020/
COPY requirements.txt /sac_elections_2020/
RUN pip3 install -r requirements.txt
COPY . /sac_elections_2020/
RUN chmod +x scripts/*
RUN chmod 755 sac_election.env
WORKDIR /sac_elections_2020/sac_elections
EXPOSE 8000

# hand over the server handling to nginx in production
