from django.shortcuts import render
from django.http import HttpResponse
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from .models import *
import requests
import json
import random


def question_answer(subject_id):
    id =str(subject_id)
    r = requests.get("https://opentdb.com/api.php?amount=10&category="+id+"&type=multiple")
    fetch_data = json.loads(r.content)
    data = fetch_data['results']
    nd = modify(data)
    return nd


def modify(d):
    for i in range(10):
        d[i]['id'] = i
        d[i]['question'] = clean(d[i]['question'])
        d[i]['correct_answer'] = clean(d[i]['correct_answer'])
        d[i]['incorrect_answers'] = [clean(k) for k in d[i]['incorrect_answers']]
        d[i]['options'] = list(d[i]['incorrect_answers'])
        d[i]['options'].append(d[i]['correct_answer'])
        random.shuffle(d[i]['options'])
    return d


def clean(var):
    for z in ['&quot;', '&ldquo;', '&rdquo;', '&#039;', '&deg;', '&amp;','&Ouml;', '&ouml;', '&uuml;','&amp;','&pi;','&delta;', '&Delta;', '&prime;', '&Prime;','&eacute;']:
        replacewith = z
        replaceby = ''
        if z == '&pi;':
            replaceby = 'pi '
        if z == '&delta;':
            replaceby='Delta '
        if z == '&Delta;':
            replaceby='Delta'
        if z == '&prime;':
            replaceby='FEET '
        if z == '&Prime;':
            replaceby='INCH'
        if z == '& eacute;':
            replaceby = 'e'

        var = var.replace(replacewith, replaceby)
    return var

# Create your views here.
def home(request):
    subject = Subject.objects.all()
    context = {'subjects': subject}
    return render(request, 'index.html', context)

def emailExist(email):
    user = User.objects.filter(email=email).first()
    if user:
        b = True
    else:
        b= False
    return b



def Subjects(request):
    if request.user.is_authenticated ==False:
        msg= {'msg': 'Only Registered User Can Take Quiz'}
        return render(request, 'login.html', msg)

    else:
        if request.method == 'POST':
            subject_name = request.POST.get('subject')
            subject = Subject.objects.get(name=subject_name)
            quiz_data = question_answer(subject.subject_id)

            context = {'quiz_data': quiz_data}
            return render(request, 'quiz.html', context)


def register(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        email = request.POST.get('email')
        flag = emailExist(email)
        if flag:
            return render(request, 'register.html', {'msg': 'Email already exists'})
        user = User(username=username, email=email)
        user.set_password(password)
        user.save()
        return render(request, 'login.html')

    else:
        return render(request, 'register.html')




def Login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(username=username, password=password)
        if user is None:
            context = {'msg': 'something is wrong'}
            return render(request, 'login.html', context)
        else:
            login(request, user)
            subject = Subject.objects.all()
            context = {'subjects': subject}
            return render(request, 'index.html', context)
    else:
        return render(request, 'login.html')



def Logout(request):
    logout(request)
    return render(request, 'login.html')


def result(request):
    if request.method == 'POST':
        name = request.user.username
        username = User.objects.get(username=name)
        quiz_data = Quiz_data.objects.create(username=username)
        quiz_data.save()
        for i in range(10):
            questionId = 'q' + str(i)
            correctId = 'c' + str(i)
            selectedId = 's' + str(i)
            statusId = 'N' + str(i)
            qus = request.POST.get(questionId)
            correct_answer = request.POST.get(correctId)
            selected_answer = request.POST.get(selectedId)
            status = request.POST.get(statusId)

            quiz = Quiz.objects.create(quiz_id=quiz_data, question=qus, correct_answer=correct_answer, selected_answer=selected_answer, status=status )
            quiz.save()

        q = Quiz.objects.filter(quiz_id=quiz_data.id)
        num, result = cal(q)
        time = request.POST.get('t9')
        min, sec = min_sec(time)
        context = {'num': num, 'result': result, 'quiz': q, 'min': min, 'sec':sec}



        return render(request, 'results.html', context)
    else:
        return HttpResponse('somthing is wrong')



def cal(ob):
    b= 0
    for i in ob :
        b = b + i.status
    if b<4 :
        result = 'Fail'
    else:
        result = 'Pass'
    return b, result

def min_sec(time):
    t = int(float(time))
    min = round(t/60)
    sec = t%60
    return min, sec

