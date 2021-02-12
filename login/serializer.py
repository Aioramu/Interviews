from rest_framework import serializers
from .models import Question,Choice,SpecId


class QuestionSerializer(serializers.ModelSerializer):
    choices=serializers.StringRelatedField(many=True)
    class Meta:
        model= Question
        fields = ('pk','qtext','pub_date','choices')
