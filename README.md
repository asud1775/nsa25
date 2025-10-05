
## Setup Instructions
```
#install python
sudo apt install python3
sudo apt install python3-pip
sudo apt install python3-venv

# create a new virtual env
python3 -m venv myenv
# activate the virtual env
source myenv/bin/activate

# ensure you are in the new virtual env and install dependencies
pip install -r requirements.txt

# run streamlit
streamlit run app.py

# run jupyter notebook
jupyter notebook --ip='*' --NotebookApp.token='' --NotebookApp.password=''

```


##  Original Repo - Just for Information Only
git clone https://github.com/fneum/streamlit-tutorial.git

# ACR Container app deployment commands

```

# build the docker image
docker build -t streamlit-modis:latest .

az acr login --name devdhan
docker tag streamlit-modis devdhan.azurecr.io/nasa/streamlit-modis
docker push devdhan.azurecr.io/nasa/streamlit-modis

az containerapp up \
  --name nasa25_modis \
  --resource-group dhan-dev-rg \
  --location eastus \
  --environment 'dhan-dev-container-apps' \
  --image devdhan.azurecr.io/nasa/streamlit-modis:latest \
  --target-port 8501 \
  --ingress external \
  --query properties.configuration.ingress.fqdn


export ACR_NAME=devdhan
export RESOURCE_GROUP=dhan-dev-rg

echo $ACR_NAME
echo $RESOURCE_GROUP
echo $IDENTITY


az acr config authentication-as-arm show --registry "$ACR_NAME"

```