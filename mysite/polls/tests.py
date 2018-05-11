import datetime

from django.utils import timezone
from django.test import TestCase
from django.urls import reverse

from .models import Question

class QuestionModelTests(TestCase):
	def test_was_published_recently_with_future_question(self):
		"""
		was_published_recently() returns False for questions
		whose pub_date is in the future
		"""
		time = timezone.now() + datetime.timedelta(days=30)
		future_question = Question(pub_date=time)
		self.assertIs(future_question.was_published_recently(), False)

	# adding two more test methods to the same class, to test the behavior
	# of the method more comprehensively
	def test_was_published_recently_with_old_question(self):
		"""
		was_published_recently() returns False for questions whose 
		pub_date is older than one day
		"""
		time = timezone.now() - datetime.timedelta(days=1, seconds=1)
		old_question = Question(pub_date=time)
		self.assertIs(old_question.was_published_recently(), False)

	def test_was_published_recently_with_recent_question(self):
		"""
		was_published_recently() returns True for questions whose 
		pub_date is within the last day
		"""
		time = timezone.now() - datetime.timedelta(hours=23, minutes=59, seconds=59)
		recent_question = Question(pub_date=time)
		self.assertIs(recent_question.was_published_recently(), True)

def create_question(question_text, days):
	""" 
	Create a question with the given 'question text' and published the
	given number of 'days' offset to now (negative for past, positive for future)
	This function is used in the tests that follow.

	"In effect, we are using the tests to tell a story of admin 
	input and user experience on the site, and checking that at 
	every state and for every new change in the state of the system, 
	the expected results are published."
	"""
	time = timezone.now() + datetime.timedelta(days=days)
	return Question.objects.create(question_text=question_text, pub_date=time)

class QuestionIndexViewTests(TestCase):
	def test_no_questions(self):
		""" If no questions exists, display message """
		response = self.client.get(reverse('polls:index'))
		self.assertEqual(response.status_code, 200)
		self.assertContains(response, "No polls are available.")
#this doesn't look right!
self.assertQuerysetEqual(response.context['latest_question_list'], [])

	def test_past_question(self):
		"""
		Questions with a pub_date in the past are displayed on the index page
		"""
		create_question(question_text="Past question.", days=-30)
		response = self.client.get(reverse('polls:index'))
		self.assertQuerysetEqual(
			['latest_question_list'], ['<Question: Past question.>']
		)

	def test_future_question(self):
		"""
		Questions with a pub_date in the future aren't displayed
		on the index page.
		"""
		create_question(question_text="Future question.", days=30)
		response = self.client.get(reverse('polls:index'))
		self.assertContains(response,"No polls are available.")

self.assertQuerysetEqual(response.context['latest_question_list'], [])

def test_two_past_questions(self):
	"""
	The questions index page may display multiple questions.
	"""
	create_question(question_text="Past question 1.", days=-30)
	create_question(question_text="Past question 2.", days=-5)
	response = self.client.get(reverse('polls:index'))
	self.assertQuerysetEqual(
		response.content['latest_question_list'], 
		['<Question: Past question 2.>', '<Question: Past question 1.>']
	)
