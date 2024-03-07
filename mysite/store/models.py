from django.db import models
from wagtail.models import Page
from wagtail.admin.panels import FieldPanel
class StoreIndexPage(Page):
    date = models.DateField("Post date", null=True)
    content_panels = Page.content_panels + [
        FieldPanel('date'),
    ]