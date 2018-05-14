from django.contrib import admin

# Register your models here.

from .models import Choice, Question

# let's customize the admin (tut 7)

#it can look different ways!
#class ChoiceInline(admin.StackedInline):
class ChoiceInline(admin.TabularInline):
	model = Choice
	extra = 3

# follow this pattern -- create a model admin class, pass
# it as the second argument to admin.site.register() -- any
# time you need to change the admin options for a model

class QuestionAdmin(admin.ModelAdmin):
	#fields = ['pub_date', 'question_text']

	# let's split it up into fieldsets!
	fieldsets = [
		(None, 					{'fields': ['question_text']}),
		('Date information', 	{'fields': ['pub_date'], 'classes': ['collapse']}),
	]
	inlines = [ChoiceInline]

	#let's display more info from a question
	list_display = ('question_text', 'pub_date', 'was_published_recently')
	#let people filter by pub date
	list_filter = ['pub_date']

	#search!
	search_fields = ['question_text']

admin.site.register(Question, QuestionAdmin)

# Let's display the choices too!
# (Will display choices, but not as related to questions!)
# admin.site.register(Choice)