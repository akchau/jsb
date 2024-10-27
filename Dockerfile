FROM python:3.10
WORKDIR /app
ARG SSH_PRIVATE_KEY
RUN mkdir -p /root/.ssh \
    touch /root/.ssh/known_hosts && \
    && chmod 0700 /root/.ssh \
    && echo "$SSH_PRIVATE_KEY" > /root/.ssh/id_rsa \
    && chmod 600 /root/.ssh/id_rsa \
    && ssh-keyscan github.com >> /root/.ssh/known_hosts
COPY ./requirements.txt /app
RUN pip install -r requirements.txt
RUN pip uninstall watchfiles -y
COPY  . /app
CMD ["python", "main.py", "go"]