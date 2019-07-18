# coding=utf-8
from django.http import HttpResponseRedirect
from django.shortcuts import render
from event.models import Users, Event, Assos, Assos_user, DocumentForm, EventForm

from django.db.models import Q
from django.views.generic import ListView, DetailView
from django.contrib.auth import logout
from django.views.generic import DetailView

import gnupg
import os
import shutil
from io import BytesIO
from django.http import HttpResponse
from django.template.loader import get_template

from xhtml2pdf import pisa
from django.views.generic import View


def home(request):
    """
    Redirige vers la page de connexion.
    """

    template = "connect.html"
    context = {}
    return render(request, template, context)


def logout_view(request):
    """
    Déconnecte l'utilisateur et le redirige vers la page de connexion.
    """

    logout(request)
    return home(request)


def assos(request):
    """
    Redirige vers la page listant les associations.
    """

    allassos = Assos.objects.all()
    template = "assos.html"
    context = {'allassos':allassos}
    return render(request, template, context)


def membres(request):
    """
    Redirige vers la page listant les membres du site.
    """

    allusers = Users.objects.all()
    username = request.user
    user = Users.objects.get(login=username)
    assos_user = Assos_user.objects.filter(user_id=user.id)

    template = "membres.html"
    context = {'allusers':allusers, 'status' : user.status, 'assos_user' : assos_user}
    return render(request, template, context)


def events(request):
    """
    Redirige vers la page listant les évènements existants.
    """

    username = request.user
    user = Users.objects.get(login=username)
    assos_user = Assos_user.objects.filter(user_id=user.id)

    allevents = Event.objects.all()

    context = {'allevents':allevents, 'user':user}

    if (assos_user):
        context = {'allevents': allevents, 'user': user, 'assos' : assos_user}

    template = "events.html"

    return render(request, template, context)


def validate_event(request, pk):
    username = request.user
    user = Users.objects.get(login=username)
    assos_user = Assos_user.objects.filter(user_id=user.id)
    allevents = Event.objects.all()
    context = {'allevents':allevents, 'user':user}

    eventt = Event.objects.filter(pk=pk)

    ev = None
    if eventt:
        ev = Event.objects.get(pk=pk)
        ev.status = "validated"
        ev.save()

    if (assos_user):
        context = {'allevents': allevents, 'user': user, 'assos' : assos_user}

    # event =

    return render(request, 'events.html', context)

def profile_page(request):
    """
    Redirige vers la page de profil de l'utilisateur.\n
    L'utilisateur peut également mettre sa signature en ligne, elle est alors chiffrée avec une clé de session. La clé
    de session est ensuite chiffrée avec la clé publique de l'utilisateur.\n
    La signature chiffrée et la clé de session chiffrée sont ensuite sauvegardées sur le système de fichiers du tiers de
    confiance.
    """

    if request.method == 'POST':
        username = request.user
        user = Users.objects.get(login=username)
        form = DocumentForm(request.POST, request.FILES, instance=user)

        if form.is_valid():

            # file is saved
            form.save()
            username = request.user
            user = Users.objects.get(login=username)

            assos_user = Assos_user.objects.filter(user_id=user.id)

            context = {"user": user, 'status': user.status, 'form': form}

            if (assos_user):
                context = {'user': user, 'assos': assos_user, 'status': user.status}

            # print('Signature path: ' + str(user.signature_file))

            encrypt_signature(user.email, str(user.signature_file))

            return render(request, "profile.html", context)
    else:
        form = DocumentForm()

    username = request.user
    user = Users.objects.get(login=username)

    assos_user = Assos_user.objects.filter(user_id=user.id)

    context = {"user":user, 'status' : user.status, 'form': form}

    if (assos_user):
        context = {'user': user, 'assos' : assos_user, 'status' : user.status, 'form': form}

    return render(request, "profile.html", context)


def encrypt_signature(email, path):
    """
    Chiffre la signature mise en ligne par l'utilisateur avec une clé de session.
    """

    key_list = path.split('/')
    key_path = './Tiers_de_confiance/' + key_list[2] + '/' + key_list[3] + '.gpg'
    if os.path.isfile(key_path):
        os.remove(key_path)
    elif not os.path.exists('Tiers_de_confiance/' + key_list[2]):
        os.mkdir('Tiers_de_confiance/' + key_list[2])

    gpg = gnupg.GPG(gnupghome='./GPG/gpghome')
    with open(path, 'rb') as f:
        status = gpg.encrypt_file(
            f, recipients=[email],
            output=key_path,
            symmetric=True)

        print('Encrypted file:')
        print('ok: ', status.ok)
        print('status: ', status.status)
        print('stderr: ', status.stderr)

    shutil.rmtree('./' + key_list[0] + '/' + key_list[1] + '/' + key_list[2], ignore_errors=True)



def forms(request):
    """
    Redirige vers la page listant les formulaires existants.
    """

    event = Event.objects.all()
    username = request.user
    user = Users.objects.get(login=username)

    context = {"event":event, 'status' : user.status}
    return render(request, "forms.html", context)




class EventDetailView(DetailView):
    model = Event
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['event'] = Event.name
        return context


class AssosDetail(DetailView):
    model = Assos

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['assos'] = Assos.name
        return context


class searchListView(ListView):
    paginate_by = 10
    def get_queryset(self):
        result = super(searchListView, self).get_queryset()
        query = request.GET.get('q')
        if query:
            query_list = query.split()
            result = result.filter(
                reduce(operator.and_,
                    (Q(firstname__icontains=q) for q in query_list)) |
                reduce(operator.and_,
                    (Q(lastname__icontains=q) for q in query_list)) |
                reduce(operator.and_,
                    (Q(login__icontains=q) for q in query_list))
            )
        return result


def render_to_pdf(template_src, context_dict={}):
    """
    Génère un pdf à partir d'un template Django.
    """

    template = get_template(template_src)
    html = template.render(context_dict)
    result = BytesIO()
    pdf = pisa.pisaDocument(BytesIO(html.encode("ISO-8859-1")), result)
    if not pdf.err:
        return HttpResponse(result.getvalue(), content_type='application/pdf')
    return None


class GeneratePDF(View):
    """
    Génère un pdf avec les informations d'un évènement.
    """


    def get(self, request, *args, **kwargs):
        template = get_template('invoice.html')
        form = Event.objects.get(pk=kwargs['pk'])
        context = {
            "form":form
        }
        html = template.render(context)
        pdf = render_to_pdf('invoice.html', context)
        if pdf:
            response = HttpResponse(pdf, content_type='application/pdf')
            filename = "Event_%s.pdf" %(kwargs['pk'])
            content = "inline; filename='%s'" %(filename)
            download = request.GET.get("download")
            if download:
                content = "attachment; filename='%s'" %(filename)
            response['Content-Disposition'] = content
            return response
        return HttpResponse("Not found")
