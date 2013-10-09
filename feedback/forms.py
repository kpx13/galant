# encoding: utf-8
from django import forms
from django.forms import ModelForm
from django.conf import settings
from django.core.mail import send_mail
from django.template import Context, Template
from models import Feedback
from livesettings import config_value


def sendmail(subject, body):
    mail_subject = ''.join(subject)
    send_mail(mail_subject, body, settings.DEFAULT_FROM_EMAIL,
        [config_value('MyApp', 'EMAIL')])

class FeedbackForm(ModelForm):
    
    class Meta:
        model = Feedback
        exclude = ('request_date', )
    

    def save(self, *args, **kwargs):
        super(FeedbackForm, self).save(*args, **kwargs)
        subject=u'Поступило новое сообщение через обратную связь',
        body_templ="""
            {% for field in form %}
                {{ field.label }} - {{ field.value }}
            {% endfor %}
            """
        ctx = Context({
            'form': self
        })
        body = Template(body_templ).render(ctx)
        sendmail(subject, body)
