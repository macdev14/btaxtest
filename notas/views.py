from django.shortcuts import render
from django.http import HttpResponseRedirect

from django.shortcuts import render, reverse
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse, Http404
from django.contrib.auth.decorators import login_required
from django.template.loader import render_to_string

from tecnospeed import plugnotas
from mongodb import querys

COLLECTION_MONGO_NAME = 'notas'

@login_required
def lista(request):
    conta = request.user.profile.conta
    notas = querys.filtra_objs(COLLECTION_MONGO_NAME, {'conta_id': str(conta.id)})

    return render(request, 'notas/lista.html', 
        {
            'notas': notas,
        }
    )