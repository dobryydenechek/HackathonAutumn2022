from django.conf.urls.static import static
from django.conf import settings
from django.contrib import admin
from django.urls import path

from general import views as general


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', general.main, name='main'),
    path('annalysis/<int:pk>/', general.analysis, name='analysis'),
    path('signin/', general.signin, name='signin'),
    path('signup/', general.signup, name='signup'),
    path('signout/', general.signout, name='signout'),
    path('persone_list/', general.persone_list, name='persone_list'),
    path('create_persone/', general.create_persone, name='create_persone'),
    path('persone_delete/<int:pk>/', general.persone_delete, name='persone_delete'),
    path('persone_view/<int:pk>/', general.persone_view, name='persone_view'),
    path('upload_pcap/', general.upload_pcap, name='upload_pcap'),
    path('package_delete/', general.package_delete, name='package_delete'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
