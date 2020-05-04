FROM python:3.7
COPY requirements.txt ./

RUN pip install --upgrade pip && \
    pip install -r requirements.txt

WORKDIR /host

#COPY model_api.py ./
#COPY averaged-ende-export500k-v2.tar.gz ./

#COPY ende_client.py ./

#RUN tar xf averaged-ende-export500k-v2.tar.gz

