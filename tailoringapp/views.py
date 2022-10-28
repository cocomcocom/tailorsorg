from django.shortcuts import render

from django.views import View

from django.http import HttpResponse, HttpResponseRedirect

import django.core.exceptions

from django.contrib import auth

import sqlite3 as sql

import os, datetime

from django.contrib.auth import decorators

from . import models

from . import forms, bruteprotect

# Create your views here.


class NullHandler:
    

    def __init__(self):

        self.Url = "/static/sample/Null.PNG"
        


class Homepage(View):

    def get(self, request, *args, **kwargs):

        template = "main/home.html"

        self.ctx = dict()
        self.ctx["stylesheet"] = "/static/files/style.css"
        self.ctx["logomage"] = "/static/files/machine.png"

        try:
            
            data = models.HomeDetails.objects.get(pk=1)

            self.ctx["mailinfo"] = data.Email

            self.ctx["address"] = data.Address

        except models.HomeDetails.DoesNotExist:
            pass


        return HttpResponse(render(request, template, self.ctx))

class Design(View):

    def __init__(self):

        self.ctx = dict()

        self.ctx["stylesheet"] = "/static/files/dstyle.css"
        self.ctx["logomage"] = "/static/files/machine.png"

        samples = list(models.DressSample.objects.all())

        if len(samples) % 2 != 0:

            samples.append(NullHandler())


        dimensions = dimensionhandler(len(samples))

        for val in range(len(samples)):

            samples[val].dimension = dimensions[val]

        self.ctx["samples"] = samples

        self.ctx["counter"] = 0

        form = forms.Enqueueform()

        self.ctx["formdata"] = form


    def get(self, request, *args, **kwargs):

        template = "design/design.html"

        return HttpResponse(render(request, template, self.ctx))
    

    def post(self, request, *args, **kwargs):

        form = forms.Enqueueform(request.POST)

        if form.is_valid():

            queue = models.Queue(Username=request.POST["Name"], Email=request.POST["Email"],
                                 Userpreferrence=request.POST["Dressid"])

            queue.Username = str(queue.Username)

            queue.Email = str(queue.Email)

            queue.Priority = datetime.date.today()

            queue.Userpreferrence = queue.Userpreferrence.split(',')

            try:

                queue.full_clean()

                testcount = models.Queue.objects.count()

                if testcount < 100:
                    
                    if queue.Userpreferrence is None:
                        
                        queue.Userprefference = 0

                    testexists = models.Queue.objects.filter(Username=queue.Username, Email = queue.Email)

                    if not testexists:
                        
                        models.Queue.objects.create(Username=queue.Username, Email=queue.Email,
                                                    Userpreferrence=queue.Userpreferrence, Priority=queue.Priority)
                    else:

                        models.Queue.objects.filter(Username=queue.Username, Email=queue.Email).update(
                            Username=queue.Username, Email=queue.Email, Userpreferrence=queue.Userpreferrence,
                            Priority=queue.Priority)

                    return HttpResponseRedirect("/successredirect/allocate")
                
                return HttpResponseRedirect("/successredirect")

            except django.core.exceptions.ValidationError as ex:

                empdata = dict()

                empdata["Email"] = request.POST["Email"]

                empdata["Name"] = request.POST["Name"]

                empdata["Dressid"] = request.POST["Dressid"]

                keys = ex.message_dict.keys()

                if 'Email' in keys:
                    empdata["Email"] = None

                if 'Name' in keys:
                    empdata["Name"] = None

                if 'Dressid' in keys:
                    empdata["Dressid"] = None

                form = forms.Enqueueform(empdata)

                self.ctx["formdata"] = form

                self.ctx["invalid"] = True

                template = "design/design.html"

                return HttpResponse(render(request, template, self.ctx))
                    

                    
        
        template = "design/design.html"

        self.ctx["formdata"] = form

        self.ctx["invalid"] = True

        return HttpResponse(render(request, template, self.ctx))

        

class Service(View):

    def get(self, request, *args, **kwargs):

        queued = models.Queue.objects.all()

        pending = models.Pending.objects.all()

        served = models.Served.objects.all()

        self.ctx = dict()

        self.ctx["queuedata"] = queued

        self.ctx["pendingdata"] = pending

        self.ctx["serveddata"] = served
        
        self.ctx["stylesheet"] = "/static/files/sstyle.css"

        template = "service/service.html"

        return HttpResponse(render(request, template, self.ctx))

    

def success(request, val=''):

    if val == 'allocate':
        
        ctx = dict()

        queued = models.Queue.objects.all()

        pending = models.Pending.objects.all()

        served = models.Served.objects.all()

        ctx["queuedata"] = queued

        ctx["pendingdata"] = pending

        ctx["serveddata"] = served

        ctx["stylesheet"] = "/static/files/sstyle.css"

        ctx["alert"] = "msg()"

        ctx["msg"] = "Check the Queue list, after then contact us for service discussion."

        ctx["ID"] = models.Queue.objects.last()

        template = "service/service.html"

        return HttpResponse(render(request, template, ctx))

    return HttpResponseRedirect("/occupied")


def no_space(request):

    
    ctx = dict()

    form = forms.Enqueueform()

    ctx["formdata"] = form

    ctx["stylesheet"] = "/static/files/dstyle.css"

    ctx["alert"] = "msg()"

    ctx["msg"] = "Queue is full, enqueue after a day"

    template = "design/design.html"

    return HttpResponse(render(request, template, ctx))



def dimensionhandler(allsamples):

    defaultleft = 0
    
    defaulttop = 0

    dimensionskeeper = []

    start = "locked"

    for sides in range(allsamples):

        dimensionskeeper += [[defaulttop, defaultleft]]

        if start:

            defaultleft += 330

            start = None

            continue

        if not start:
            
            defaulttop += 210

            defaultleft = 0

            start = "locked"

    return dimensionskeeper


class Manager(View):

    def get(self, request, *args, **kwargs):

        if request.user.is_authenticated:

            self.template = "manage/manager.html"

            self.ctx = dict()

            self.queued = models.Queue.objects.all()

            self.pending = models.Pending.objects.all()

            self.served = models.Served.objects.all()

            self.ctx["queuedata"] = self.queued

            self.ctx["pendingdata"] = self.pending

            self.ctx["serveddata"] = self.served

            self.ctx["stylesheet"] = "/static/files/manager.css"

            self.mContent = """<button onclick = "logout()" style="position: absolute;width: 100px;
            height: 40px;background-color: red;color: white;font-size: 20px;
            border-radius: 10px;top: 10px;">Logout</button>
            <button onclick="autodequeue()" style="position: absolute;width: 200px;font-size: 20px;
            background-color: red;color: white;left: 40em;border-radius: 10px;top: 3px;">
	    Dequeue Non-responded
	    </button> """

            self.ctx["mContent"] = self.mContent

            return HttpResponse(render(request, self.template, self.ctx))

        return HttpResponseRedirect("/login")

def Login(request):
    
    #request method is get
    
    if request.method == "GET":

        form = forms.Loginform()

        ctx = dict()

        ctx['form'] = form

        template = 'login/login.html'

        return HttpResponse(render(request, template, ctx))

    #if request method is not get, hence it is post

    user = auth.authenticate( username = request.POST['Username'], password = request.POST['Password'] )

    tested = None

    if user:

        #bruteforce protection test

        status = bruteprotect.initialize()

        tested = True

        if not status:

            auth.login(request, user)

            return HttpResponseRedirect("/manage")


    #bruteforce protection test

    ctx = dict()

    if tested:

        ctx['bruteprotect'] = tested

    else:

        ctx['bruteprotect'] = bruteprotect.initialize()

    template = "login/login.html"

    ctx['unauth'] = True

    form = forms.Loginform(request.POST)

    ctx['form'] = form

    return HttpResponse(render(request, template, ctx))


def Logout(request):

    auth.logout(request)

    return HttpResponseRedirect("/login")


@decorators.login_required(redirect_field_name="/manage", login_url="/login")

def Addpending(request):

    data = models.Queue.objects.first()

    ctx = dict()

    ctx['alert'] = "noqueued()"

    if data:

        models.Pending.objects.create( Username = data.Username, Email = data.Email,
                                       Userpreferrence = data.Userpreferrence, Priority = data.Priority)

        data.delete()

        del ctx['alert']
        

    template = "manage/manager.html"


    queued = models.Queue.objects.all()

    pending = models.Pending.objects.all()

    served = models.Served.objects.all()

    ctx["queuedata"] = queued

    ctx["pendingdata"] = pending

    ctx["serveddata"] = served

    ctx["stylesheet"] = "/static/files/manager.css"

    mContent = """<button onclick = "logout()" style="position: absolute;width: 100px;
            height: 40px;background-color: red;color: white;font-size: 20px;
            border-radius: 10px;top: 10px;">Logout</button>
            <button onclick="autodequeue()" style="position: absolute;width: 200px;font-size: 20px;
            background-color: red;color: white;left: 40em;border-radius: 10px;top: 3px;">
	    Dequeue Non-responded
	    </button> """

    ctx["mContent"] = mContent

    return HttpResponse(render(request, template, ctx))


@decorators.login_required(redirect_field_name="/manage", login_url="/login")

def Addserved(request):

    data = models.Pending.objects.first()

    ctx = dict()

    ctx['alert'] = "nopending()"

    if data:

        models.Served.objects.create( Username = data.Username, Email = data.Email )

        data.delete()

        del ctx['alert']

    template = "manage/manager.html"

    queued = models.Queue.objects.all()

    pending = models.Pending.objects.all()

    served = models.Served.objects.all()

    ctx["queuedata"] = queued

    ctx["pendingdata"] = pending

    ctx["serveddata"] = served

    ctx["stylesheet"] = "/static/files/manager.css"

    mContent = """<button onclick = "logout()" style="position: absolute;width: 100px;
            height: 40px;background-color: red;color: white;font-size: 20px;
            border-radius: 10px;top: 10px;">Logout</button>
            <button onclick="autodequeue()" style="position: absolute;width: 200px;font-size: 20px;
            background-color: red;color: white;left: 40em;border-radius: 10px;top: 3px;">
	    Dequeue Non-responded
	    </button> """

    ctx["mContent"] = mContent

    return HttpResponse(render(request, template, ctx))

@decorators.login_required(redirect_field_name="/manage", login_url="/login")

def Removeserved(request):

    data = models.Served.objects.last()

    ctx = dict()

    ctx['alert'] = "noserved()"

    if data:
        
        data.delete()

        del ctx['alert']

    template = "manage/manager.html"

    ctx = dict()

    queued = models.Queue.objects.all()

    pending = models.Pending.objects.all()

    served = models.Served.objects.all()

    ctx["queuedata"] = queued

    ctx["pendingdata"] = pending

    ctx["serveddata"] = served

    ctx["stylesheet"] = "/static/files/manager.css"

    mContent = """<button onclick = "logout()" style="position: absolute;width: 100px;
            height: 40px;background-color: red;color: white;font-size: 20px;
            border-radius: 10px;top: 10px;">Logout</button>
            <button onclick="autodequeue()" style="position: absolute;width: 200px;font-size: 20px;
            background-color: red;color: white;left: 40em;border-radius: 10px;top: 3px;">
	    Dequeue Non-responded
	    </button> """

    ctx["mContent"] = mContent

    return HttpResponse(render(request, template, ctx))



@decorators.login_required(redirect_field_name="/manage", login_url="/login")

def Dequeue(request):

    queue = models.Queue.objects.all()

    ctx = dict()

    ctx['alert'] = "noqueued()"

    if queue:

        status = None

        date = datetime.date.today()

        for person in queue:

            if (person.Priority - date).days >= 2:

                person.delete()

                status = True

        if status:

            ctx['alert'] = "dequeueinfo()"

        else:

            ctx['alert'] = "nodequeued()"
        

    template = "manage/manager.html"

    queued = models.Queue.objects.all()

    pending = models.Pending.objects.all()

    served = models.Served.objects.all()

    ctx["queuedata"] = queued

    ctx["pendingdata"] = pending

    ctx["serveddata"] = served

    ctx["stylesheet"] = "/static/files/manager.css"

    mContent = """<button onclick = "logout()" style="position: absolute;width: 100px;
            height: 40px;background-color: red;color: white;font-size: 20px;
            border-radius: 10px;top: 10px;">Logout</button>
            <button onclick="autodequeue()" style="position: absolute;width: 200px;font-size: 20px;
            background-color: red;color: white;left: 40em;border-radius: 10px;top: 3px;">
	    Dequeue Non-responded
	    </button> """

    ctx["mContent"] = mContent

    return HttpResponse(render(request, template, ctx))

