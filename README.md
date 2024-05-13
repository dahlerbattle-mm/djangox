> A batteries-included Django starter project. To learn more visit [LearnDjango.com](https://learndjango.com).


### Getting Started with Docker

Use the following commands to build the Docker image, run the container, and execute the standard commands within Docker.

```
$ sudo docker-compose up -d --build
$ sudo docker-compose exec web python manage.py migrate
$ sudo docker-compose exec web python manage.py createsuperuser
# Load the site at http://127.0.0.1:8000
```

## Starting up with ngrok
Use the following commands to start the ngrok site, which allows the user to see MM website on a publically facing http address. 

```
docker run --net=host -it -e NGROK_AUTHTOKEN=2bsabaYSp28A1B1Q5cwASLC5W0H_5RDUBPMRnKgCMMSrmNrWZ ngrok/ngrok:latest http --domain=officially-fast-condor.ngrok-free.app 8000
```

## Running docker container commands
Make sure to run everything within the docker container when making updates, etc. 

```
sudo docker-compose exec web ..... 

Oftentimes this will look like: 
sudo docker-compose exec web python manage.py check 
... or other django related commands
```

## 🚀 Features

- Django 5.0 & Python 3.12
- Install via [Pip](https://pypi.org/project/pip/) or [Docker](https://www.docker.com/)
- User log in/out, sign up, password reset via [django-allauth](https://github.com/pennersr/django-allauth)
- Static files configured with [Whitenoise](http://whitenoise.evans.io/en/stable/index.html)
- Styling with [Bootstrap v5](https://getbootstrap.com/)
- Debugging with [django-debug-toolbar](https://github.com/jazzband/django-debug-toolbar)
- DRY forms with [django-crispy-forms](https://github.com/django-crispy-forms/django-crispy-forms)
- Custom 404, 500, and 403 error pages
----

----

## Next Steps
- Add [gunicorn](https://pypi.org/project/gunicorn/) as the production web server.
- Update the [EMAIL_BACKEND](https://docs.djangoproject.com/en/4.0/topics/email/#module-django.core.mail) and connect with a mail provider.
- Make the [admin more secure](https://opensource.com/article/18/1/10-tips-making-django-admin-more-secure).
- `django-allauth` supports [social authentication](https://django-allauth.readthedocs.io/en/latest/providers.html) if you need that.


