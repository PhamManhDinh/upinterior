from django.db import models
from wagtail.models import Page
from wagtail.admin.panels import FieldPanel
from blog.models import BlogIndexPage
from new.models import NewIndexPage
from product.models import ProductIndexPage

class ServiceIndexPage(Page):
    date = models.DateField("Post date", null=True)
    content_panels = Page.content_panels + [
        FieldPanel('date'),
    ]
    def get_context(self, request):
        context = super().get_context(request)
        url_new_index = NewIndexPage.objects.live()[0]
        url_blog_index = BlogIndexPage.objects.live()[0]
        url_product_index = ProductIndexPage.objects.live()[0]
        context['url_blog_index'] = url_blog_index
        context['url_new_index'] = url_new_index
        context['url_product_index'] = url_product_index
        return context

class Registration(models.Model):
    username = models.CharField(max_length=100)
    email = models.EmailField()
    number_phone = models.CharField(max_length=15)
    support = models.CharField(max_length=100)
    message = models.TextField()


class CustomerInquiry(models.Model):
    full_name = models.CharField(max_length=100)
    email = models.EmailField()
    phone_number = models.CharField(max_length=20)
    service_request = models.CharField(max_length=200)
    message = models.TextField()

    def __str__(self):
        return self.full_name