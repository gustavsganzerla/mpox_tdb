from django.urls import path
from . import views
from .views import CSSRQueryView, ISSRQueryView, SSRQueryView, VNTRQueryView

urlpatterns = [
        path('home/', views.home, name='home'),
        path('query/', views.query, name='query'),
        path('api/cssr/', CSSRQueryView.as_view(), name='cssr-query'),
        path('api/issr/', ISSRQueryView.as_view(), name='issr-query'),
        path('api/ssr/', SSRQueryView.as_view(), name='ssr-query'),
        path('api/vntr/', VNTRQueryView.as_view(), name='vntr-query'),
        path('download/sequence/', views.download, name='download-sequence'),
        path('autocomplete/', views.autocomplete, name='autocomplete'),
        path('faq/', views.faq, name='faq'),
        path('resources/', views.resources, name='resources'),
        path('api_documentation/', views.api_documentation, name='api_documentation'),
        path('contact/', views.contact, name='contact')
]
