from django.urls import path

from translations import views

app_name = 'translations'

urlpatterns = [
    path('', views.TranslationIndexCreateApiView.as_view(), name='translations_index_create'),
    path('<int:pk>', views.TranslationRetrieveUpdateApiView.as_view(), name='translations_retrieve_update'),
]
