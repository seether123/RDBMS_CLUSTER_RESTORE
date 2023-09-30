FROM image_name
USER root
RUN apt-get update && \
    apt-get install -y python3 python3-pip &&\
    pip3 install boto3 requests psycopg2-binary --break-broken-packages
COPY . .
CMD ["./execute.sh"]
