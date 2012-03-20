# -*- coding:utf-8 -*-

from django.conf.urls.defaults import patterns, include, url
import settings

# Uncomment the next two lines to enable the admin:
#from django.contrib import admin
#admin.autodiscover()

from monkey.apps.admin import views as av

urlpatterns = patterns('',
    (r'^login/$',av.login),
    (r'^logout/$',av.logout),
    (r'^$',av.index,{'category':'index'}),
    (r'^index/$',av.index,{'category':'index'}),
    (r'^project/$',av.index,{'category':'project'}),
    (r'^project/(?P<pid>\w+)/$',av.project),
    #(r'^useradmin/$',av.useradmin),
    (r'^user/$',av.useradmin),
    (r'^adduser/(\w*)$',av.adduser),
    (r'^group/(\w*)$',av.group),
    (r'^addproject/(\w*)$',av.addproject),
    (r'^delete/(?P<dtype>\w+)/(?P<did>\w+)/$',av.delete),
    (r'^user/(?P<uid>\w+)/$',av.user),
    (r'^error/$',av.error),
    (r'^view/(?P<p>\w*)/(?P<tpl>\w*)/$',av.view),
    #(r'^view/',include('monkey.www.urls')),
	('^static_url/(?P<path>.*)','django.views.static.serve',{'document_root': settings.STATIC_PATH}),
)
