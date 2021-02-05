from django.shortcuts import render, redirect
from django.views.decorators.csrf import csrf_protect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from .models import Pessoa
import requests

# Create your views here.


def login_user(request):
    return render(request, 'login.html')


@csrf_protect
def submit_login(request):
    if request.POST:
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('/')
        else:
            messages.error(request, ' Invalid user or password. Try another')
    return redirect('/login/')


def logout_user(request):
    logout(request)
    return redirect('/login/')


@login_required(login_url='/login/')
def list_all_pessoas(request):
    pessoa = Pessoa.objects.all().order_by('nome')
    return render(request, 'index.html', {'pessoa': pessoa})


def register_pessoa(request):
    #pessoa_id = request.POST.get('_id') nao funciona =/
    pessoa_id = request.GET.get("id")
    if pessoa_id:
        pessoa = Pessoa.objects.get(id=pessoa_id)
        return render(request, 'register-pessoa.html', {'pessoa': pessoa})
    else: 
        return render(request, 'register-pessoa.html')


@login_required(login_url='/login/')
def delete_pessoa(request, id):
    pessoa = Pessoa.objects.get(id=id)
    pessoa.delete()
    return redirect('/pessoas/all/')


@login_required(login_url='/login/')
def set_pessoa(request):
    nome = request.POST.get('nome')
    sobrenome = request.POST.get('sobrenome')
    apelido = request.POST.get('apelido')
    idade = request.POST.get('idade')
    email = request.POST.get('email')
    data_nascimento = request.POST.get('data_nascimento')
    observacao = request.POST.get('observacao')

    if(nome and sobrenome and idade and email and data_nascimento):
        pessoa = Pessoa.objects.create(
            nome=nome, sobrenome=sobrenome,
            apelido=apelido, idade=idade,
            email=email, data_nascimento=data_nascimento,
            observacao=observacao)
        return redirect('/pessoas/all')

    else:
        messages.error(request, ' Campo obrigatorio vazio!')
        return redirect('/pessoas/register')


@ login_required(login_url='/login/')
def generate(request):
    nome = requests.get(
        "https://gerador-nomes.herokuapp.com/apelidos/25").json()[0]
    sobrenome = requests.get(
        "https://gerador-nomes.herokuapp.com/apelidos/25").json()[1]
    return render(request, 'register-pessoa.html', {'nome': nome, 'sobrenome': sobrenome})
