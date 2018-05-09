from django.urls import path

from . import views

# what if there are other apps with similar path names?
# no problem, add a namespace!:

#does the namespace break the app?
app_name = 'polls'

urlpatterns = [
	#REFORMATTED TO USE GENERIC VIEWS.  ROLL BACK TO SEE EXPLICIT DECLARATIONS
	# ex: /polls/
	path('', views.IndexView.as_view(), name='index'),
	path('<int:pk>/', views.DetailView.as_view(), name='detail'),
	path('<int:pk>/results/', views.ResultsView.as_view(), name='results'),
	path('<int:question_id>/vote/', views.vote, name='vote'), 
]