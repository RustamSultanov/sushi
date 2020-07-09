from django.db import models
from wagtail.search import index
from wagtail.documents.models import Document

class Subjects(models.Model):
    (T_TEH_CARD, T_REGULATIONS, T_PROMOTIONS, T_BEFORE_OPEN,
     T_MENU, T_OTHER_MAKET, T_VIDEO, T_AUDIO,
     T_PERSONAL, T_PERSONAL_INVOICES, T_TRAINING)  = range(11)
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
     T_PERSONAL, T_PERSONAL_INVOICES, T_TRAINING)  = range(11)
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
    sub_type =  models.ForeignKey(Subjects, verbose_name='тематика',
                                  on_delete=models.CASCADE,
                                  related_name='documents',
                                  null=True,
                                  blank=True)

    search_fields = Document.search_fields +[
        index.SearchField('doc_type'),
        index.FilterField('doc_type'),
        index.FilterField('sub_type_id')
    ]

    @property
    def preview(self):
        path ='/media/icons_documents/'

        if self.file_extension == 'jpg' or\
            self.file_extension == 'svg' or\
            self.file_extension == 'png' or\
            self.file_extension == 'bmp':
            return self.url

        if self.file_extension == 'doc' or\
            self.file_extension == 'docx':
            return f'{path}word.svg'

        if self.file_extension == 'xls' or\
            self.file_extension == 'xlsx':
            return f'{path}excel.svg'

        if self.file_extension == 'pdf':
            return f'{path}pdf.svg'

        if self.file_extension == 'ppt':
            return f'{path}ppt.svg'
        if self.file_extension == 'cdr':
            return f'{path}cdr.svg'
        if self.file_extension == 'ai':
            return f'{path}ai.svg'
