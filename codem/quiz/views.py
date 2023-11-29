from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.http import HttpResponse
from .models import Quiz, UserProfile
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.views.generic import ListView


# Create your views here.
def quiz(request):
    # Assuming you want 10 quizzes per page, adjust as needed
    quizzes_per_page = 1

    result_range = [
        (0, 2, "You are an excellent social person and you spend time with your community.\n "
               "Continue at this level and make sure that you are with good people who are supporting to you."),
        (3, 5, "You are vulnerable to social isolation, and to avoid it, you must work to organize your time.\n "
               "Watch this video about time management"),
        ]
    if request.method == 'POST':
        import pdb; pdb.set_trace()
        user_name = request.POST.get('name')
        total_score = 0

        # Get or create UserProfile for the provided username
        user, created = User.objects.get_or_create(username='VIVEK'.lower())
        user_profile, created = UserProfile.objects.get_or_create(user=user)

        # Delete previous quiz responses for the user
        Quiz.objects.filter(user=user).delete()

        for question_id, response in request.POST.items():
            if question_id.startswith('question_'):
                try:
                    # get the question instance and save with updated response
                    question_instance = Quiz.objects.get(pk=int(question_id.split('_')[1]))
                    question_instance.response = response
                    question_instance.save()

                    total_score += int(response)

                except Quiz.DoesNotExist:
                    pass

        # Handle the case where the question doesn't exist
        user_profile.total_score = total_score
        user_profile.save()

        # Determine the result based on total_score
        result = get_result(total_score, result_range)
        return render(request, 'quiz_results.html', {'result': result})
        # return redirect('quiz_results')
        return HttpResponse("The view is processed successfully")

    # Fetch all the questions from Quiz order by id
    quizzes = Quiz.objects.all().order_by('id')

    # Paginate the quizzes
    paginator = Paginator(quizzes, quizzes_per_page)
    page = request.GET.get('page', 1)

    try:
        quizzes = paginator.page(page)
    except PageNotAnInteger:
        quizzes = paginator.page(1)
    except EmptyPage:
        quizzes = paginator.page(paginator.num_pages)

    return render(request, 'quiz.html', {'quizzes': quizzes})


def get_result(total_score, result_range):
    for start, end, result_text in result_range:
        if start <= total_score <= end:
            return result_text
    return "No result found"  # Handle the case where the total_score doesn't fall into any range
