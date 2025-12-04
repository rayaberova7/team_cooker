FROM inseefrlab/onyxia-python-pytorch:py3.13.8

ENV TIMEOUT=3600

ENV PROJ_LIB=/opt/conda/share/proj

# set api as the current work dir
WORKDIR /api

# copy the requirements list
COPY requirements.txt requirements.txt

# copy the main code of fastapi
COPY ./src /api

# launch the unicorn server to run the api
# If you are running your container behind a TLS Termination Proxy (load balancer) like Nginx or Traefik,
# add the option --proxy-headers, this will tell Uvicorn to trust the headers sent by that proxy telling it
# that the application is running behind HTTPS, etc.
CMD ["uvicorn", "src.app:app", "--host", "0.0.0.0", "--port", "8000"]
