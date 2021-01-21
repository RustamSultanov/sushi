from django.db import models
from django.utils.translation import gettext_lazy as _
from wagtail.documents.models import Document
from wagtail.search import index


class Subjects(models.Model):
    (T_TEH_CARD, T_REGULATIONS, T_PROMOTIONS, T_BEFORE_OPEN,
     T_MENU, T_OTHER_MAKET, T_VIDEO, T_AUDIO,
     T_PERSONAL, T_PERSONAL_INVOICES, T_TRAINING) = range(11)
    STATUS_CHOICE = (
        (T_TEH_CARD, "Техкарты"),
        (T_REGULATIONS, "Регламенты"),
        (T_PROMOTIONS, "Акции"),
        (T_BEFORE_OPEN, "Перед открытием"),
        (T_MENU, "Меню"),
        (T_OTHER_MAKET, "Другие макеты"),
        (T_VIDEO, "Видеоролики"),
        (T_AUDIO, "Аудиоролики"),
        (T_PERSONAL, "Личные документы"),
        (T_PERSONAL_INVOICES, "Личные счета"),
        (T_TRAINING, "Обучение"),
    )

    name = models.CharField(max_length=255, blank=False, null=False,
                            verbose_name='Наименование')
    type = models.SmallIntegerField(choices=STATUS_CHOICE, default=T_TEH_CARD)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Тематика(папка)'
        verbose_name_plural = 'Тематики(папки)'


class DocumentSushi(Document):
    (T_TEH_CARD, T_REGULATIONS, T_PROMOTIONS, T_BEFORE_OPEN,
     T_MENU, T_OTHER_MAKET, T_VIDEO, T_AUDIO,
     T_PERSONAL, T_PERSONAL_INVOICES, T_TRAINING) = range(11)
    STATUS_CHOICE = (
        (T_TEH_CARD, "Техкарты"),
        (T_REGULATIONS, "Регламенты"),
        (T_PROMOTIONS, "Акции"),
        (T_BEFORE_OPEN, "Перед открытием"),
        (T_MENU, "Меню"),
        (T_OTHER_MAKET, "Другие макеты"),
        (T_VIDEO, "Видеоролики"),
        (T_AUDIO, "Аудиоролики"),
        (T_PERSONAL, "Личные документы"),
        (T_PERSONAL_INVOICES, "Личные счета"),
        (T_TRAINING, "Обучение"),
    )

    doc_type = models.IntegerField(choices=STATUS_CHOICE, default=T_TEH_CARD)
    sub_type = models.ForeignKey(Subjects, verbose_name='тематика',
                                 on_delete=models.CASCADE,
                                 related_name='documents',
                                 null=True,
                                 blank=True)

    search_fields = Document.search_fields + [
        index.SearchField('doc_type'),
        index.FilterField('doc_type'),
        index.FilterField('sub_type_id')
    ]

    @property
    def preview(self):
        path ='/static/icons_documents/'
        file_extension = self.file_extension.lower()

        if file_extension in ('jpg', 'svg', 'png', 'bmp'):
            return self.url

        if file_extension in ('doc', 'docx'):
            return f'{path}word.svg'
        elif file_extension in ('xls', 'xlsx'):
            return f'{path}excel.svg'
        else:
            return f'{path}{file_extension}.svg'


class DocumentPreview(models.Model):
    base_document = models.ForeignKey(DocumentSushi,
                                      on_delete=models.CASCADE)

    preview_title = models.CharField(max_length=255, verbose_name=_('preview_title'), default=None)
    preview_file = models.FileField(upload_to='document_previews', verbose_name=_('preview_file'), default=None)
