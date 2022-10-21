from django.conf.urls.static import static
from django.conf import settings
from django.contrib import admin
from django.urls import path

from general import views as general


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', general.main, name='main'),
    path('sheet/', general.sheet, name='sheet'),
    path('signin/', general.signin, name='signin'),
    path('signup/', general.signup, name='signup'),
    path('signout/', general.signout, name='signout'),
    path('create_persone/', general.create_persone, name='create_persone'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
