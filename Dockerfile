FROM python

ENV PYTHONUNBUFFERED 1
ENV PYTHONDONTWEITEBYTECODE 1

WORKDIR /backend

COPY requirements.txt ./
RUN pip install -r requirements.txt

EXPOSE 8000

COPY . .