import datetime

from django.test import TestCase
from django.urls import reverse
from django.utils import timezone

from .models import Question


class QuestionModelTests(TestCase):
    def test_was_published_recently_with_future_question(self):
        time = timezone.now() + datetime.timedelta(days=30)
        future_question = Question(pub_date=time)
        self.assertIs(future_question.was_published_recently(), False)

    def test_was_published_recently_with_old_question(self):
        time = timezone.now() - datetime.timedelta(days=1, seconds=1)
        old_question = Question(pub_date=time)
        self.assertIs(old_question.was_published_recently(), False)

    def test_was_published_recently_with_recent_question(self):
        time = timezone.now() - datetime.timedelta(hours=23, minutes=59)
        recent_question = Question(pub_date=time)
        self.assertIs(recent_question.was_published_recently(), True)


def create_question(question_text, days, question_title):
    time = timezone.now() + datetime.timedelta(days=days)
    return Question.objects.create(question_text=question_text, pub_date=time, question_title=question_title)


class QuestionIndexViewTests(TestCase):
    def test_no_questions(self):
        response = self.client.get("/")
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "No project are available.")
        self.assertQuerysetEqual(response.context["latest_question_list"], [])

    def test_past_question(self):
        question = create_question(question_text="Past question", days=-30, question_title="Paste")
        response = self.client.get("/")
        self.assertQuerysetEqual(response.context["latest_question_list"], [question])

    def test_future_question(self):
        create_question(question_text="Future question.", days=30, question_title="Future")
        response = self.client.get("/")
        self.assertContains(response, "No project are available.")
        self.assertQuerysetEqual(response.context["latest_question_list"], [])

    def test_future_question_and_past_question(self):
        question = create_question(question_text="Past question", days=-30, question_title="Paste")
        create_question(question_text="Future question.", days=30, question_title="Future")
        response = self.client.get("/")
        self.assertQuerysetEqual(response.context["latest_question_list"], [question])

    def test_two_past_questions(self):
        question1 = create_question(question_text="Past question 1", days=-30, question_title="Paste1")
        question2 = create_question(question_text="Past question 2", days=-30, question_title="Paste2")
        response = self.client.get("/")
        self.assertQuerysetEqual(response.context["latest_question_list"], [question1, question2])


class QuestionDetailViewTests(TestCase):
    def test_future_question(self):
        future_question = create_question(question_text="Future question", days=5, question_title="Future")
        url = reverse("/", args=(future_question.id,))
        response = self.client.get(url)
        self.assertEqual(response.status_code, 404)

    def test_past_question(self):
        past_question = create_question(question_text="Post question", days=-5, question_title="Post")
        url = reverse("/", args=(past_question.id,))
        response = self.client.get(url)
        self.assertContains(response, past_question.question_text)
