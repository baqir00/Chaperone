from .form import Loginform, Signupform
from django.shortcuts import render, get_object_or_404, redirect, reverse
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponseRedirect, Http404
from django.http import HttpResponse, JsonResponse
from bs4 import BeautifulSoup
import requests
from django.core.files.storage import FileSystemStorage
from pdfminer.pdfinterp import PDFResourceManager, PDFPageInterpreter
from pdfminer.converter import TextConverter
from pdfminer.layout import LAParams
from pdfminer.pdfpage import PDFPage
from io import StringIO
from .models import Result
from random import randint
import re, json, glob
from collections import Counter

RUN_URL = u'http://api.hackerearth.com/code/run/'
COMPILE_URL = u'http://api.hackerearth.com/code/compile/'
CLIENT_SECRET = '7187a7186abc85dcbe21f965e0b94bb05776f931'


def convert_pdf_to_txt(path):
    rsrcmgr = PDFResourceManager()
    retstr = StringIO()
    codec = 'utf-8'
    laparams = LAParams()
    device = TextConverter(rsrcmgr, retstr, codec=codec, laparams=laparams)
    fp = open(path, 'rb')
    interpreter = PDFPageInterpreter(rsrcmgr, device)
    password = ""
    maxpages = 0
    caching = True
    pagenos = set()
    for page in PDFPage.get_pages(fp, pagenos, maxpages=maxpages, password=password, caching=caching,
                                  check_extractable=True):
        interpreter.process_page(page)
    text = retstr.getvalue()
    fp.close()
    device.close()
    retstr.close()
    return text


def r1(request):
    if request.method == 'POST' and request.FILES['file']:
        myfile = request.FILES['file']
        fs = FileSystemStorage()
        filename = fs.save("documents/" + request.user.username + ".pdf", myfile)
        uploaded_file_url = fs.url(filename)
        a = convert_pdf_to_txt(fs.path(filename))
        result = Result.objects.get(username=request.user)
        if re.search('debate', a, re.IGNORECASE):
            result.mba += result.mba / 10 + 0.8
            result.mbawe += result.mbawe / 10 + 0.7
            result.priv += result.priv / 10 + 0.5
            result.entre += result.entre / 10 + 0.7
            result.civil += result.civil / 10 + 0.2
            result.govt += result.govt / 10 + 0.2
        pattern1 = re.compile(
            r"\btopcoder\b|\bspoj\b|\bhackerearth\b|\bhackerrank\b|\bcodechef\b|\bacm\b|\beuler\b|\bcodejam\b|\binternship\b",
            re.IGNORECASE)
        if re.search(pattern1, a):
            result.priv += result.priv / 10 + 0.9
        pattern2 = re.compile(
            r'\balgorithm\b|\bdata\b|\bstructure\b|\bc\b|\bcpp\b|\bcoding\b|\bprogramming\b|\bhtml\b|\blinux\b',
            re.IGNORECASE)
        if re.search(pattern2, a):
            result.priv += result.priv / 10 + 0.8
        if len(str(a)) < 2000:
            result.civil += result.civil
        if re.search('hobbies', a, re.IGNORECASE):
            result.bank += result.bank / 10 + 0.3
        pattern3 = re.compile(
            r'\bms office\b|\bms excel\b|\bwindows\b|\btype writing\b|\bwpm\b|\bimo\b|\bmathematics\b|\blinux\b',
            re.IGNORECASE)
        if re.search(pattern3, a):
            result.bank += result.bank / 10 + 0.8
        pattern4 = re.compile(
            r'\bieee\b|\bconferance\b|\bmachine learning\b|\bresearch\b|\bntse\b|\brank\b|\bcomputer vision\b|\bhtml\b|\blinux\b',
            re.IGNORECASE)
        if re.search(pattern4, a):
            result.ms += result.ms / 10 + 0.7
            result.mtech += result.mtech / 10 + 0.7
        result.save()
        return render(request, 'main/round1.html', {
            'uploaded_file_url': uploaded_file_url
        })
    return render(request, 'main/round1.html')


def index(request):
    return render(request, 'main/home.html')


def login_view(request):
    if request.method == "POST":
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(username=username, password=password)
        if user is not None:
            login(request, user)
            if request.method == "GET":
                if request.GET["next"]:
                    return HttpResponseRedirect(request.GET['next'])
            return render(request, 'main/home.html', {"user": user})
    return render(request, 'main/login.html', {"form": Loginform(request.POST or None)})


def signup_view(request):
    if request.method == "POST":
        form = Signupform(request.POST)
        if form.is_valid():
            user = User.objects.create_user(request.POST['username'], request.POST['email'], request.POST['password'])
            user.first_name = request.POST['first_name']
            user.last_name = request.POST['last_name']
            user.save()
            result = Result.objects.create(username=user)
            login(request, user)
            return render(request, 'main/home.html', {"user": user})
    return render(request, 'main/signup.html', {"form": Signupform(request.POST or None)})


def logout_view(request):
    logout(request)
    return redirect('main:index')


def contest(request):
    return render(request, 'main/contest.html')


def validate_spoj(request):
    username = request.GET.get('username', None)
    url = "http://www.spoj.com/users/" + username + "/"
    r = requests.get(url)
    data = r.text
    soup = BeautifulSoup(data)
    d = {'data': soup.find('dd').text}
    return JsonResponse(d)


def validate_hackerearth(request):
    user = request.GET.get('username', None)
    url = 'https://www.hackerearth.com/users/pagelets/' + user + '/coding-data/'.format(user)
    r = requests.get(url)
    soup = BeautifulSoup(r.text, 'lxml')
    d = {'data': soup.find(string='Problems Solved').find_next().text}
    return JsonResponse(d)


def validate_codechef(request):
    username = request.GET.get('username', None)
    url = "https://www.codechef.com/users/" + str(username) + "/"
    print(url)
    r = requests.get(url)
    data = r.text
    soup = BeautifulSoup(data)
    print(soup.find('h5'))
    d = {'data': soup.find('h5').text[14:-1]}
    return JsonResponse(d)


def validate_compile(request):
    lang = request.GET.get('lang', None)
    code = request.GET.get('code', None)
    data = {
        'client_secret': CLIENT_SECRET,
        'source': code,
        'lang': lang
    }
    r = requests.post(COMPILE_URL, data=data)
    a = r.json()
    d = {'compile_status': a["compile_status"]}
    return JsonResponse(d)


def validate_run(request):
    lang = request.GET.get('lang', None)
    code = request.GET.get('code', None)
    a = request.GET.get('id', None)
    fs = FileSystemStorage()
    passed = total = 0
    error = False
    for i in glob.glob(r"media\test\q" + str(a) + "in*.txt"):
        data = {
            'client_secret': CLIENT_SECRET,
            'source': code,
            'lang': lang,
            'input': fs.open(i[6:], mode='rb').read(),
        }
        r = requests.post(RUN_URL, data=data)
        b = r.json()
        try:
            output = b["run_status"]["output"]
            error = False
        except KeyError:
            output = "Compilation Error"
            error = True
        if Counter(output.rstrip()) == Counter(fs.open(i[6:13] + "out" + i[15:], mode='r').read().rstrip()):
            passed += 1
        total += 1
    d = {'run_status': str(passed) + "/" + str(total) + " test cases have been passed.", 'error': error}
    return JsonResponse(d)


def r2(request):
    a = randint(1, 5)
    a = 1
    fs = FileSystemStorage()
    q = fs.open('question/q' + str(a) + '.txt', mode='rb').read()
    i = fs.open('input/q' + str(a) + '.txt', mode='rb').read()
    o = fs.open('output/q' + str(a) + '.txt', mode='rb').read()
    c = fs.open('constraints/q' + str(a) + '.txt', mode='rb').read()
    return render(request, 'main/round2.html', {
        'q': q,
        'i': i,
        'o': o,
        'c': c,
        'id': a,
    })
