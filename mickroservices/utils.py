from django.conf import settings
from django.core.mail import EmailMessage
# from django.contrib.sites.models import Site
from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string

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

        output_dir, output_name = path.split(output_path)

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


