FROM python:latest
LABEL org.opencontainers.image.source https://github.com/WeatherXM/cod-demo
RUN pip3 install matplotlib matplotlib pandas scipy
WORKDIR /app
COPY src/QoF.py /app
CMD python QoF.py
