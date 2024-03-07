from django.db import models
from django import forms
from wagtail.models import Page, Orderable
from wagtail.fields import RichTextField
from wagtail.admin.panels import FieldPanel, InlinePanel, MultiFieldPanel
from wagtail.search import index
from modelcluster.fields import ParentalKey, ParentalManyToManyField
from wagtail.snippets.models import register_snippet
from django.shortcuts import redirect
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

class BlogIndexPage(Page):
    date = models.DateField("Post date", null=True)
    intro = RichTextField(blank=True)
    content_panels = Page.content_panels + [
        FieldPanel('intro'),
        FieldPanel('date'),
    ]
    def get_context(self, request):
        # Cập nhật ngữ cảnh để chỉ bao gồm các bài đăng đã xuất bản, được sắp xếp theo niên đại ngược
        '''context = super().get_context(request)
        blogpages = self.get_children().live() #.order_by('-first_published_at')
        context['blogpages'] = blogpages
        # Lấy 10 bài viết mới nhất của BlogPage
        blog_posts = BlogPage.objects.live().order_by('-date')[:10]
        context['blog_posts'] = blog_posts
        return context'''
        context = super().get_context(request)
        
        # Lấy tất cả các bài đăng của trang con, sắp xếp theo ngày đăng mới nhất
        blogpages = self.get_children().live() #.order_by('-first_published_at')
        context['blogpages'] = blogpages
        blog_posts = BlogPage.objects.live().order_by('-first_published_at')
        # Phân trang
        page = request.GET.get('page')
        paginator = Paginator(blog_posts, 18)  # Số bài viết trên mỗi trang là 10
        try:
            blog_posts = paginator.page(page)
        except PageNotAnInteger:
            blog_posts = paginator.page(1)
        except EmptyPage:
            blog_posts = paginator.page(paginator.num_pages)
        
        context['blog_posts'] = blog_posts
        return context
    
class BlogIndexTwoPage(Page):
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
        context['blogpages'] = blogpages
        # Lấy tất cả các trang con cùng cấp với trang hiện tại
        sibling_pages = self.get_siblings().live()
        context['sibling_pages'] = sibling_pages
        # Lấy trang cha của trang hiện tại
        context['parent_page'] = self.get_parent()
        # Xác định trang đang được hiển thị
        context['active_page'] = self.get_url()
         # Sử dụng Paginator với 16 bài post mỗi trang
        paginator = Paginator(blogpages, 18)
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
   
class BlogPage(Page):
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
   
class BlogPageGalleryImage(Orderable):
    page = ParentalKey(BlogPage, on_delete=models.CASCADE, related_name='gallery_images')
    image = models.ForeignKey(
        'wagtailimages.Image', on_delete=models.CASCADE, related_name='+'
    )
    caption = models.CharField(blank=True, max_length=250)

    panels = [
        FieldPanel('image'),
        FieldPanel('caption'),
    ]
    
@register_snippet
class Author(models.Model):
    name = models.CharField(max_length=255)
    author_image = models.ForeignKey(
        'wagtailimages.Image', null=True, blank=True,
        on_delete=models.SET_NULL, related_name='+'
    )

    panels = [
        FieldPanel('name'),
        FieldPanel('author_image'),
    ]

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = 'Authors'