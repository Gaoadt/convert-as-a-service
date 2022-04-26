# STAGE 1
# Goal: download model
FROM cirrusci/wget as BUILD-ENV

# Downloading model
COPY setup.sh ./
RUN  ["sh", "setup.sh"]

# STAGE 2
# Goal: deployment container
FROM tensorflow/tensorflow as DEPLOY
WORKDIR /home/app
COPY --from=BUILD-ENV data ./data
COPY * ./
COPY requirements.docker.txt requirements.txt
COPY /src ./src
RUN ["pip","install","-r","requirements.txt"]
CMD ["python3", "main.py"]
EXPOSE 5000


