

# Make virtual environment 

## On windows
Virtualenv
py -m venv env
.\venv\Scripts\activate

## On Linux
virtualenv venv
venv\bin\activate

## Install requirements
pip install -r requirements.txt


----------------------------
# Flask config to local environment

## On Windows 
$env:FLASK_APP ="models.py"
$env:FLASK_ENV="development"
$env:DEBUG=1

## On Linux
export FLASK_APP ="models.py"
export FLASK_ENV="development"
export DEBUG=1