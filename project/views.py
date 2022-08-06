import datetime

from django.contrib.auth import authenticate, login
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import get_object_or_404, render
from django.urls import reverse, reverse_lazy
from django.utils import timezone
from django.views import generic

from .models import Question, TimeVoting


class IndexView(generic.ListView):
    template_name = "project/index.html"
    context_object_name = "latest_question_list"
    paginate_by = 7

    def get_queryset(self):
        days30 = timezone.now() - datetime.timedelta(days=30)
        if self.request.GET.get("select") == "date":
            return (
                Question.objects.filter(pub_date__lte=timezone.now()).filter(pub_date__gte=days30).order_by("pub_date")
            )
        elif self.request.GET.get("select") == "title":
            return (
                Question.objects.filter(pub_date__lte=timezone.now())
                .filter(pub_date__gte=days30)
                .order_by("question_title")
            )
        else:
            return (
                Question.objects.filter(pub_date__lte=timezone.now()).filter(pub_date__gte=days30).order_by("-pub_date")
            )


class DetailView(generic.DetailView):
    model = Question
    template_name = "project/detail.html"

    def get_queryset(self):
        return Question.objects.filter(pub_date__lte=timezone.now())


class ResultsView(generic.DetailView):
    model = Question
    template_name = "project/results.html"


class SignUpView(generic.CreateView):
    form_class = UserCreationForm
    success_url = reverse_lazy("index")
    template_name = "project/signup.html"

    # Переопределяю, для автоматической авторизации после регестрации
    def form_valid(self, form):
        valid = super(SignUpView, self).form_valid(form)
        username, password = form.cleaned_data.get("username"), form.cleaned_data.get("password1")
        new_user = authenticate(username=username, password=password)
        login(self.request, new_user)
        return valid


def vote(request, question_id):
    # Нахожу текущий Question
    question = get_object_or_404(Question, pk=question_id)

    # Если приходит запрос на удаление проверяю, что запрос POST и что он содержит 'delete-btn'
    if request.method == "POST" and "delete-btn" in request.POST and request.user == question.question_author:
        question.delete()
        return HttpResponseRedirect("/")

    # Проверка на аутентификацию
    if request.user.is_authenticated:
        try:
            time = TimeVoting.objects.get(
                users=request.user, question=question
            )  # Нахожу существующее время голосования
            time_current = timezone.now()  # Беру текущее время
            if (
                time_current - datetime.timedelta(days=1) < time.time_voting
            ):  # Из текущего вычитаю 1 день и смотрю меньше ли он чем время голосования
                return render(
                    request,
                    "project/detail.html",
                    {"question": question, "error_message": "Вы уже голосовали (голосовать можно раз в день)"},
                )
            else:
                # Если с момента последнего времени голосования прошло больше 1 дня, меняю время голосования
                time.time_voting = timezone.now()
                time.save()
        except (KeyError, TimeVoting.DoesNotExist):
            TimeVoting.objects.create(users=request.user, question=question, time_voting=timezone.now())

        selected_choice = question.choice_set.get(pk=request.POST["choice"])
        selected_choice.votes += 1
        selected_choice.save()
        return HttpResponseRedirect(reverse("results", args=(question.id,)))
    else:
        return HttpResponseRedirect(reverse("login"))


def add_quest(request):
    questions = Question.objects
    users = User.objects.all()

    if request.method == "POST" and request.user in users:
        form = request.POST

        # Вытаскиваю данные из формы в переменные
        title = form.get("question_title")
        text = form.get("question_text")
        author = request.user
        date = timezone.now()
        choice_arr = form.getlist("choice")

        questions.create(
            question_title=title, question_text=text, pub_date=date, question_author=author
        )  # Создания опроса
        questionNew = questions.get(question_title=title)  # Нахожу толькое что созданый запрос
        for item in choice_arr:
            questionNew.choice_set.create(choice_text=item, votes=0)  # Создаю варианты ответов

        return HttpResponseRedirect("/")
    else:
        form = request

    return render(request, "project/add.html", {"form": form})
