from rest_framework import serializers

from .models import Quiz, Question, Option


class OptionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Option
        fields = "__all__"


class QuestionSerializer(serializers.ModelSerializer):
    choices = OptionSerializer(source='options', many=True, read_only=True)

    class Meta:
        model = Question
        fields = ('id', 'description', 'choices')


class QuizSerializer(serializers.ModelSerializer):
    class Meta:
        model = Quiz
        fields = "__all__"
