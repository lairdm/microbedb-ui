from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, get_object_or_404, render_to_response
from django.template import RequestContext
from django.conf import settings
from webui.models import *
from django.core.urlresolvers import reverse
#from .utils.formatter import *
import json
import re
import pprint
import os
import base64

def index(request):
    return render(request, 'index.html')
#    return HttpResponse("Hello, world. You're at the poll index.")

def fetchraw(request, gpid, version):
    context = {}
    
    # Check for parameters
    if request.GET.get('filetype'):
        filetype = request.GET.get('filetype')
        if not filetype in FILE_TYPES:
            return HttpResponse(status=400)
    else:
        # We require a filetype
        return HttpResponse(status=400)

    if request.GET.get('reptype'):
        reptype = request.GET.get('reptype')
        if not reptype in REP_TYPES:
            return HttpResponse(status=400)

    gp = Genomeproject.objects.get(gp_id=gpid, version_id=version)

    genome_dir = gp.gpv_directory
    
    replicons = gp.replicon_set.all()
    
    context['genomepronect'] = gp.to_struct()
    context['replicons'] = []
    
    context['status'] = "OK"
    
    for r in replicons:
        if not re.match('.*' + filetype, str(r.file_types)):
            context['status'] = 'ERROR'
            context['message'] = "File type does not exist for this genomeproject"
            del context['replicons']
            break
        
        if not reptype == r.rep_type:
            continue
        
        filename = os.path.join(genome_dir, r.file_name + '.' + filetype)
        with open(filename, "rb") as genomefile:
            fileglob = base64.urlsafe_b64encode(genomefile.read())
        context['replicons'].append(r.to_struct({'file': fileglob}))
            
    data = json.dumps(context, indent=4, sort_keys=True)
    
    return HttpResponse(data, content_type="application/json")

def fetchgenomeproject(request, gpid, version):
    context = {}
    
    try:
        gp = Genomeproject.objects.get(gp_id=gpid, version_id=version)
    except:
        return HttpResponse(status=400)
    
    context['genomeproject'] = gp.to_struct()
        
    replicons = gp.replicon_set.all()

    context['replicons'] = []
    
    for r in replicons:
        context['replicons'].append(r.to_struct())
        

    context['status'] = "OK"

    data = json.dumps(context, indent=4, sort_keys=True)
    
    return HttpResponse(data, mimetype="application/json")

def fetchgenomeprojects(request, gpid):
    context = {}
    
    try:
        gp = Genomeproject.objects.filter(gp_id=gpid)
    except Exception as e:
        return HttpResponse(status=400)

    context['status'] = "OK"
    context['genomeproject'] = []
    
    for g in gp:
        context['genomeproject'].append(g.to_struct())

    data = json.dumps(context, indent=4, sort_keys=True)
    
    return HttpResponse(data, content_type="application/json")
    
    
def fetchallgenomeprojects(request, version):
    context = {}
    
    try:
        gp = Genomeproject.objects.filter(version_id=version)
    except Exception as e:
        return HttpResponse(status=400)

    context['status'] = "OK"
    context['genomeprojects'] = []
    
    for g in gp:
        context['genomeprojects'].append(g.to_struct())

    data = json.dumps(context, indent=4, sort_keys=True)
    
    return HttpResponse(data, content_type="application/json")
    

def getfiles(request, gpid, version):
    context = {}
    
    try:
        replicons =  Genomeproject.objects.get(gp_id=gpid, version_id=version).replicon_set.all()
    except:
        return HttpResponse(status=400)
    
    context['replicons'] = []
    
    for r in replicons:
        context['replicons'].append(r.to_struct())

    context['status'] = "OK"

    data = json.dumps(context)
    
    return HttpResponse(data, mimetype="application/json")

    

def versions(request):
    context = {}
    
    versions = Version.objects.all().values_list('version_id', flat=True)
    
    context['versions'] = list(versions)
    context['status'] = "OK"
    
    data = json.dumps(context)
    
    return HttpResponse(data, mimetype="application/json")
    
def versionsnewest(request):
    
    context = {}
    
    versions = Version.objects.order_by('-version_id')[0]
    
    context['versions'] = versions.version_id   
    context['status'] = "OK"
    
    data = json.dumps(context)
    
    return HttpResponse(data, mimetype="application/json")
    