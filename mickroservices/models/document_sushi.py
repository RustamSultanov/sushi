from django.db import models
from wagtail.search import index
from wagtail.documents.models import Document

class DocumentSushi(Document):
    (T_TEH_CARD, T_REGULATIONS, T_STOCK, T_BEFORE_OPEN,
    T_MENU, T_OTHER_MAKET, T_VIDEO, T_AUDIO)  = range(8)
    STATUS_CHOICE = (
        (T_TEH_CARD, "Техкарты"),
        (T_REGULATIONS, "Регламенты"),
        (T_STOCK, "Акции"),
        (T_BEFORE_OPEN, "Перед открытием"),
        (T_MENU, "Меню"),
        (T_OTHER_MAKET, "Другие макеты"),
        (T_VIDEO, "Видеоролики"),
        (T_AUDIO, "Аудиоролики"),
    )

    doc_type = models.IntegerField(choices=STATUS_CHOICE, default=T_TEH_CARD)

    search_fields = Document.search_fields +[
        index.SearchField('doc_type'),
        index.FilterField('doc_type'),
    ]


