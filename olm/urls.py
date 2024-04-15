from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name = 'index'),
    path('docs/', views.DocListView.as_view(), name = 'docs'),
    path('docs/<int:pk>', views.DocDetailView.as_view(), name = 'doc-detail-view'),
    path('persons/', views.PersonListView.as_view(), name = 'persons'),
    path('persons/<int:pk>', views.PersonDetailView.as_view(), name = 'person-detail-view'),
    path('conversations/', views.ConversationListView.as_view(), name = 'conversations'),
    path('conversations/<int:pk>', views.ConversationDetailView.as_view(), name = 'conversation-detail-view'),
]
