from django.shortcuts import render
from django.shortcuts import HttpResponse
import json
import os
import subprocess

modelname = None
# Create your views here.
def index(request):
    return render(request, "polls/index.html")

def upload(request):
    if request.method == "POST":
        file = request.FILES['input-folder']
        if file.name.split('.')[-1] == "onnx":
            global modelname
            modelname = file.name
            #print(modelname)
        root_path = os.path.join("project")
        path = os.path.join(root_path, file.name)
        if not os.path.exists(root_path):
            os.mkdir(root_path)
        with open(path, 'wb+') as f:
            for chunk in file.chunks():
                f.write(chunk)
        return HttpResponse(json.dumps({'status': 'Success', 'file': file.name}))

def build(request):
    if request.method == "POST":
        print("-------------starting service-------------")
        f = os.popen("pwd")
        root_path = f.read().strip('\n') + '/project'
        #print(root_path)
        os.chdir(root_path)
        global modelname
        if modelname == None:
            return HttpResponse("No model!")
        subprocess.call('./build.sh -m ' + modelname, shell=True)
        return HttpResponse("OK")
