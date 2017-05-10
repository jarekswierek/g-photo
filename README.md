# G-Photo

Web application for computer vision which applies Clarifai API for image recognition.

Built with:

- Python 3.6

- Django 1.11

- clarifai 2.0.21


# Setup

1. Clone repository

```
git clone git@github.com:jarekswierek/g-photo.git
cd g-photo
```

2. Install Docker and docker-compose

https://docs.docker.com/engine/installation/linux/ubuntu/#install-using-the-repository

```
sudo pip install docker-compose==1.11.2
```

3. Add docker to group (after that you don't have to use sudo before docker-compose commands)

```
sudo usermod -aG docker ${USER}
```

4. Get Clarifai API access keys (Client ID and Client secret)

Click here and sign in and add new project for keys --> https://developer.clarifai.com/

5. Add Clarifai API keys

Create api_keys.json file

```
{
    "api_key" : "<your_api_key>",
    "api_secret" : "<your_api_secret>"
}
```

6. Dockerize app

```
docker-compose build
docker-compose run web python3 manage.py migrate
docker-compose run web python3 manage.py createsuperuser
docker-compose up
```

# Notes

- App run on localhost:8000

- If you have conflict with postgres container on port 5432 you can:

A. use pkill for kill your local postgres process (recommended)

```
sudo pkill -u postgres
```

or

B. change postgres container port on docker-compose.yml file by adding bellow 
two lines to postgres container settings. After that you must remember to 
change also database port in settings.py file.

```
ports:
    -"5433:5432"
```

C. You can create your on postgres database, remove postgres contaier settings 
from docker-compose.yml file and change database settings in settings.py file 
to your own.


# Alternative setup (virtualenv)

As alternative you can use virtualenv. Create new ENV, install there 
requirements from requirements.txt by pip, create postgres database, 
change database settings in settings.py file for your own. After that you can 
add your clarifai keys, make migrations, create superuser and run app.
