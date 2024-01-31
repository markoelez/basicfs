FROM python:3.12


RUN apt-get update

RUN apt-get install -y libsnappy-dev
RUN apt-get install -y libleveldb-dev
# RUN apt-get install -y libleveldb1v5

RUN rm -rf /var/lib/apt/lists/*

RUN pip install --upgrade pip
RUN pip install uwsgi
RUN pip install pytest
RUN pip install plyvel
RUN pip install requests


RUN python -c "import plyvel;"


# Copy the project files into the container
COPY . /tmp/