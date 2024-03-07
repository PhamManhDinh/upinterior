from .models import ZaloChatWidget

def zalo_chat_widget(request):
    zalo_chat_widget = ZaloChatWidget.objects.first()
    return {'zalo_chat_widget': zalo_chat_widget}