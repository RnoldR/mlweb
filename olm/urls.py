from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name = 'index'),
    path('docs/', views.DocListView.as_view(), name = 'docs'),
    path('docs/<int:pk>', views.DocDetailView.as_view(), name = 'doc-detail'),
]
