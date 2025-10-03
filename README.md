
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
