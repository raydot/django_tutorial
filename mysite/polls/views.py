#rewriting this to use generic views.  Roll back in Github to see the "long way"


from django.shortcuts import get_object_or_404, render
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.views import generic

from .models import Choice, Question


class IndexView(generic.ListView):
	template_name = 'polls/index.html'
	context_object_name = 'latest_question_list'

	def get_queryset(self):
		"""Return the last five published questions."""
		return Question.objects.order_by('-pub_date')[:5]


class DetailView(generic.DetailView):
	model = Question
	template_name = 'polls/detail.html'


class ResultsView(generic.DetailView):
	model= Question
	template_name = 'polls/results.html'


def vote(request, question_id):
	#what is difference between HttpResponse and HttpResponseRedirect?
	question = get_object_or_404(Question, pk=question_id)
	try:
		selected_choice = question.choice_set.get(pk=request.POST['choice'])
	except (KeyError, Choice.DoesNotExist):
		#redisplay the question voting form
		return render(request, 'polls/detail.html', {
			'question': question,
			'error_message': "You didn't select anything!",
		})
	else:
		selected_choice.votes += 1
		selected_choice.save()
		#always return an HttpResponseRedirect after successfully dealing
		#with POST data.  This prevents data from being posted twice if the
		#user hits the back button.
		return HttpResponseRedirect(reverse('polls:results', args=(question.id,)))