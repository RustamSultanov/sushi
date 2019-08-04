from django.db import models
from wagtail.search import index
from wagtail.documents.models import Document

class DocumentSushi(Document):
    T_TEH_CARD, T_REGULATIONS = range(2)
    STATUS_CHOICE = (
        (T_TEH_CARD, "Техкарты"),
        (T_REGULATIONS, "Регламенты"),
    )

    doc_type = models.IntegerField(choices=STATUS_CHOICE, default=T_TEH_CARD)

    search_fields = Document.search_fields +[
        index.SearchField('doc_type'),
        index.FilterField('doc_type'),
    ]


