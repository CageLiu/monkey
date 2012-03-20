# -*- coding:utf-8 -*-
from django import forms

from monkey.apps.admin import models as am

from django.forms.models import modelformset_factory

class Login(forms.Form):
    '''The login form'''
    usm = forms.CharField(widget = forms.TextInput(attrs = {'class':'text-input','id':'lusm'}))
    pwd = forms.CharField(widget = forms.PasswordInput(attrs = {'class':'text-input','id':'lpwd'}))

class AddGroup(forms.Form):
    class Meta:
        model = am.Group

class AddMember(forms.ModelForm):
    class Meta:
        model = am.User

class ChangeMember(forms.ModelForm):
    class Meta:
        model = am.User
        exclude = ('usm','pwd','rename','email')

class CreateProject(forms.ModelForm):
    class Meta:
        model = am.Project
        exclude = ('enname','zhnam','title','status','starttime','period')
