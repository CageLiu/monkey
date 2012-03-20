# -*- coding:utf-8 -*-
from django.db import models

class Group(models.Model):
    name        = models.CharField(max_length = 100,unique = True)
    access      = models.IntegerField()

    def __unicode__(self):
        return self.name

class User(models.Model):
    usm         = models.CharField(max_length = 100,unique = True)
    pwd         = models.CharField(max_length = 128)
    rename      = models.CharField(max_length = 100)
    email       = models.EmailField(unique = True)
    group       = models.ForeignKey(Group)
    
    class Meta:
        ordering = ['id']

    def __unicode__(self):
        return self.rename

class Status(models.Model):
    name = models.CharField(max_length = 100)
    local_zh = models.CharField(max_length = 100)

    def __unicode__(self):
        return self.name

class Project(models.Model):
    enname      = models.CharField(max_length = 100,unique = True)
    zhname      = models.CharField(max_length = 100,unique = True)
    title       = models.TextField(max_length = 255)
    status      = models.ForeignKey(Status)
    starttime   = models.DateTimeField()
    period      = models.IntegerField()
    member      = models.ManyToManyField(User,related_name = 'member',through="Usership")
    manager     = models.ForeignKey(User,related_name = 'manager')

    plist = []

    def __unicode__(self):
        return self.zhname

    #def save(self,*args,**kwargs):
        #super(Project,self).save()
        #for item in self.plist:
            #p,created = User.objects.get_or_create(usm = item)
            #self.usm.add(p)

class Usership(models.Model):
    user        = models.ForeignKey(User)
    project     = models.ForeignKey(Project)
