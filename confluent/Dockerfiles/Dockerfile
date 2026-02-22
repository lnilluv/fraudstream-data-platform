FROM jedha/confluent-image

COPY requirements.txt /dependencies/requirements.txt
RUN pip install -r /dependencies/requirements.txt
RUN pip install scikit-learn --upgrade
CMD bash