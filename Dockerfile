FROM python:3.7
RUN apt-get update -qq && apt-get install -y libopus0 ffmpeg
RUN mkdir /code
WORKDIR /code
COPY requirements.txt /code/requirements.txt
RUN pip install -r requirements.txt
COPY . /code
CMD ["python3", "-u", "run.py"]
