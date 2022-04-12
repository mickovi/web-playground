from django.http import Http404
from django.shortcuts import redirect, render
from django.urls import reverse_lazy
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from django.views.generic import TemplateView
from .models import Thread, Message
from django.http import Http404, JsonResponse
from django.shortcuts import get_object_or_404, redirect
from django.contrib.auth.models import User
from django.urls import reverse_lazy

from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator

# Decoramos el método para verificar si el usuario existe
""" @method_decorator(login_required, name='dispatch')
class ThreadList(ListView):
    model = Thread # Todas las instancias del modelo Thread

    # Sobreescribimos el filtro para extraer el usuario
    def get_queryset(self):
        queryset = super(ThreadList, self).get_queryset()
        return queryset.filter(users=self.request.user) """

# Usando la relación inversa user.threads.all() podemos consultar los hilos que forman parte del usuario
@method_decorator(login_required, name='dispatch')
class ThreadList(TemplateView):
    # En el template podemos consultar los hilos del ususario
    template_name = 'messenger/thread_list.html'

@method_decorator(login_required, name='dispatch')
class ThreadDetail(DetailView):
    model = Thread

    # get_ebject es el método para filtrar instancias de DetailView
    # Debemos evitar que un usuario acceda a un hilo que no es parte
    def get_object(self):
        obj = super(ThreadDetail, self).get_object()
        # Búsqueda inversa
        if self.request.user not in obj.users.all():
            raise Http404()
        return obj

def add_messenge(request, pk):
    # print(request.GET)
    json_response = {'created': False}
    if request.user.is_authenticated:
        content = request.GET.get('content', None)
        if content:
            thread = get_object_or_404(Thread, pk=pk) # Recuperamos el hilo
            message = Message.objects.create(user=request.user, content=content) # Crear un mensaje con el usuario identificado
            thread.messages.add(message) # Añadir el mensaje al hilo
            json_response['created'] = True # Se ha creado el mensaje
            if len(thread.messages.all()) is 1:
                json_response['first'] = True
    else:
        raise Http404('User is not authenticated')
        
    return JsonResponse(json_response) # obj python -> obj json

@login_required
def start_thread(request, username):
    user = get_object_or_404(User, username=username)
    thread = Thread.objects.find_or_create(user, request.user)
    return redirect(reverse_lazy('messenger:detail', args=[thread.pk]))
