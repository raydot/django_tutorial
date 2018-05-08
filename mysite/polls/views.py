#from django.shortcuts import render

# Create your views here.
from django.http import HttpResponse
from django.template import loader

from .models import Question


def index(request):
	#return HttpResponse("Hello world!  Dave rules!  This is the polls index.")
	
	#you could code your pages here but then there wouldn't be a separation of concerns! 
	#the template lives at /template/polls/index.html
	latest_question_list = Question.objects.order_by('-pub_date')[:5]
	template = loader.get_template('polls/index.html')
	#output = ', '.join([q.question_text for q in latest_question_list])
	context = {
		'latest_question_list': latest_question_list,
	}
	#return HttpResponse(output)
	return HttpResponse(template.render(context, request))

def detail(request, question_id):
	return HttpResponse("You're looking at question %s." % question_id)

def results(request, question_id):
	response = "You're looking at the results of question %s."
	return HttpResponse(response % question_id)

def vote(request, question_id):
	return HttpResponse("You're voting on question %s." % question_id)
