from django.urls import path

from . import views

question_list = views.QuestionViewSet.as_view({'get': 'list'})
question_detail = views.QuestionViewSet.as_view({'get': 'retrieve'})

urlpatterns = [
    path('questions/', question_list, name='question-list'),
    path('questions/<int:pk>/', question_detail, name='question-detail'),
    path('', view=views.quiz, name='quiz'),

]
