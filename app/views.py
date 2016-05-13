from django.shortcuts import render

# Create your views here.
from app.models import Mandado, Oficial
from app.serializers import MandadoSerializer, OficialSerializer
from rest_framework import generics
from django.contrib.auth.models import User
from rest_framework import permissions
from app.permissions import IsOwnerOrReadOnly
from django.views.decorators.csrf import csrf_exempt
import datetime



"""
            fazer o serializer e o view do endereco e do telefone dos mandados em aberto do oficial

            ver para utilizar session em swift, se aceita cookies no ios, para o acesso as views do REST
            para ler o endereco e telefone por exemplo. ou se nao tenho que proceder a consulta dos mandados
            e depois formar o queryset dos enderecos, telefones e status relacionados ao mandado para
            preencher o db do aplicativo


"""



class MandadoList(generics.ListCreateAPIView):
    queryset = Mandado.objects.all()
    serializer_class = MandadoSerializer
    permission_classes = (permissions.IsAuthenticated,) #.IsAuthenticatedOrReadOnly,)

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)

    def get_queryset(self):
        """
        This view should return a list of all the purchases
        for the currently authenticated user.
        """
        user = self.request.user
        return Mandado.objects.filter(oficial__usuario=user)


class MandadoDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Mandado.objects.all()
    serializer_class = MandadoSerializer
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,
                           IsOwnerOrReadOnly,)


class OficialList(generics.ListAPIView):
    queryset = Oficial.objects.all()
    serializer_class = OficialSerializer


class OficialDetail(generics.RetrieveAPIView):
    queryset = Oficial.objects.all()
    serializer_class = OficialSerializer

"""

#testes pdf Pisa
from django.shortcuts import get_object_or_404
from django.template.loader import get_template
from django.template import Context
from django.http import HttpResponse
import cStringIO as StringIO
from sx.pisa3 import pisaDocument
import cgi
from django.template import Template

def article(request, id):
    mand = get_object_or_404(Mandado, pk=id)
    return render_to_pdf('doc_template.html', {
        'pagesize' : 'A4',
        'article' : str(mand.ordem.modelo.modelo).replace('\r','').replace('\n','').replace('\'', '"'),
        'mandado': mand,
        'date': datetime.date.today(),
        }, template_in_context=True)

def render_to_pdf(template_src, context_dict, template_in_context=True):
    template = get_template(template_src)
    context = Context(context_dict)
    html = template.render(context)
    if template_in_context:
        template = Template(html)
        html = template.render(context)
    result = StringIO.StringIO()
    pdf = pisaDocument(StringIO.StringIO(html.encode("ISO-8859-1")), result)
    if not pdf.err:
        return HttpResponse(result.getvalue(), mimetype='application/pdf')
    return HttpResponse('We had some errors<pre>%s</pre>' % cgi.escape(html))




"""