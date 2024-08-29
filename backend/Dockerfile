# Use a base image with Miniconda
FROM continuumio/miniconda3:24.7.1-0

# Set working directory
WORKDIR /app

# Add additional channels
RUN conda config --add channels conda-forge \
&& conda config --add channels defaults

# Copy environment.yml file and create the Conda environment
COPY conda-environment.yml .
RUN conda env create -f conda-environment.yml

# Activate the environment and set it as default
SHELL ["conda", "run", "-n", "ParquetReader", "/bin/bash", "-c"]
RUN conda init bash
ENV PATH /opt/conda/envs/ParquetReader/bin:$PATH

# Copy your application code
COPY . .

EXPOSE 5000

# Run main python script
CMD ["flask", "--app", "main.py", "run", "--host=0.0.0.0"]