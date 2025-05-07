# FishArt-Experience-Backend

Python must be installed

## Optional create a venv
python -m venv venv

# Activate the venv
.\venv\Scripts\activate


## install the requirements
pip install -r requirements.txt


## Run the server

uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload
