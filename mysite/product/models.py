from django.db import models
from django import forms
from wagtail.models import Page, Orderable
from wagtail.fields import RichTextField
from wagtail.admin.panels import FieldPanel, InlinePanel, MultiFieldPanel
from wagtail.search import index
from modelcluster.fields import ParentalKey, ParentalManyToManyField
from wagtail.snippets.models import register_snippet
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

class ProductIndexPage(Page):
    date = models.DateField("Post date", null=True)
    intro = RichTextField(blank=True)
    content_panels = Page.content_panels + [
        FieldPanel('intro'),
        FieldPanel('date'),
    ]
    
    
    def get_context(self, request):
        # Cập nhật ngữ cảnh để chỉ bao gồm các bài đăng đã xuất bản, được sắp xếp theo niên đại ngược
        context = super().get_context(request)
        blogpages = self.get_children().live().order_by('-first_published_at')

        # Sử dụng Paginator với 12 bài post mỗi trang
        paginator = Paginator(blogpages, 12)
        page = request.GET.get('page')

        try:
            blogpages = paginator.page(page)
        except PageNotAnInteger:
            # Nếu page không phải là một số nguyên, hiển thị trang đầu tiên
            blogpages = paginator.page(1)
        except EmptyPage:
            # Nếu page vượt quá số trang hiện có, hiển thị trang cuối cùng
            blogpages = paginator.page(paginator.num_pages)

        context['blogpages'] = blogpages
        return context
    

class ProductPage(Page):
    date = models.DateField("Post date")
    intro = models.CharField(max_length=250)
    image = models.ForeignKey(
        'wagtailimages.Image', null=True, blank=True,
        on_delete=models.SET_NULL, related_name='+'
    )
    body = RichTextField(blank=True, features=['h1', 'h2', 'h3', 'h5', 'h6', 'bold', 'italic', 'link', 'ol', 'ul', 'hr', 'document-link', 'image', 'embed', 'code', 'superscript', 'subscript', 'strikethrough', 'blockquote'])
    authors = ParentalManyToManyField('blog.Author', blank=True)
    def main_image(self):
        gallery_item = self.gallery_images.first()
        if gallery_item:
            return gallery_item.image
        else:
            return None
        
    search_fields = Page.search_fields + [
        index.SearchField('intro'),
        index.SearchField('body'),
    ]

    content_panels = Page.content_panels + [
        FieldPanel('date'),
        FieldPanel('image'),
        FieldPanel('intro'),
        FieldPanel('body', classname="full"),
    ]
    def get_context(self, request):
        # Gọi method gốc để lấy context
        context = super().get_context(request)

        # Lấy 10 bài viết gần nhất từ NewIndexPage (hoặc một logic tương tự)
        recent_posts = ProductPage.objects.live().order_by('-first_published_at')[:10]
        context['recent_posts'] = recent_posts

        return context
   