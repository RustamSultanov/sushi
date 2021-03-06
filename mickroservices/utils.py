from django.conf import settings
from django.core.mail import EmailMessage
# from django.contrib.sites.models import Site
from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string
from mickroservices.consts import CONVERT_TO_PDF_EXTENSIONS
from mickroservices.models import DocumentPreview

import logging
from subprocess import call
from os import path, rename


def send_message(template, ctx, subject, to_email, request=None,
                 from_email=settings.DEFAULT_FROM_EMAIL):
    '''Отправка электронных писем'''
    if request:
        current_site = get_current_site(request)
        domain = current_site.domain
    else:
        domain = settings.DEFAULT_DOMAIN

    ctx.update({'protocol': settings.DEFAULT_PROTOCOL, 'domain': domain})
    message = render_to_string(template, ctx)
    if isinstance(to_email, str):
        to_email = [to_email]
    msg = EmailMessage(subject=subject, body=message,
                       to=to_email,
                       from_email=from_email)
    msg.content_subtype = 'html'
    try:
        msg.send()
    except Exception as e:
        print('There was an error sending an email: ', e)
        logging.error('Ошибка отправки письма . Причина: %s', str(e), exc_info=True)
        return e



class FileConverter:

    def __init__(self):
        self.convert_funcs = {
            ('docx', 'pdf') : self.convert_docx_to_pdf,
            ('doc', 'pdf') : self.convert_docx_to_pdf,
            ('ppt', 'pdf') : self.convert_ppt_to_pdf,
            ('pptx', 'pdf') : self.convert_pptx_to_pdf,
            ('xls', 'pdf') : self.convert_excel_to_pdf,
            ('xlsx', 'pdf') : self.convert_excel_to_pdf,
        }

    def convert(self, type_a, type_b, path_a, path_b):
        ''' Возвращает True в случае успеха '''

        key = (type_a, type_b)
        if key in self.convert_funcs:
            return self.convert_funcs[key](path_a, path_b)

        return False
    
    def _libre_convert(self, target_type, source_path, output_path):
        command = ['libreoffice', '--headless', 
                   '--convert-to', target_type, source_path]

        output_dir = path.dirname(output_path)

        try:
            success = call(command, cwd=output_dir) == 0
            if success:
                src_name_without_ext = path.splitext(path.split(source_path)[1])[0]
                real_output_name = '.'.join([src_name_without_ext, target_type])
                real_path = path.join(output_dir, real_output_name)
                rename(real_path, output_path)
                return success

        except Exception as e:
            return False
        
    def convert_docx_to_pdf(self, source_path, output_path):
        return self._libre_convert('pdf', source_path, output_path)

    def convert_ppt_to_pdf(self, source_path, output_path):
        return self._libre_convert('pdf', source_path, output_path)

    def convert_pptx_to_pdf(self, source_path, output_path):
        return self._libre_convert('pdf', source_path, output_path)

    def convert_excel_to_pdf(self, source_path, output_path):
        return self._libre_convert('pdf', source_path, output_path)




def generate_doc_preview(doc):
    try:
        _generate_doc_preview(doc)
    except Exception as e:
        pass

        
def _generate_doc_preview(doc):
    filename = doc.file.name
    media_preview_path = path.join(settings.MEDIA_ROOT, 'document_previews/')
    source_path = path.join(settings.MEDIA_ROOT, filename)
    ext = filename.split('.')[-1].lower()
    
    available_types = CONVERT_TO_PDF_EXTENSIONS

    if ext == 'pdf':
        return 

    if ext in available_types:
        target_filename = path.split(filename)[1]
        target_filename = target_filename.split('.')[0] + '_preview.pdf'
        target_path = path.join(media_preview_path, target_filename)
        relative_target_path = path.join('document_previews/', target_filename)
        converter = FileConverter()
        if converter.convert(ext, 'pdf', source_path, target_path):
            preview = DocumentPreview(preview_file=relative_target_path,
                                      preview_title=target_filename,
                                      base_document=doc)

            preview.save()

