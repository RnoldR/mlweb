from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name = 'index'),
    path('llms/',    views.LLMListView.as_view(),    name = 'llms'),
    path('persons/', views.PersonListView.as_view(), name = 'persons'),
    path('docs/',    views.DocListView.as_view(),    name = 'docs'),
    path('llms/<int:pk>',    views.LLMDetailView.as_view(),    name = 'llm-detail-view'),
    path('persons/<int:pk>', views.PersonDetailView.as_view(), name = 'person-detail-view'),
    path('docs/<int:pk>',    views.DocDetailView.as_view(),    name = 'doc-detail-view'),

    path('trainedllms/', views.TrainedLLMListView.as_view(), name = 'trainedllms'),
    path('trainedllms/<int:pk>', views.TrainedLLMDetailView.as_view(), name = 'trainedllm-detail-view'),
    path('conversations/', views.ConversationListView.as_view(), name = 'conversations'),
    path('conversations/<int:pk>', views.ConversationDetailView.as_view(), name = 'conversation-detail-view'),
    path('statements/', views.StatementListView.as_view(), name = 'statements'),
    path('statements/<int:pk>', views.StatementDetailView.as_view(), name = 'statement-detail-view'),

    path('trainedllm/id:pk>/train', views.train_llm, name = 'train_llm')
]
