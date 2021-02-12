from django.shortcuts import render,get_object_or_404
from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework import status
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.http import HttpResponse
from .models import Question,Choice,SpecId
from .serializer import *

# Create your views here.
def index(request):
    latest_question_list = Question.objects.order_by('-pub_date')[:5]
    output = ', '.join([q.qtext for q in latest_question_list])
    return HttpResponse(output)

def results(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    return HttpResponse(response % question)


@api_view(['GET','POST'])
def vote(request):
    if request.method=='GET':
        data=[]
        nextPage = 1
        previousPage = 1
        questions = Question.objects.all()
        choises = Choice.objects.all()
        page = request.GET.get('page', 1)
        paginator = Paginator(questions, 10)
        try:
            data = paginator.page(page)
        except PageNotAnInteger:
            data = paginator.page(1)
        except EmptyPage:
            data = paginator.page(paginator.num_pages)
        #data=Question.objects.order_by('-pub_date')
        qserializer=QuestionSerializer(data,context={'request': request} ,many=True)
        if data.has_next():
            nextPage = data.next_page_number()
        if data.has_previous():
            previousPage = data.previous_page_number()

        return Response({'data': qserializer.data, 'count': paginator.count, 'numpages' : paginator.num_pages, 'nextlink': '/api/questions/?page=' + str(nextPage), 'prevlink': '/api/questions/?page=' + str(previousPage)})
@api_view(['GET','POST'])
def send_vote(request):
    if request.method=='POST':
        question = get_object_or_404(Question, pk=request.data['question'])
        selected_choice = question.choices.get(ctext=request.data['choice'])
        uid=selected_choice.specid_set.create(user_id=request.data['uid'])
        selected_choice.votes += 1
        selected_choice.save()

        return Response({'data':selected_choice.votes})
    return Response({'data':0})
@api_view(['GET','POST'])
def see_vote(request):
    asd=[]
    if request.method=='POST':
        uid=request.data['uid']
        id=SpecId.objects.all()
        for i in id:
            if i.user_id==uid:
                print(i.choice)
                choice=get_object_or_404(Choice,ctext=i.choice.ctext)
                question=get_object_or_404(Question,qtext=choice.question)
                print(question,choice)
                asd.append({'question':{'pk':int(question.pk),'qtext':str(question)},'choice':str(choice.ctext)})
        #return Response({'data':{'question':{
        #'pk':int(question.pk),'qtext':str(question)},'choice':str(choice.ctext)}})
        return Response({'data':asd})
