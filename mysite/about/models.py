from django.db import models
from django import forms
from wagtail.models import Page, Orderable
from wagtail.fields import RichTextField
from wagtail.admin.panels import FieldPanel, InlinePanel, MultiFieldPanel
from wagtail.search import index
from modelcluster.fields import ParentalKey, ParentalManyToManyField
from wagtail.snippets.models import register_snippet
from django.shortcuts import redirect
from product.models import ProductPage
from wagtail.snippets.models import register_snippet

@register_snippet
class ZaloChatWidget(models.Model):
    chat_code = models.TextField()

    def __str__(self):
        return "Zalo Chat Widget"

class AboutIndexPage(Page):
    date = models.DateField("Post date", null=True)
    intro = RichTextField(blank=True)
    image = models.ForeignKey(
        'wagtailimages.Image', null=True, blank=True,
        on_delete=models.SET_NULL, related_name='+'
    )
    content_panels = Page.content_panels + [
        FieldPanel('intro'),
        FieldPanel('image'),
        FieldPanel('date'),
        InlinePanel('founder_gallery_images', label="Founder images"),
        InlinePanel('customer_gallery_images', label="Customer images"),
    ]
    def get_context(self, request):
        # Cập nhật ngữ cảnh để chỉ bao gồm các bài đăng đã xuất bản, được sắp xếp theo niên đại ngược
        context = super().get_context(request)
        blogpages = self.get_children().live() #.order_by('-first_published_at')
        context['blogpages'] = blogpages
        return context

class FounderPageGalleryImage(Orderable):
    page = ParentalKey(AboutIndexPage, on_delete=models.CASCADE, related_name='founder_gallery_images')
    position = models.CharField(max_length=250, blank=True, null=True)
    image = models.ForeignKey(
        'wagtailimages.Image', on_delete=models.CASCADE, related_name='+'
    )
    caption = models.TextField()
    panels = [
        FieldPanel('image'),
        FieldPanel('position'),
        FieldPanel('caption'),
    ]

class CustomerPageGalleryImage(Orderable):
    page = ParentalKey(AboutIndexPage, on_delete=models.CASCADE, related_name='customer_gallery_images')
    position = models.CharField(max_length=250, blank=True, null=True)
    image = models.ForeignKey(
        'wagtailimages.Image', on_delete=models.CASCADE, related_name='+'
    )
    caption = models.TextField()
    panels = [
        FieldPanel('image'),
        FieldPanel('position'),
        FieldPanel('caption'),
    ]

class PartnerIndexPage(Page):
    date = models.DateField("Post date", null=True)
    intro = RichTextField(blank=True)
    image = models.ForeignKey(
        'wagtailimages.Image', null=True, blank=True,
        on_delete=models.SET_NULL, related_name='+'
    )
    content_panels = Page.content_panels + [
        FieldPanel('intro'),
        FieldPanel('image'),
        FieldPanel('date'),
    ]
    def get_context(self, request):
        # Cập nhật ngữ cảnh để chỉ bao gồm các bài đăng đã xuất bản, được sắp xếp theo niên đại ngược
        context = super().get_context(request)
        newproduct = ProductPage.objects.live().order_by('-first_published_at')[:3]
        blogpages = self.get_children().live() #.order_by('-first_published_at')
        # Lấy ra danh sách CustomerPageGalleryImage
        try:
            about_page = AboutIndexPage.objects.get(id=self.get_parent().specific.id)
            customer_gallery_images = about_page.customer_gallery_images.all()
        except AboutIndexPage.DoesNotExist:
            customer_gallery_images = []
        context['blogpages'] = blogpages
        context['newproduct'] = newproduct
        context['customer_gallery_images'] = customer_gallery_images
        return context

class SiteSettings(models.Model):
    chat_code = RichTextField()

    panels = [
        FieldPanel('chat_code'),
    ]

    class Meta:
        abstract = True