FROM quay.io/jupyter/base-notebook:latest

#Dependencies
RUN pip install --no-cache-dir \
    numpy \
    pandas \
    matplotlib \
    scipy \
    seaborn 

#Working directory
WORKDIR /home/jovyan/work 
