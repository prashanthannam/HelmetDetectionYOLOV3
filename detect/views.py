from django.shortcuts import render,redirect
# import cv2
from django.http import HttpResponse,HttpResponseRedirect
from .forms import *
from django.conf import settings
from .models import Helmet
from django.core.files.storage import FileSystemStorage
from django.contrib.auth.decorators import login_required
from recpic1 import ma
from recvid import ma1
from darkflow.net.build import TFNet
import os

# loading the models
options = {
    'model': 'cfg/tiny-yolo-voc-3c.cfg',
    'load': 13125,
    'threshold': 0.4,
    }
# options1 = {
#     'model': 'cfg/tiny-yolo-voc-3c1.cfg',
#     'load': 2375,
#     'threshold': 0.3,
#     'labels':'labels1.txt'
#     }
tfnet = TFNet(options)
# tfnet1 = TFNet(options1)
def conv_dir(dir):
    dir2=""
    for i in dir:
        if i=='\\':
            dir2=dir2+"/"
        else:
            dir2=dir2+i
    return dir2            

@login_required(login_url='/accounts/login')
def helmetview(request):
    if request.method=='POST':
        directory = settings.MEDIA_ROOT
        print(directory)
        for filename in os.listdir(directory):
            os.remove(directory+"/"+filename)
    if request.method=='POST':
        if request.FILES:
            myfile=request.FILES['img']
            fs=FileSystemStorage()
            # saving image in the server
            filename=fs.save('img.png',myfile)
            upload_file_url=fs.url(filename)

            base_directory = conv_dir(settings.BASE_DIR)

            print(base_directory)
            # calling the object detection function
            arr=ma(base_directory+upload_file_url, tfnet)
            print(upload_file_url)
            p_no=arr[0]
            b_no=arr[1]
            plate_ar=arr[2]
            if arr[3]==0:
                total_bikes=None
            else:
                total_bikes=arr[3]
            user_name=request.user
            pl=[]
            bi=[]
            for i in range(0,p_no):
                val='/media/plate'+str(i+1)+'.png'
                pl.append(val)
            for i in range(0,b_no):
                val='/media/bike'+str(i+1)+'.png'
                bi.append(val)
            print(pl)
            plate_data=zip(pl,plate_ar)
            return render(request,'detect/index.html',{'url':upload_file_url,'p_data':plate_data,'b_list':bi, 'b_no':b_no, 'tot_bikes':total_bikes, 'p_url':pl})
    
    user_name=request.user
    directory = settings.MEDIA_ROOT
    # for filename in os.listdir(directory):
    #     os.remove(directory+"/"+filename)
    return render(request,'detect/index.html',{'user_name':user_name})








@login_required(login_url='/accounts/login')
def helmetview1(request):
    if request.method=='POST':
        directory = settings.MEDIA_ROOT
        for filename in os.listdir(directory):
            os.remove(directory+"/"+filename)
    BASE="C:/detection_helmet/djano-project/Helmet"
    if request.method=='POST':
        if request.FILES:
            myfile=request.FILES['vid']
            fs=FileSystemStorage()
            filename=fs.save('vid.mp4',myfile)
            upload_file_url=fs.url(filename)
            print(BASE+upload_file_url)
            print('a')
            arr=ma1("C:/detection_helmet/djano-project/Helmet"+upload_file_url, tfnet, tfnet1)
            p_no=arr[0]
            b_no=arr[1]
            plate_ar=arr[2]
            user_name=request.user
            pl=[]
            bi=[]
            for i in range(0,p_no):
                val='/media/plate'+str(i+1)+'.png'
                pl.append(val)
            for i in range(0,b_no):
                val='/media/bike'+str(i+1)+'.png'
                bi.append(val)
            print(pl)
            plate_data=zip(pl,plate_ar)
            return render(request,'detect/index1.html',{'url':upload_file_url,'p_data':plate_data,'b_list':bi, 'b_no':b_no})
    
    user_name=request.user
    directory = settings.MEDIA_ROOT
    for filename in os.listdir(directory):
        os.remove(directory+"/"+filename)
    return render(request,'detect/index1.html',{'user_name':user_name})

@login_required(login_url='/accounts/login')
def base(request):
    return render(request,'detect/index.html') 

def success(request):
    helmets=Helmet.objects.all()
    return render(request,'detect/display.html',{'hel':helmets})

    # new_item=request.POST['img']
    # # cv2.imshow('img',new_item)
    # return render(request,'index.html',{'data':new_item})
    