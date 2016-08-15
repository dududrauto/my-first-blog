from django.shortcuts import render

# Create your views here.
from app.models import Mandado, Oficial, Telefone, Diligencia, Tipo_Diligencia, Estatus_Cumprimento, \
    Foto, Audio, Comarca, Vara, Ordem
from app.serializers import MandadoSerializer, OficialSerializer, TelefoneSerializer,\
    DiligenciaSerializer, Tipo_DiligenciaSerializer, Estatus_CumprimetoSerializer, FotoSerializer, AudioSerializer, \
    VaraSerializer, ComarcaSerializer, OrdemSerializer
from rest_framework import generics
from django.contrib.auth.models import User
from rest_framework import permissions
from app.permissions import IsOwnerOrReadOnly
from django.views.decorators.csrf import csrf_exempt
import datetime
from app.printing import MyPrint
from io import BytesIO
from django.http import HttpResponse


def print_users(request):
    '''
    Gera o pdf de varias diligencias, chamando o metodo
    '''
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename="myUsers.pdf"'#se comentar essa linha o arquivo abre no navegador

    buffer = BytesIO()

    report = MyPrint(buffer, 'Letter')
    d = Diligencia.objects.all()#envia uma lista de diligencias para a função print_documentos
    pdf = report.print_documentos(d)

    '''

    d = Diligencia.objects.all()[0]#envia uma diligencia para a função print_documento
    pdf = report.print_documentos(d)

    '''
    response.write(pdf)
    return response


class ComarcaList(generics.ListCreateAPIView):
    queryset = Comarca.objects.all()
    serializer_class = ComarcaSerializer
    permission_classes = (permissions.DjangoModelPermissionsOrAnonReadOnly,)


class ComarcaDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Comarca.objects.all()
    serializer_class = ComarcaSerializer
    permission_classes = (permissions.DjangoModelPermissionsOrAnonReadOnly,)

class VaraList(generics.ListCreateAPIView):
    queryset = Vara.objects.all()
    serializer_class = VaraSerializer
    permission_classes = (permissions.DjangoModelPermissionsOrAnonReadOnly,)


class VaraDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Vara.objects.all()
    serializer_class = VaraSerializer
    permission_classes = (permissions.DjangoModelPermissionsOrAnonReadOnly,)


class AudioList(generics.ListCreateAPIView):
    queryset = Audio.objects.all()
    serializer_class = AudioSerializer
    permission_classes = (permissions.DjangoModelPermissionsOrAnonReadOnly,)


class AudioDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Audio.objects.all()
    serializer_class = AudioSerializer
    permission_classes = (permissions.DjangoModelPermissionsOrAnonReadOnly,)


class FotoList(generics.ListCreateAPIView):
    queryset = Foto.objects.all()
    serializer_class = FotoSerializer
    permission_classes = (permissions.DjangoModelPermissionsOrAnonReadOnly,)


class FotoDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Foto.objects.all()
    serializer_class = FotoSerializer
    permission_classes = (permissions.DjangoModelPermissionsOrAnonReadOnly,)


class EstatusCumprimentoList(generics.ListCreateAPIView):
    queryset = Estatus_Cumprimento.objects.all()
    serializer_class = Estatus_CumprimetoSerializer
    permission_classes = (permissions.DjangoModelPermissionsOrAnonReadOnly,)


class EstatusCumprimentoDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Estatus_Cumprimento.objects.all()
    serializer_class = Estatus_CumprimetoSerializer
    permission_classes = (permissions.DjangoModelPermissionsOrAnonReadOnly,)


class OrdemList(generics.ListCreateAPIView):
    queryset = Ordem.objects.all()
    serializer_class = OrdemSerializer
    permission_classes = (permissions.DjangoModelPermissionsOrAnonReadOnly,)


class OrdemDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Ordem.objects.all()
    serializer_class = OrdemSerializer
    permission_classes = (permissions.DjangoModelPermissionsOrAnonReadOnly,)


class TipoDiligenciaList(generics.ListCreateAPIView):
    queryset = Tipo_Diligencia.objects.all()
    serializer_class = Tipo_DiligenciaSerializer
    permission_classes = (permissions.DjangoModelPermissionsOrAnonReadOnly,)


class TipoDiligenciaDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Tipo_Diligencia.objects.all()
    serializer_class = Tipo_DiligenciaSerializer
    permission_classes = (permissions.DjangoModelPermissionsOrAnonReadOnly,)


class DiligenciaList(generics.ListCreateAPIView):
    queryset = Diligencia.objects.all()
    serializer_class = DiligenciaSerializer
    permission_classes = (permissions.DjangoModelPermissionsOrAnonReadOnly,)


class DiligenciaDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Diligencia.objects.all()
    serializer_class = DiligenciaSerializer
    permission_classes = (permissions.DjangoModelPermissionsOrAnonReadOnly,)

'''
class EnderecoList(generics.ListCreateAPIView):
    queryset = Endereco.objects.all()
    serializer_class = EnderecoSerializer


class EnderecoDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Endereco.objects.all()
    serializer_class = EnderecoSerializer


class CepList(generics.ListCreateAPIView):
    queryset = CEP.objects.all()
    serializer_class = CepSerializer


class CepDetail(generics.RetrieveUpdateDestroyAPIView):#para não deletar trocar a generic por outra
    queryset = CEP.objects.all()
    serializer_class = CepSerializer
'''

class MandadoList(generics.ListCreateAPIView):
    #queryset = Mandado.objects.all()
    serializer_class = MandadoSerializer
    permission_classes = (permissions.DjangoModelPermissionsOrAnonReadOnly,)
    #permission_classes = (permissions.IsAuthenticated,) #.IsAuthenticatedOrReadOnly,)

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
    #permission_classes = (permissions.IsAuthenticatedOrReadOnly,IsOwnerOrReadOnly,)
    permission_classes = (permissions.DjangoModelPermissionsOrAnonReadOnly,)


class TelefoneList(generics.ListCreateAPIView):
    queryset = Telefone.objects.all()
    serializer_class = TelefoneSerializer
    permission_classes = (permissions.DjangoModelPermissionsOrAnonReadOnly,)

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)

    def get_queryset(self):
        """
        This view should return a list of all the purchases
        for the currently authenticated user.
        """
        user = self.request.user
        return Telefone.objects.filter(oficial__usuario=user)


class TelefoneDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Telefone.objects.all()
    serializer_class = TelefoneSerializer
    permission_classes = (permissions.DjangoModelPermissionsOrAnonReadOnly,)


class OficialList(generics.ListAPIView):
    queryset = Oficial.objects.all()
    serializer_class = OficialSerializer
    permission_classes = (permissions.DjangoModelPermissionsOrAnonReadOnly,)


class OficialDetail(generics.RetrieveAPIView):
    queryset = Oficial.objects.all()
    serializer_class = OficialSerializer
    permission_classes = (permissions.DjangoModelPermissionsOrAnonReadOnly,)


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