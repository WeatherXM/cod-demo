FROM python
RUN pip3 install matplotlib matplotlib pandas scipy
WORKDIR /app
COPY src/QoF.py /app
CMD python QoF.py
