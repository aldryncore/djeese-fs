FROM aldryn/base:2.2
RUN mkdir -p /app
VOLUME /data
ADD server-requirements.txt /app/server-requirements.txt
RUN pip install -r /app/server-requirements.txt
ADD ./ /app/
RUN pip install --editable /app/
ENV ROOT_FOLDER=/data/content \
    ROOT_URL=http://media.example.com/content \
    AUTH_SERVER='' \
    MAX_BUCKET_SIZE=1073741824 \
    MAX_FILE_SIZE=209715200 \
    PORT=80
CMD start web
