from django.contrib.auth.models import User
from django.db.models import Choices
from django.http import HttpResponse
from django.shortcuts import render
from rest_framework import viewsets
import re
from .models import Quiz, UserProfile, Question, Option
from .serializers import QuestionSerializer


class QuestionViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Question.objects.all().order_by('pk')
    serializer_class = QuestionSerializer


# Create your views here.
def quiz(request):
    result_range = [
        (0, 2, "You are an excellent social person, and you spend time with your community."
               "Continue at this level and make sure that you are with good people who are supporting to you."),
        (3, 5, "You are vulnerable to social isolation, and to avoid it, you must work to organize your time."
               "Watch this video about time management- https://youtu.be/VpQn48MV1Js?si=Tmi2p3O93svbBn6U"),
        (6, 8, "You are socially isolated, and this could be due to personal reasons."
               "You must know the importance of public relations at university and that it also benefits you after "
               "university. "
               "Watch this video on how to develop your relationship with those around you - "
               "https://youtu.be/lB2mmk-kirc?si=kZ2fZUrvzHJPWBVK"),
        (9, 20,
         "You are a socially isolated person, and this could be due to psychological reasons such as stress or the "
         "onset of depression "
         "You can contact the psychologists at the university and request advice from them. You can get an "
         "appointment via this link.- https://irshad.kfupm.edu.sa/ar/refer-himself")
    ]
    if request.method == 'POST':
        # import pdb; pdb.set_trace()
        user_name = request.POST.get('name')
        total_score = 0

        # Get or create UserProfile for the provided username
        user, created = User.objects.get_or_create(username=user_name or 'VIVEK'.lower())
        user_profile, created = UserProfile.objects.get_or_create(user=user)

        # Delete previous quiz responses for the user
        Quiz.objects.filter(user=user).delete()

        for question_id, response in request.POST.items():
            if question_id.startswith('question_'):
                try:
                    # get the question instance and save with updated response
                    question = Question.objects.get(pk=int(question_id.split('_')[1]))

                    quiz_instance = Quiz(question=question, response_id=response, user=user)
                    quiz_instance.save()

                    total_score += int(quiz_instance.response.value)

                except Quiz.DoesNotExist:
                    pass

        # Handle the case where the question doesn't exist
        user_profile.total_score = total_score
        user_profile.save()

        # Determine the result based on total_score
        result = get_result(total_score, result_range)

        context = {'result': result}
        # import pdb; pdb.set_trace()
        https_link_match = re.search(r'https://[^\s]+', result)
        https_link = https_link_match.group() if https_link_match else None

        if https_link and 'youtu.be' in https_link:
            context['https_link'] = https_link
            context['word_suggestion'] = 'watch the video'
        else:
            context['https_link'] = https_link
            context['word_suggestion'] = 'open this link'

        # split results and get the bold words and join the username
        list_of_words = result.split(",")
        bold_words, other_words = list_of_words[0], list_of_words[1]
        bold_words = user_name + ' ' + bold_words

        context['bold_words'] = bold_words
        context['other_words'] = other_words

        return render(request, 'quiz_results.html', context)

    return render(request, 'quiz2.html', {})


def get_result(total_score, result_range):
    for start, end, result_text in result_range:
        if start <= total_score <= end:
            return result_text
    return "No result found"  # Handle the case where the total_score doesn't fall into any range
