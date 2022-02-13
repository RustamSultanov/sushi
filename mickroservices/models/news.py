from django.db import models
from django.urls import reverse
from django.db.models import Q

from wagtail.core.models import Page
from wagtail.core.fields import RichTextField
from wagtail.admin.edit_handlers import FieldPanel
from wagtail.images.edit_handlers import ImageChooserPanel


class NewsPage(Page):
    image = models.ForeignKey(
        'wagtailimages.Image',
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='+'
    )
    preview = RichTextField(blank=True)
    body = RichTextField(blank=True)
    announcement = models.TextField(blank=True)

    content_panels = Page.content_panels + [
        FieldPanel('body', classname="full"),
        ImageChooserPanel('image'),
    ]

    class Meta:
        verbose_name = "Новости"

    @classmethod
    def get_live(cls):
        return cls.object.filter(
            Q(live=True) & Q(go_live_at=None) | Q(go_live_at__lt=timezone.now())
        )

    def get_context(self, request):
        context = super(NewsPage, self).get_context(request)
        context['breadcrumb'] = [
            {'title': 'Новости',
             'url': reverse('mickroservices:news')},
            {'title': self.title}
        ]
        return context
