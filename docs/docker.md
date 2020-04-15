# Docker

## Docker image versions
* `nsembleai/nsvision` - latest
* `nsembleai/nsvision:jupyter` - jupyter server vision
* `nsembleai/nsvision:slim` - lite version

<b>Sample docker file for running image classifier flask app in docker</b>

Dockerfile
```
FROM nsembleai/nsvision

WORKDIR /app

ADD requirements.txt /app

RUN pip install --upgrade pip && pip install -r requirements.txt

ADD . /app

EXPOSE 5000

CMD ["python","app.py"]
```


## Docker image - jupyter version
Running nsvision docker jupyter server

usage:
```bash
docker pull nsembleai/nsvision:jupyter

docker run -it nsembleai/nsvision:jupyter -v "./notebooks:/src/notebooks" -p 8888:8888 -d
```