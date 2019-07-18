# coding=utf-8
from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from .models import Event, EventForm, DocumentForm
from django.views.generic.edit import CreateView
from django.contrib.auth.decorators import login_required
from .models import Users

import gnupg
import os
from django.http import HttpResponse


def index(request):
    """
    Redirection vers une page après validation du formulaire.
    """

    return render(request, 'home.html')


def get_passphrase(request):
    """
    Affiche une page de demande de passphrase pour la génération de la paire de clés asymétriques.
    """

    return render(request, 'passphrase.html')


@login_required
def logged_after_passphrase(request):
    """
    Vérifie que l'authentification du CRI a fonctionné.\n
    L'utilisateur est renvoyé vers la page d'accueil.
    """

    user = request.user
    data = request.user.social_auth.get(provider="epita").extra_data
    passphrase = request.POST.get('textfield', None)
    public_key, private_key = gen_keys(user.email, passphrase)
    if not os.path.exists('Tiers_de_confiance/'):
        os.mkdir('Tiers_de_confiance/')
    print(1)
    user_dir = 'user_{0}/'.format(user.username)
    os.mkdir('Tiers_de_confiance/' + user_dir)

    with open('Tiers_de_confiance/' + user_dir + 'public_key_' + user.username + '.asc', 'w') as f:
        f.write(public_key)

    new_user = Users(status="student", login=user.username, lastname=user.last_name,
                     firstname=user.first_name, email=user.email, private_key=private_key)
    new_user.save()

    myuser = Users.objects.get(login=user.username)

    allevents = Event.objects.all()
    context = {
        'user': user,
        'extra_data': data,
        'status' : myuser.status,
        'allevents': allevents
    }
    return render(request, 'home.html', context)


@login_required
def logged(request):
    """
    Vérifie que l'authentification du CRI a fonctionné.\n
    Si l'utilisateur se connecte pour la première fois:\n
    Il est renvoyé vers une page lui demandant de rentrer un passphrase pour générer une paire de clés asymétriques.\n
    Sinon:\n
    Il est renvoyé vers la page d'accueil.
    """

    user = request.user

    test_user = Users.objects.filter(login=user.username).count()
    if test_user == 0:
        return render(request, 'passphrase.html')

    myuser = Users.objects.get(login=user.username)

    data = request.user.social_auth.get(provider="epita").extra_data

    allevents = Event.objects.all()
    context = {
        'user': user,
        'extra_data': data,
        'status' : myuser.status,
        'allevents': allevents
    }
    return render(request, 'home.html', context)


def gen_keys(email, passphrase):
    """
    Génère une paire de clés asymétriques publique/privée avec pgp.
    """

    gpg = gnupg.GPG(gnupghome='./GPG/gpghome')
    input_data = gpg.gen_key_input(
        name_email=email,
        passphrase=passphrase)
    key = gpg.gen_key(input_data)
    ascii_armored_public_keys = gpg.export_keys(key.fingerprint)
    ascii_armored_private_keys = gpg.export_keys(key.fingerprint, True, passphrase=passphrase)
    return ascii_armored_public_keys, ascii_armored_private_keys
