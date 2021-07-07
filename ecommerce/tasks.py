from celery import shared_task
from time import sleep
from django.core.mail import send_mail
from django.conf import settings


@shared_task(name="test")
def  return_somthing():
    subject = 'Thank you for registering to our site ooo my god'
    message = 'this a test of sending an email from a celery task'
    email_from = settings.EMAIL_HOST_USER
    recipient_list = ['kakigi6017@herrain.com']    
    send_mail( subject, message, email_from, recipient_list)
    

    
    return  None
    
  

@shared_task(name='send_test_email')
def send_email_task():
    subject = 'Thank you for registering to our site mannnnnnnnnnnnnnnnnnnn'
    message = 'this a test of sending an email from a celery task okeys'
    email_from = settings.EMAIL_HOST_USER
    recipient_list = ['kakigi6017@herrain.com']    
    send_mail( subject, message, email_from, recipient_list)
    return 1+2

