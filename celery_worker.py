from celery import Celery

def make_celery(app_name=__name__):
    celery = Celery(app_name, broker='redis://localhost:6379/0')
    celery.config_from_object('celeryconfig')
    return celery

celery = make_celery()