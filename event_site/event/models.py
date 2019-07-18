from django.db import models
from django.urls import reverse
from django.http import HttpResponseRedirect
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Submit, Row, Column
from django.views.generic.edit import CreateView
from django.urls import path
import os

from django import forms

def user_directory_path(instance, filename):
    return os.path.join('media/signature/', 'user_{0}/{1}'.format(instance.login, filename))

class Users(models.Model):
    status = models.CharField(null = False, max_length = 64, default = 'FILLER')
    login = models.CharField(null = False, max_length = 64, default = 'FILLER')
    lastname = models.CharField(null = False, blank = False, max_length = 64, default = 'FILLER')
    firstname = models.CharField(null = False, max_length = 64, default = 'FILLER')
    email = models.CharField(null = False, max_length = 64, default = 'FILLER')
    promo = models.CharField(null = False, max_length = 64, default = 'FILLER')
    phone = models.CharField(null = False, max_length = 64, default = 'FILLER')
    signature_file = models.FileField(null=False, upload_to=user_directory_path, default='FILLER')
    signature_key = models.CharField(null=False, max_length=64, default='FILLER')
    private_key = models.TextField(null=False, default='FILLER')
    def __str__(self):
        return self.login


class DocumentForm(forms.ModelForm):
    class Meta:
        model = Users
        fields = ('signature_file', )


def get_image_path(instance, filename):
    return os.path.join('logos/', str(instance.id), filename)


class Assos(models.Model):
    name = models.CharField( max_length = 64)
    president_id = models.IntegerField()
    nb_members = models.IntegerField()
    description = models.CharField(null = True, max_length= 200)
    image = models.ImageField(upload_to="media/logos", blank=True, null=True)

    def __str__(self):
        return self.name


class Event(models.Model):
    users = models.ForeignKey(Users, on_delete = models.CASCADE)
    assos = models.ForeignKey(Assos, null = True, on_delete = models.CASCADE)
    name = models.CharField( max_length=200)
    date_time = models.DateTimeField('start date | format: mm/dd/year')
    end_time = models.TimeField('end time | format: 00:00:0000', auto_now=False)
    begin_time = models.TimeField('begin time | format: 00:00:0000',  auto_now=False)
    recurrence = models.BooleanField(default = False)
    frequence = models.IntegerField()
    until = models.DateField('end date | format: mm/dd/year')
    responsible = models.CharField( max_length=64)
    responsible_phone = models.CharField( max_length = 64)
    responsible_class = models.CharField( max_length = 64)
    nb_days = models.IntegerField()
    tutor_name = models.CharField(max_length = 64)
    tutor_phone = models.CharField(max_length = 64)
    tutor_job = models.CharField( max_length = 64)
    nb_ionis_student = models.IntegerField()
    nb_members = models.IntegerField()
    nb_externs = models.IntegerField()
    description = models.CharField(max_length = 200, default = 'short description')
    civil_liability = models.BooleanField(default = False)
    place = models.CharField(max_length = 64)
    rooms = models.CharField(max_length = 200)
    material = models.CharField(max_length = 200)
    drinks = models.IntegerField()
    comment = models.CharField(max_length = 200, default = 'some text')
    status = models.CharField(max_length = 200, default = 'pending')

    def __str__(self):
        return self.name



class Assos_user(models.Model):
    user_id = models.ForeignKey(Users, on_delete = models.CASCADE, null = False)
    assos_id = models.ForeignKey(Assos, on_delete = models.CASCADE, null = False)
    status = models.CharField(max_length = 64, null = False)


class EventForm(CreateView):
    model = Event
    fields = '__all__'
    template_name = 'event/form.html'
    success_url = '/event'

    def get_form(self, form_class=None):
        form = super().get_form(form_class)
        form.helper = FormHelper()
        form.helper.layout = Layout(
            Row(
                Column('users', css_class='form-group col-md-6 mb-0'),
                Column('assos', css_class='form-group col-md-6 mb-0'),
                css_class='form-row'
            ),
            Row(
                Column('name', css_class='form-group col-md-6 mb-0'),
                Column('date_time', css_class='form-group col-md-6 mb-0'),
                css_class='form-row'
            ),
            Row(
                Column('end_time', css_class='form-group col-md-6 mb-0'),
                Column('begin_time', css_class='form-group col-md-6 mb-0'),
                css_class='form-row'
            ),
            Row(
                Column('recurrence', css_class='form-group col-md-2 mb-0'),
            ),
            Row(
                Column('frequence', css_class='form-group col-md-3 mb-0'),
                Column('until', css_class='form-group col-md-6 mb-0'),
                Column('nb_days', css_class='form-group col-md-3 mb-0'),
                css_class='form-row'
            ),
            Row(
                Column('responsible', css_class='form-group col-md-4 mb-0'),
                Column('responsible_phone', css_class='form-group col-md-4 mb-0'),
                Column('responsible_class', css_class='form-group col-md-4 mb-0'),
                css_class='form-row'
            ),
            Row(
                Column('tutor_name', css_class='form-group col-md-4 mb-0'),
                Column('tutor_phone', css_class='form-group col-md-4 mb-0'),
                Column('tutor_job', css_class='form-group col-md-4 mb-0'),
                css_class='form-row'
            ),
            Row(
                Column('nb_ionis_student', css_class='form-group col-md-4 mb-0'),
                Column('nb_members', css_class='form-group col-md-4 mb-0'),
                Column('nb_externs', css_class='form-group col-md-4 mb-0'),
                css_class='form-row'
            ),
            Row(
                Column('description', css_class='form-group col-md-12 mb-0'),
            ),
            Row(
                Column('civil_liability', css_class='form-group col-md-2 mb-0'),
            ),
            Row(
                Column('place', css_class='form-group col-md-4 mb-0'),
                Column('rooms', css_class='form-group col-md-2 mb-0'),
                Column('material', css_class='form-group col-md-6 mb-0'),
                css_class='form-row'
            ),
            Row(
                Column('drinks', css_class='form-group col-md-2 mb-0'),
                Column('comment', css_class='form-group col-md-6 mb-0'),
                Column('status', css_class='form-group col-md-4 mb-0'),
                css_class='form-row'
            ),
            Submit('submit', 'Submit')
        )
        return form

# Create your models here.
