FROM python:3.7

# system library pre-requisites
RUN \
    apt-get update && \
    apt-get install -y \
    libgfortran5 \
    libtbb2 \
    gmodule-2.0 sudo && \
    rm -rf /var/lib/apt/lists/*

# Update Python with the required packages
RUN pip install --upgrade pip
# Install Flowty
RUN pip install flowty
# Install or_datasets
RUN pip install or_datasets
# Install networkx matplotlib
RUN pip install networkx matplotlib
# Install networkx boto3 sagemaker
RUN pip install boto3 sagemaker json

ENV PYTHONUNBUFFERED=TRUE

ENTRYPOINT ["python3"]
