__author__ = 'Dudu'
from reportlab.lib.pagesizes import letter, A4
from reportlab.platypus import SimpleDocTemplate, Paragraph
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.enums import TA_CENTER
from django.contrib.auth.models import User
from reportlab.lib.units import inch
from reportlab.platypus import PageBreak
from html.parser import HTMLParser
from app.models import Modelo_Documento
from django import template
import html

import pdfkit
import os
from django.http import HttpResponse

class MyHTMLParser(HTMLParser):
    def __init__(self):
        super().__init__()
        self.list_data = []

    def handle_starttag(self, tag, attrs):
        print("Encountered a start tag:", tag)

    def handle_endtag(self, tag):
        print("Encountered an end tag :", tag)

    def handle_data(self, data):
        print("Encountered some data  :", data)
        self.list_data.append(data)


class MyPrint:

    def __init__(self, buffer, pagesize):
        self.buffer = buffer
        if pagesize == 'A4':
            self.pagesize = A4
        elif pagesize == 'Letter':
            self.pagesize = letter
        self.width, self.height = self.pagesize

    def print_documento(self, diligencia):
        """
        imprime o documento da diligencia
        :param diligencia: diligencia
        :return: pdf
        """
        buffer = self.buffer
        doc = SimpleDocTemplate(buffer,
                                rightMargin=72,
                                leftMargin=72,
                                topMargin=72,
                                bottomMargin=72,
                                pagesize=self.pagesize)

        # Our container for 'Flowable' objects
        elements = []

        # A large collection of style sheets pre-made for us
        styles = getSampleStyleSheet()
        styles.add(ParagraphStyle(name='centered', alignment=TA_CENTER))

        # Draw things on the PDF. Here's where de PDF generation happens.
        # See the ReportLab documentation for the full list of functionality.
        #users = User.objects.all()
        html = diligencia.documento
        parser = MyHTMLParser()
        parser.feed(html)
        documento = parser.list_data
        elements.append(Paragraph('My User Names', styles['Heading1'],))
        for i, user in enumerate(documento):
            #elements.append(Paragraph(user.get_full_name(), styles['Normal']))
            elements.append(Paragraph(user, styles['Normal']))
        #elements.append(PageBreak())

        doc.build(elements)#, onFirstPage=self._header_footer, onLaterPages=self._header_footer)

        # get the value os the BytesIO buffer and write in to the response.
        pdf = buffer.getvalue()
        buffer.close()
        return pdf

    def print_documentos(self, diligencias):
        """

        :param diligencias: lista de diligencias com os documentos que devem ser impressos
        :return:arquivo pdf com os documentos
        """
        buffer = self.buffer
        doc = SimpleDocTemplate(buffer,
                                rightMargin=72,
                                leftMargin=72,
                                topMargin=72,
                                bottomMargin=72,
                                pagesize=self.pagesize)

        # Our container for 'Flowable' objects
        elements = []

        # A large collection of style sheets pre-made for us
        styles = getSampleStyleSheet()
        styles.add(ParagraphStyle(name='centered', alignment=TA_CENTER))

        # Draw things on the PDF. Here's where de PDF generation happens.
        # See the ReportLab documentation for the full list of functionality.
        #users = User.objects.all()
        for diligencia in diligencias:
            html = diligencia.documento
            parser = MyHTMLParser()
            parser.feed(html)
            documento = parser.list_data
            elements.append(Paragraph('My User Names', styles['Heading1'],))
            for i, user in enumerate(documento):
                #elements.append(Paragraph(user.get_full_name(), styles['Normal']))
                elements.append(Paragraph(user, styles['Normal']))
            elements.append(PageBreak())

        doc.build(elements)#, onFirstPage=self._header_footer, onLaterPages=self._header_footer)

        # get the value os the BytesIO buffer and write in to the response.
        pdf = buffer.getvalue()
        buffer.close()
        return pdf

    def print_avisos(self, mandados):
        """
        :param mandados:
        :return:
        """
        from weasyprint import HTML, CSS
        from django.conf import settings
        av = Modelo_Documento.objects.get(nome='AVISO')

        modelo_html = ''
        for i in range(len(mandados)):
            if i == 0:                                          #primeiro aviso
                modelo_html += '<!DOCTYPE html>' \
                                  '<head>' \
                                  '<meta charset="utf-8" />' \
                                  '</head>' \
                                  '<body>' \
                                  '<div style="float: none;">' \
                                  '<div>'
                c = template.Context({'mandado':mandados[0]})
                t = template.Template(av.modelo)
                modelo_html += t.render(c)
                modelo_html += '</div>'
            else:                                               #avisos intermediarios
                modelo_html += '<div style="page-break-before:always;">'
                c = template.Context({'mandado':mandados[i]})
                t = template.Template(av.modelo)
                modelo_html += t.render(c).encode(encoding="UTF-8")
                modelo_html += '</div>'
        modelo_html += '</div></body>'
        print(modelo_html)
        '''
        options = {
            'page-size': 'A4',
            'margin-top': '0.75in',
            'margin-right': '0.75in',
            'margin-bottom': '0.75in',
            'margin-left': '1.25in',
        }
        pdfkit.from_string(modelo_html, 'out.pdf', options=options)
        pdf = open("out.pdf",'rb').read()
        os.remove("out.pdf")  # remove the locally created pdf file.
        '''
        pdf_file = HTML(string=modelo_html).write_pdf(stylesheets=[CSS(string='body { font-family: Arial }')])
        return pdf_file  # returns the response.



    ''' funciona com o pdfkit wkhtmltopdf
    def print_avisos(self, mandados):
        """
        :param mandados:
        :return:
        """
        import django.utils.html as hhtml
        av = Modelo_Documento.objects.get(nome='AVISO')

        modelo_html = ''
        for i in range(len(mandados)):
            if i == 0:                                          #primeiro aviso
                modelo_html += '<!DOCTYPE html>' \
                                  '<head>' \
                                  '<meta charset="utf-8" />' \
                                  '</head>' \
                                  '<body>' \
                                  '<div style="float: none;">' \
                                  '<div>'
                c = template.Context({'mandado':mandados[0]})
                t = template.Template(av.modelo)
                modelo_html += t.render(c)
                modelo_html += '</div>'
            else:                                               #avisos intermediarios
                modelo_html += '<div style="page-break-before:always;">'
                c = template.Context({'mandado':mandados[i]})
                t = template.Template(av.modelo)
                modelo_html += t.render(c)
                modelo_html += '</div>'
        modelo_html += '</div></body>'
        print(modelo_html)
        options = {
            'page-size': 'A4',
            'margin-top': '0.75in',
            'margin-right': '0.75in',
            'margin-bottom': '0.75in',
            'margin-left': '1.25in',
        }
        pdfkit.from_string(modelo_html, 'out.pdf', options=options)
        pdf = open("out.pdf",'rb').read()
        os.remove("out.pdf")  # remove the locally created pdf file.
        return pdf  # returns the response.

    '''
    '''antigo com reportlab
    def print_avisos(self, mandados):
        """

        :param diligencias: lista de diligencias com os documentos que devem ser impressos
        :return:arquivo pdf com os documentos
        """


        av = Modelo_Documento.objects.get(nome='AVISO')
        buffer = self.buffer
        doc = SimpleDocTemplate(buffer,
                                rightMargin=72,
                                leftMargin=72,
                                topMargin=72,
                                bottomMargin=72,
                                pagesize=self.pagesize)

        # Our container for 'Flowable' objects
        elements = []

        # A large collection of style sheets pre-made for us
        styles = getSampleStyleSheet()
        styles.add(ParagraphStyle(name='centered', alignment=TA_CENTER))

        # Draw things on the PDF. Here's where de PDF generation happens.
        # See the ReportLab documentation for the full list of functionality.
        #users = User.objects.all()
        for mandado in mandados:
            c = template.Context({'mandado':mandado})
            t = template.Template(html.unescape(av.modelo))
            modelo_html = t.render(c)
            print(modelo_html)
            parser = MyHTMLParser()
            parser.feed(modelo_html)
            documento = parser.list_data
            #elements.append(Paragraph('My User Names', styles['Heading1'],))
            for i, user in enumerate(documento):
                #elements.append(Paragraph(user.get_full_name(), styles['Normal']))
                elements.append(Paragraph(user, styles['Heading5'],))#, styles['Normal']))
            elements.append(PageBreak())

        doc.build(elements)#, onFirstPage=self._header_footer, onLaterPages=self._header_footer)

        # get the value os the BytesIO buffer and write in to the response.
        pdf = buffer.getvalue()
        buffer.close()
        return pdf
    '''



