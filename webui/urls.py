from django.conf.urls import patterns, url

from webui import views

urlpatterns = patterns('',
    url(r'^$', views.index, name='index'),
    url(r'^json/versions/$', views.versions, name="versions"),
    url(r'^json/versions/newest$', views.versionsnewest, name="versionsnewest"),
    url(r'^json/versions/(?P<ver1>\d+)/(?P<ver2>\d+)/$', views.versiondiff, name="versiondiff"),
    url(r'^json/fetchraw/(?P<gpid>\d+)/(?P<version>\d+)/$', views.fetchraw, name="fetchrawjson"),
    url(r'^json/fetchgp/(?P<gpid>\d+)/(?P<version>\d+)/$', views.fetchgenomeproject, name="fetchgenomeprojectjson"),
    url(r'^json/fetchgp/(?P<gpid>\d+)/$', views.fetchgenomeprojects, name="fetchgenomeprojectsjson"),
    url(r'^json/fetchgps/(?P<version>\d+)/$', views.fetchallgenomeprojects, name="fetchallgenomeprojectsjson"),
    url(r'^json/getfiles/(?P<gpid>\d+)/(?P<version>\d+)/$', views.getfiles, name="getfilesjson"),

)
