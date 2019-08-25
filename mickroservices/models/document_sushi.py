from django.db import models
from wagtail.search import index
from wagtail.documents.models import Document

class DocumentSushi(Document):
    (T_TEH_CARD, T_REGULATIONS, T_PROMOTIONS, T_BEFORE_OPEN,
     T_MENU, T_OTHER_MAKET, T_VIDEO, T_AUDIO,
     T_PERSONAL, T_PERSONAL_INVOICES)  = range(10)
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
    )

    doc_type = models.IntegerField(choices=STATUS_CHOICE, default=T_TEH_CARD)

    search_fields = Document.search_fields +[
        index.SearchField('doc_type'),
        index.FilterField('doc_type'),
    ]


