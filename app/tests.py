from django.test import TestCase, Client
from django.utils import timezone
from django.urls import reverse
from django.contrib.auth.models import User

import datetime
from .models import Snippet, Tag

def create_snippet(**info):
    time = timezone.now()
    return Snippet.objects.create(**info, pub_date=time)

# testing account
USER, PASS = 'testuser', 'pass6974'

class IndexViewTests(TestCase):
    def test_page_no_login(self):
        response = self.client.get(reverse('app:index'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Welcome to Recall, a programming tool that allows you to store snippets of code along with short explanations.')
    def test_page_login(self):
        self.credentials = {
            'username': USER,
            'password': PASS
        }
        User.objects.create_user(**self.credentials)
        response = self.client.post('/accounts/login/', self.credentials, follow=True)
        self.assertTrue(response.context['user'].is_authenticated)

        response = self.client.get(reverse('app:index'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Add new snippet')

class TagDetailViewTests(TestCase):
    def setUp(self):
        self.credentials = {
            'username': USER,
            'password': PASS
        }
        self.user = User.objects.create_user(**self.credentials)
    def test_deletion_of_tag_does_not_delete_snippets(self):
        # create snippets
        code = '''
        (defun doors (n)
            (loop for a from 1 to n collect
                (zerop (mod (sqrt a) 1))))
        '''

        tags = [
            Tag.objects.create(tag_type='algorithms', user=self.user),
            Tag.objects.create(tag_type='functional', user=self.user),
        ]

        snip = create_snippet(
            user=self.user,
            code=code,
            language='lisp',
            title='doors problem',
            description='doors problem in lisp',
            starred=True,
        )

        for tag in tags:
            snip.tags.add(tag)

        tags[0].delete()
        self.assertEqual(Snippet.objects.all().count(), 1)
        tags[1].delete()
        self.assertEqual(Snippet.objects.all().count(), 1)

class LoginTest(TestCase):
    def setUp(self):
        self.credentials = {
            'username': USER,
            'password': PASS
        }
        User.objects.create_user(**self.credentials)
    def test_login(self):
        response = self.client.post('/accounts/login/', self.credentials, follow=True)
        self.assertTrue(response.context['user'].is_authenticated)

class SettingsViewTest(TestCase):
    def setUp(self):
        self.credentials = {
            'username': USER,
            'password': PASS
        }
        self.user = User.objects.create_user(**self.credentials)
    def test_user_deletion(self):
        response = self.client.post('/accounts/login/', self.credentials, follow=True)
        self.assertTrue(response.context['user'].is_authenticated)

        response = self.client.post(reverse('app:settings'), self.credentials, follow=True)
        self.assertEquals(response.status_code, 200)
        self.assertFalse(response.context['user'].is_active)

"""
def create_question(question_text, days):
    time=timezone.now()+datetime.timedelta(days=days)
    return Question.objects.create(question_text=question_text, pub_date=time)

class QuestionIndexViewTests(TestCase):
    def test_no_questions(self):
        response=self.client.get(reverse('polls:index'))
        self.assertEqual(response.status_code,200)
        self.assertContains(response, 'No polls are available.')
        self.assertQuerysetEqual(response.context['latest_question_list'],[])
    def test_past_question(self):
        question=create_question('Past question.', days=-30)
        response=self.client.get(reverse('polls:index'))
        self.assertQuerysetEqual(response.context['latest_question_list'], [question],)
    def test_future_question(self):
        create_question(question_text='Future question.', days=30)
        response = self.client.get(reverse('polls:index'))
        self.assertContains(response, 'No polls are available.')
        self.assertQuerysetEqual(response.context['latest_question_list'], [])
    def test_future_question_and_past_question(self):
        future=create_question(question_text='Future question.', days=30)
        past=create_question(question_test='Past question.', days=-30)
        response = self.client.get(reverse('polls:index'))
        self.assertQuerysetEqual(response.context['latest_question_list'], [past])
    def test_two_past_questions(self):
        past1 = create_question(question_text='Past question 1.', days=-30)
        past2 = create_question(question_text='Past question 2.', days=-21)
        response = self.client.get(reverse('polls:index'))
        self.assertQuerysetEqual(response.context['latest_question_list'], [past1, past2])

class QuestionModelTests(TestCase):
    def test_was_published_recently_with_future_question(self):
        '''
        was_published_recently() returns False for questions whose pub_date is in the future
        '''
        time = timezone.now() + datetime.timedelta(days=30)
        future_question = Question(pub_date=time)

        self.assertIs(future_question.was_published_recently(), False)

    def test_was_published_recently_with_old_question(self):
        time=timezone.now()
        datetime.timedelta(days=1, seconds=1)
        old_question = Question(pub_date=time)
        self.assertIs(old_question.was_published_recently(), False)

    def test_was_published_recently_with_recent_question(self):
        datetime.timedelta(hours=23, minutes=59, seconds=59)
        recent_question = Question(pub_date=timezone.now())
        self.assertIs(recent_question.was_published_recently(), True)

class QuestionDetailViewTests(TestCase):
    def test_future_question(self):
        future_question = create_question(question_text='Future question.', days=5)
        url=reverse('polls:detail', args=(future_question.id,))
        response=self.client.get(url)
        self.assertEqual(response.status_code,404)
    def test_past_question(self):
        past_question = create_question(question_text='Past question.', days=-5)
        url=reverse('polls:detail', args=(past_question.id,))
        response=self.client.get(url)
        self.assertContains(response, past_question.question_text)
"""