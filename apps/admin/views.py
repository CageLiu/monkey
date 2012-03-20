# -*- coding:utf-8 -*-

from djangomako.shortcuts import render_to_response
from django.http import HttpResponseRedirect
from md5 import md5
import datetime
from django.db.models import Q
from monkey.apps.admin import models as am

import os
from monkey.sets import Global

from django.utils.encoding import smart_unicode
from django.utils.encoding import smart_str

from django.core.mail import EmailMessage
from django.template import loader

from settings import EMAIL_HOST_USER 


def login(request):
    if request.session.get('username'):
        return HttpResponseRedirect("/index/")
    else:
        if 'username' in request.POST and 'password' in request.POST:
            username = request.POST['username']
            password = request.POST['password']
            if len(username) == 0 :
                utips = u'用户名不能为空'
            elif len(password) == 0:
                utips = u'密码不能为空'
            else:
                try:
                    rightpwd = am.User.objects.get(usm = username).pwd
                except am.User.DoesNotExist:
                    utips = u'用户不存在'
                else:
                    if rightpwd == password:
                        request.session['username'] = username
                        request.session.set_expiry(0)
                        return HttpResponseRedirect('')
                    else:
                        utips = u'密码错误'
    return render_to_response("www/admin/login.html",locals())

def logout(request):
    del request.session['username']
    return HttpResponseRedirect('/login/')

def index(request,category):
    if request.session.get('username'):
        project = am.Project.objects.all().order_by('-starttime')
        member = am.User.objects.all()
    else:
        return HttpResponseRedirect('/login/')
    return render_to_response("www/admin/index.html",locals())

def user(request,uid=''):
    if request.session.get('username'):
        mem = am.User.objects.get(id = uid)
        project = mem.usership_set.all()
    else:
        return HttpResponseRedirect('/login/')
    return render_to_response("www/admin/user.html",locals())

def project(request,pid=''):
    if request.session.get('username'):
        project = am.Project.objects.get(id = pid)
        htmldir = Global.project_dir + project.enname
        cssdir = Global.static_dir + project.enname + '/css'
        jsdir = Global.static_dir + project.enname + '/js'
        imgdir = Global.static_dir + project.enname + '/img'
        htmlfiles = [i for i in findfile(htmldir) if not (i.startswith('_') or '.swp' in i)]
        modpage = [i for i in findfile(htmldir) if i.startswith('_')]

    else:
        return HttpResponseRedirect('/login/')
    return render_to_response('www/admin/project.html',locals())

def useradmin(request):
    if request.session.get('username'):
        if am.User.objects.get(usm = request.session['username']).group.id > 1:
            return HttpResponseRedirect("/error/?path=/index/")
        member = am.User.objects.all().order_by('group')
    else:
        return HttpResponseRedirect('/login/')
    return render_to_response('www/admin/useradmin.html',locals())

def adduser(request,uid=""):
    if request.session.get('username'):
        user = am.User.objects.get(usm = request.session['username'])
        if user.group.id > 1:
            return HttpResponseRedirect('/error/?path=/index/')
        else:
            if uid:
                user = am.User.objects.get(id = uid)
                if request.method == 'POST':
                    am.User.objects.filter(id = uid).update(\
                    rename = request.POST['rename'],email = request.POST['email'],group = request.POST['group'])
                    return HttpResponseRedirect('/user/')
            else:
                if request.method == 'POST':
                    am.User(usm = request.POST['usm'],pwd = request.POST['pwd'],\
                    rename = request.POST['rename'],email = request.POST['email'],group = am.Group.objects.get(id = int(request.POST['group']))).save()
                    return HttpResponseRedirect('/user/')
    else:
        return HttpResponseRedirect('/login/')
    return render_to_response('www/admin/adduser.html',locals())

def addproject(request,pid=''):
    if request.session.get('username'):
        user = am.User.objects.get(usm = request.session['username'])
        alluser = am.User.objects.all()
        if pid:
            p = am.Project.objects.get(id = pid)
            if request.method == 'POST':
                path = {'project_path' : Global.project_dir + request.POST['enname'],\
                        'css_path' : Global.static_dir + request.POST['enname'] + '/css',\
                        'js_path' : Global.static_dir + request.POST['enname'] + '/js',\
                        'img_path' : Global.static_dir + request.POST['enname'] + '/img'
                        }
                item = am.Project.objects.filter(id = pid).update(zhname = request.POST['zhname'],\
                title = request.POST['title'],status = request.POST['status'],starttime = request.POST['starttime'],\
                period = request.POST['period'],manager = am.User.objects.get(id = int(request.POST['manager'])))
                #clear the usership
                p.member.clear()
                #get the newest member list
                l = [am.User.objects.get(id = int(i)) for i in request.POST.getlist('member')]
                #update usership
                for i in l:
                    am.Usership.objects.create(user = i,project = p)
                touchfile(path['project_path'] + '/_header.html',Global._mod_header_html)
                #_footer.html
                touchfile(path['project_path'] + '/_footer.html',Global._mod_footer_html)
                #_merge.html
                touchfile(path['project_path'] + '/_merge.html',Global._mod_merge_html)
                for u in l:
                    if u.group.access == 2:
                        for k,v in path.items():
                            if k == 'project_path':
                                touchfile(v + '/_' + u.usm + '.html',Global._mod_user_html)
                            elif k == 'css_path':
                                touchfile(v + '/_' + u.usm + '.css','/*' + u.usm + ' css file*/')
                            elif k == 'js_path':
                                touchfile(v + '/_' + u.usm + '.js','/*' + u.usm + ' js file*/')
                            else:
                                break
                p = am.Project.objects.get(id = pid)
                subject = u'Monkey Admin通知 ｜ ' + p.zhname + u"变更"
                htmlfiles = [i.split('.')[0] for i in findfile(Global.project_dir + p.enname) if not (i.startswith('_') or '.swp' in i)]
                html_content = loader.render_to_string('www/admin/mail.html',locals())
                send_mail(subject,html_content,[i.email for i in p.member.all()])
                return HttpResponseRedirect('/project/')
        else:
            if request.method == "POST":
                path = {'project_path' : Global.project_dir + request.POST['enname'],\
                        'css_path' : Global.static_dir + request.POST['enname'] + '/css',\
                        'js_path' : Global.static_dir + request.POST['enname'] + '/js',\
                        'img_path' : Global.static_dir + request.POST['enname'] + '/img'
                        }
                item = am.Project.objects.create(enname = request.POST['enname'],zhname = request.POST['zhname'],\
                title = request.POST['title'],status = am.Status.objects.get(id = int(request.POST['status'])),starttime = request.POST['starttime'],\
                period = request.POST['period'],manager = am.User.objects.get(id = int(request.POST['manager'])))
                l = [am.User.objects.get(id = int(i)) for i in request.POST.getlist('member')]
                for i in l:
                    am.Usership.objects.create(user = i,project = item)
                #create the floder in system
                for v in path.values():
                    if not os.path.exists(v):
                        os.makedirs(v)
                #create the file
                #_header.html
                touchfile(path['project_path'] + '/_header.html',Global._mod_header_html)
                #_footer.html
                touchfile(path['project_path'] + '/_footer.html',Global._mod_footer_html)
                touchfile(path['project_path'] + '/_merge.html',Global._mod_merge_html)
                for u in l:
                    if u.group.access == 2:
                        for k,v in path.items():
                            if k == 'project_path':
                                touchfile(v + '/_' + u.usm + '.html',Global._mod_user_html)
                            elif k == 'css_path':
                                touchfile(v + '/_' + u.usm + '.css','/*' + u.usm + ' css file*/')
                            elif k == 'js_path':
                                touchfile(v + '/_' + u.usm + '.js','/*' + u.usm + ' js file*/')
                            else:
                                break
                p = item;
                subject = u'Monkey Admin通知 ｜ ' + p.zhname + u"变更"
                html_content = loader.render_to_string('www/admin/mail.html',locals())
                send_mail(subject,html_content,[i.email for i in p.member.all()])
                return HttpResponseRedirect('/project/')
    else:
        return HttpResponseRedirect('/login/')
    return render_to_response('www/admin/addproject.html',locals())

def delete(request,did='',dtype=''):
    if request.session.get('username'):
        if am.User.objects.get(usm = request.session.get('username')).group.access != 1:
            return HttpResponseRedirect('/error/?path=/index/')
        if did:
            if dtype == 'user':
                am.User.objects.get(id = did).delete()
            elif dtype == 'project':
                if am.Project.objects.get(id = did).enname != 'base':
                    am.Project.objects.get(id = did).delete()
    else:
        return HttpResponseRedirect('/login/')
    return HttpResponseRedirect('/' + dtype + '/')

def group(request,gid):
    if request.session.get('username'):
        if am.User.objects.get(usm = request.session.get('username')).group.access != 1:
            return HttpResponseRedirect('/error/?path=/index/')
        if gid:
            return render_to_response('www/admin/addgroup.html',locals())
    else:
        return HttpResponseRedirect('/login/')
    return render_to_response('www/admin/group.html',locals())

def error(request):
    if 'path' in request.GET:
        path = request.GET['path']
    else:
        path = '/index/'
    return render_to_response('www/admin/error.html',locals())


def view(request,p='',tpl=''):
    template = 'www/' + p + '/' + tpl + '.html'
    dever = [i for i in am.User.objects.all() if i.group.id == 2]
    tlist = {i.usm:'www/base/_' + i.usm + '.html' for i in dever}
    csslist = ['/static/base/' + 'css/_' + i.usm + '.css' for i in dever ]
    jslist = ['/static/base/' + 'js/_' + i.usm + '.js' for i in dever ]
    mem = [i for i in am.Project.objects.get(enname = p).member.all() if i.group.id == 2]
    mlist = {f.usm:'www/' + p + '/_' + f.usm + '.html' for f in mem}
    if p != 'base':
        basehtml = getpage(True,**tlist)
        #mlist = ['www/' + p + '/_' + f.usm + '.html' for f in mem]
        csslist.extend(['/static/' + p + '/css/_' + i.usm + '.css' for i in mem])
        jslist.extend(['/static/' + p + '/js/_' + i.usm + '.js' for i in mem])
    else:
        basehtml = ''
        #mem = [i for i in am.User.objects.all() if i.group.id == 2]
    modhtml = getpage(True,**mlist)
    cssfiles = static('css',*csslist)
    jsfiles = static('js',*jslist)
    return render_to_response(template,locals())



#-------------------------------------------

def touchfile(thefile,cont):
    if os.path.isfile(thefile):
        return
    cont = cont or ''
    #cont = unicode(cont.decode().encode('utf-8'),'utf-8')
    f = open(thefile,'w')
    f.write(cont)
    f.close()

def getpage(cleaned=True,**filename):
    html = []
    start_str = '''<%include file='_header.html' />'''
    end_str = '''<%include file='_footer.html' />'''
    for k,v in filename.items():
        try:
            f = open(v)
            text = unicode(f.read(),'utf-8')
            if cleaned:
                text = text[text.find(start_str) + len(start_str) : text.find(end_str)]
                text = text.split()
                idstr = ''' id="''' + k +'''"'''
                text[0] += idstr
                html.append(' '.join(text))
            else:
                html.append(f.read())
        except IOError:
            pass
        else:
            f.close()
    html = ''.join(html)
    return html

def static(ftype,*filename):
    if ftype == 'css':
        return ''.join(['''<link type="text/css" rel="stylesheet" href="''' + i +'''"/>''' for i in filename])
    elif ftype == 'js':
        return ''.join(['''<script type="text/javascript" src="''' + i +'''"></script>''' for i in filename])

def findfile(path):
    l = []
    for root,dirs,f in os.walk(path):
        for files in f:
            l.append(files)
    return l
def send_mail(subject,html_content,recipient_list):
    msg = EmailMessage(subject,html_content,EMAIL_HOST_USER,recipient_list)
    msg.content_subtype = 'html'
    msg.send()
