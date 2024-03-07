from django.db import models
from wagtail.models import Page, Orderable
from wagtail.fields import RichTextField
from wagtail.admin.panels import FieldPanel, InlinePanel
from wagtail.admin.rich_text.editors import draftail
from wagtail import hooks
from blog.models import BlogIndexPage
from new.models import NewPage, NewIndexPage
from modelcluster.fields import ParentalKey

class HomePage(Page):
    body = RichTextField(blank=True)
        
    content_panels = Page.content_panels + [
        FieldPanel('body'),
        InlinePanel('home_gallery_images', label="Gallery images"),
    ]
    
    def get_context(self, request):
        context = super().get_context(request)
        newblog = NewPage.objects.live().order_by('-first_published_at')[:6]
        url_new_index = NewIndexPage.objects.live()[0]
        url_blog_index = BlogIndexPage.objects.live()[0]
        context['new_blog'] = newblog
        context['url_blog_index'] = url_blog_index
        context['url_new_index'] = url_new_index
        return context
    
class HomePageGalleryImage(Orderable):
    page = ParentalKey(HomePage, on_delete=models.CASCADE, related_name='home_gallery_images')
    #title = models.CharField(blank=True, max_length=250)
    image = models.ForeignKey(
        'wagtailimages.Image', on_delete=models.CASCADE, related_name='+'
    )
    caption = models.CharField(blank=True, max_length=250)

    panels = [
        FieldPanel('image'),
        FieldPanel('caption'),
    ]