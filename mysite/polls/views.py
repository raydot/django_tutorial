#from django.http import Http404
from django.shortcuts import get_object_or_404, render

#these are now farmed out to render
from django.http import HttpResponseRedirect, HttpResponse
#from django.template import loader

from django.urls import reverse

from .models import Choice, Question


def index(request):
	#return HttpResponse("Hello world!  Dave rules!  This is the polls index.")
	
	#you could code your pages here but then there wouldn't be a separation of concerns! 
	#the template lives at /template/polls/index.html
	latest_question_list = Question.objects.order_by('-pub_date')[:5]
	
	#2nd change, farming this out to render
	#template = loader.get_template('polls/index.html')
	#return HttpResponse(template.render(context, request))


	#1st change, use a template
	#output = ', '.join([q.question_text for q in latest_question_list])
	#return HttpResponse(output)
	
	context = {'latest_question_list': latest_question_list}
	return render(request, 'polls/index.html', context)


def detail(request, question_id):
	#changing this to throw a 404 if question not found
	#return HttpResponse("You're looking at question %s." % question_id)

	#another change, the try/except can be called with get_object_or_404()
	#try:
	#	question = Question.objects.get(pk=question_id)
	#except Question.DoesNotExist:
	#	raise Http404("Sorry, that question does not exist!")
	
	#what is
	question = get_object_or_404(Question, pk=question_id)

	return render(request, 'polls/detail.html', {'question': question})

def results(request, question_id):
	response = "You're looking at the results of question %s."
	return HttpResponse(response % question_id)

def vote(request, question_id):
	# placeholder
	# return HttpResponse("You're voting on question %s." % question_id)

	question = get_object_or_404(Question, pk=question_id)
	try: 
		selected_choice = question.choice_set.get(pk=request.POST['choice'])
	except (KeyError, Choice.DoesNotExist):
		#redisplay the question voting form
		return render(request, 'polls/detail.html', {
				'question': question,
				'error_message': "You didn't make a choice!",
			})
	else:
		selected_choice.votes += 1
		selected_choice.save()
		# Always return an HttpResponseRedirect after successfully dealing
		# with POST data.  This prevents data from being posted twice if the
		# user hits the back button.
		return HttpResponseRedirect(reverse('polls:results', args=(question.id,)))
