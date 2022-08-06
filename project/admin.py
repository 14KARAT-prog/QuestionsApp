from django.contrib import admin

from .models import Choice, Question, TimeVoting


class ChoiceInline(admin.TabularInline):
    model = Choice
    extra = 1


class QuestionAdmin(admin.ModelAdmin):
    fieldsets = [
        ("Questions information", {"fields": ["question_title", "question_text", "question_author"]}),
        ("Date information", {"fields": ["pub_date"]}),
    ]
    inlines = [ChoiceInline]
    list_display = ("question_title", "pub_date", "was_published_recently")
    list_filter = ["pub_date"]
    search_fields = ["question_title"]


admin.site.register(Question, QuestionAdmin)
admin.site.register(TimeVoting)
