from django.urls import path , include
from myapp.views import LoginViews
from . import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [


   #path('index/',LoginViews.index_view, name='index_view'),
   path('signup',LoginViews.as_view()),
   path('login',LoginViews.as_view()),
]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)