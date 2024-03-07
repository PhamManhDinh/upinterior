from wagtail.images.formats import Format, register_image_format
from django.utils.html import format_html

class CaptionedImageFormat(Format):
    def __init__(self, name, label, classnames, class_bootstrap, width_percent, height_percent):
        super().__init__(name, label, classnames, filter_spec="width-750")
        self.class_bootstrap = class_bootstrap
        self.width_percent = width_percent
        self.height_percent = height_percent

    def image_to_html(self, image, alt_text, extra_attributes=None):

        default_html = super().image_to_html(image, alt_text, extra_attributes)
        # Thêm thuộc tính style để đặt chiều rộng theo %
        style_attribute = f"width: {self.width_percent}; height: {self.height_percent}"
        #default_html = format_html(default_html.replace('<img', f'<img style="width: 100%; height: 100%;"'))
        default_html = format_html(default_html.replace('<img ', f'<img class="{self.class_bootstrap}" style="{style_attribute}" '))
        return format_html('{}<figcaption class="text-center">{}</figcaption>', default_html, alt_text)

register_image_format(
    CaptionedImageFormat('captioned_fullwidth', 'Width 100%, height auto', 'bodytext-image', class_bootstrap="rounded", width_percent='100%', height_percent='auto')
)
register_image_format(
    CaptionedImageFormat('captioned_fullwidth1', 'Width 50%, height auto, float left', 'bodytext-image', class_bootstrap="rounded float-start", width_percent='50%', height_percent='auto')
)
register_image_format(
    CaptionedImageFormat('captioned_fullwidth2', 'Width 50%, height auto, float right', 'bodytext-image', class_bootstrap="rounded float-end", width_percent='50%', height_percent='auto')
)
register_image_format(
    CaptionedImageFormat('captioned_fullwidth3', 'Width 50%, height auto, float center', 'bodytext-image', class_bootstrap="rounded mx-auto d-block", width_percent='50%', height_percent='auto')
)
register_image_format(
    CaptionedImageFormat('captioned_fullwidth4', 'Width 80%, height auto, float left', 'bodytext-image', class_bootstrap="rounded float-start", width_percent='80%', height_percent='auto')
)
register_image_format(
    CaptionedImageFormat('captioned_fullwidth5', 'Width 80%, height auto, float right', 'bodytext-image', class_bootstrap="rounded float-end", width_percent='80%', height_percent='auto')
)
register_image_format(
    CaptionedImageFormat('captioned_fullwidth6', 'Width 80%, height auto, float center', 'bodytext-image', class_bootstrap="rounded mx-auto d-block", width_percent='80%', height_percent='auto')
)
register_image_format(
    CaptionedImageFormat('captioned_fullwidth7', 'Width 90%, height auto, float left', 'bodytext-image', class_bootstrap="rounded float-start", width_percent='90%', height_percent='auto')
)
register_image_format(
    CaptionedImageFormat('captioned_fullwidth8', 'Width 90%, height auto, float right', 'bodytext-image', class_bootstrap="rounded float-end", width_percent='90%', height_percent='auto')
)
register_image_format(
    CaptionedImageFormat('captioned_fullwidth9', 'Width 90%, height auto, float center', 'bodytext-image', class_bootstrap="rounded mx-auto d-block", width_percent='90%', height_percent='auto')
)
register_image_format(Format('thumbnail', 'Thumbnail', 'richtext-image thumbnail', 'max-100x120'))
