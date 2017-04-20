from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from acorta.models import AcortaUrl
from django.views.decorators.csrf import csrf_exempt

# Create your views here.
@csrf_exempt
def acortar(request):
    if request.method == "GET":
        list_urls = AcortaUrl.objects.all()
        if AcortaUrl.objects.all().exists():
            resp = "Urls acortadas:<br/>"
            for i in list_urls:
                resp += str(i.id) + " que proviene de: " + i.url_larga + "<br/>"
        else:
            resp = "No hay ninguna url acortada"

        resp += "Introduce la url que desee acortar" \
                "<form method='POST' action>" \
                "URL: <input type='text' name='url_larga'><br>" \
                "<input type='submit' value='Enviar'></form>"
        return HttpResponse(resp)

    elif request.method == "POST":
        #url = urllib.parse.unquote(request.POST['url_larga'])
        acortada = False
        url = request.POST['url_larga']
        if url.startswith('http://') or url.startswith('https://'):
            url_real = url
        else:
            url_real = "http://" + url
        list_urls = AcortaUrl.objects.all()
        for i in list_urls:
            if i.url_larga == url_real:
                url_acortada = AcortaUrl.objects.get(url_larga = url_real)
                url_acortada = url_acortada.id
                acortada = True
        if acortada == False:
            url_nueva = AcortaUrl(url_larga = url_real)
            url_nueva.save()
            url_acortada = url_nueva.id
        resp = "url_acortada: " + str(url_acortada), " que proviene de: " + url_real
        return HttpResponse(resp)
    else:
        return HttpResponse('Method not allowed', status=405)

def redirigir(request, numero):
    try:
        url_real = AcortaUrl.objects.get(id=numero).url_larga
        return HttpResponseRedirect(url_real)
    except AcortaUrl.DoesNotExist:
        resp = "El numero de la url que ha indicado no es correcto o no se encuentra disponible"
        return HttpResponse(resp)
