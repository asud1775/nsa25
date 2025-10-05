# Use an official Python base image
# FROM python:3.12-slim
FROM conda/miniconda3

# Avoid interactive prompts from apt
ENV DEBIAN_FRONTEND=noninteractive


# Create app directory
WORKDIR /app

# Copy requirements and install Python deps# Install system dependencies required for cartopy
# RUN apt-get update && apt-get install -y \
#     build-essential \
#     libgeos-dev \
#     libproj-dev
#     libproj-dev \
#     proj-data \
#     proj-bin \
#     libgeos-dev \
#     libgeos++-dev \
#     libgeos-c1v5 \
#     libgdal-dev \
#     gdal-bin \
#     libhdf5-dev \
#     libnetcdf-dev \
#     pkg-config \
#     gcc \
#     g++ \
#     gfortran \`
#     libopenblas-dev \
#     liblapack-dev \
#     libffi-dev \
#     libssl-dev \
#     && rm -rf /var/lib/apt/lists/*

COPY requirements.txt /app/requirements.txt
RUN conda install -c conda-forge cartopy
# RUN pip install --no-cache-dir -r /app/requirements.txt
RUN pip install -r /app/requirements.txt

# Copy application code
COPY . /app

# Expose Streamlit default port
EXPOSE 8501

# Run the Streamlit app
CMD ["streamlit", "run", "app.py", "--server.port=8501", "--server.address=0.0.0.0", "--server.enableCORS=false", "--server.enableXsrfProtection=false"]
