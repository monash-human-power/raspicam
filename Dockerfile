FROM python:3.7

ENV MQTT_BROKER_IP=host.docker.internal
ENV QT_X11_NO_MITSHM=1

RUN useradd -ms /bin/bash cam
RUN apt-get update \
    && apt-get install -y libpango-1.0-0 libatk1.0-0 libcairo-gobject2 libpangocairo-1.0-0 libqt4-test libtiff5 libqtcore4 libwebp6 \
        libavcodec58 libavutil56 libqtgui4 libavformat58 libgdk-pixbuf2.0-0 libgtk-3-0 libilmbase23 libcairo2 libswscale5 libopenexr23

COPY requirements.txt /tmp/requirements.txt
COPY optional-requirements.txt /tmp/optional-requirements.txt
RUN pip install -r /tmp/optional-requirements.txt; \
    pip install -r /tmp/requirements.txt --extra-index-url https://www.piwheels.org/simple

COPY . /cam
WORKDIR /cam/CameraOverlay

ENTRYPOINT [ "/cam/entrypoint.sh" ]
CMD [ "overlay_all_stats.py" ]
