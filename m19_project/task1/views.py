from django.shortcuts import render
from django.views.generic import TemplateView
from django.http import HttpResponse

from task1.forms import UserRegister
from task1.models import *

buyers_list = []


# Create your views here.
class Platform(TemplateView):
    template_name = 'platform.html'
    title = 'Главная'
    pagename = 'Главная страница'
    content = 'Мы рады приветствовать Вас в нашем магазине компьютерных игр!'
    extra_context = {
        'title': title,
        'pagename': pagename,
        'content': content,
    }


class Games(TemplateView):
    template_name = 'games.html'
    title = 'Каталог'
    pagename = 'Игры'
    # games = ['Atomic Heart', 'Cyberpunk 2077', 'PayDay 2', 'Doom 2']
    games = Game.objects.all()
    extra_context = {
        'title': title,
        'pagename': pagename,
        'games': games,
    }


class Cart(TemplateView):
    template_name = 'cart.html'
    title = 'Корзина'
    pagename = 'Корзина'
    content = 'Извините, ваша корзина пуста'
    extra_context = {
        'title': title,
        'pagename': pagename,
        'content': content,
    }


def check_data(data):
    buyers = Buyer.objects.all()
    for buyer in buyers:
        buyers_list.append(buyer.name)
    if data['name'] in buyers_list:
        return 'Пользователь уже существует'
    elif data['password'] != data['repeat_password']:
        return 'Пароли не совпадают'
    elif int(data['age']) < 16:
        return 'Вы должны быть старше 18'
    return f'Приветствуем, {data['name']}!'

def sign_up_by_django(request):
    info = {}
    if request.method == 'POST':
        form = UserRegister(request.POST)
        if form.is_valid():
            name = form.cleaned_data['name']
            password = form.cleaned_data['password']
            repeat_password = form.cleaned_data['repeat_password']
            age = form.cleaned_data['age']
            info = {'name': name,
                    'password': password,
                    'repeat_password': repeat_password,
                    'age': age,
                    }
            check = check_data(info)
            if 'Приветствуем' in check:
                info.update({'greetings': check})
                Buyer.objects.create(name=name, password=password, age=age)
            else:
                info.update({'error': check})
    else:
        form = UserRegister()
    info.update({'form': form})
    return render(request, 'registration_page.html', info)


def sign_up_by_html(request):
    info = {}
    if request.method == 'POST':
        name = request.POST.get('name')
        password = request.POST.get('password')
        repeat_password = request.POST.get('repeat_password')
        age = request.POST.get('age')
        info = {'name': name,
                'password': password,
                'repeat_password': repeat_password,
                'age': age,
                }
        check = check_data(info)
        if 'Приветствуем' in check:
            info.update({'greetings': check})
            Buyer.objects.create(name=name, password=password, age=age)
        else:
            info.update({'error': check})
    return render(request, 'registration_page.html', info)
