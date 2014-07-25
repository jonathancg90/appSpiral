# -*- coding: utf-8 -*-

import uuid
from mock import patch
from django.test import TestCase
from django.test.client import RequestFactory
from django.test.client import Client
from django.core.urlresolvers import reverse
from django.contrib.auth.models import User
from django.contrib.messages.storage.fallback import FallbackStorage
from django.contrib.sessions.backends.db import SessionStore

from apps.sp.views.website.Home import HomeFormView, RegisterUser


class HomeTest(TestCase):

    def setUp(self):
        self.request_factory = RequestFactory()
        self.client = Client()
        self.password = uuid.uuid4().hex
        self.session = SessionStore()
        self.create_user()

    def create_user(self):
        self.user = User()
        self.user.username = 'testUser'
        self.user.set_password(self.password)
        self.user.email = 'testuser@gmail.com'
        self.user.save()

    def test_home_form_view_not_logged(self):
        view = HomeFormView.as_view()
        request = self.request_factory.get(
            reverse('home')
        )
        request.user = self.user
        response = view(request)
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.get('location'), reverse('dashboard_view'))


    @patch('django.contrib.auth.models.AbstractBaseUser.is_authenticated')
    def test_home_form_view_logger(self, mock_is_authenticated):
        mock_is_authenticated.return_value = False

        view = HomeFormView.as_view()
        request = self.request_factory.get(
            reverse('home')
        )
        request.user = self.user
        response = view(request)
        self.assertEqual(response.status_code, 200)

    def test_home_form_login(self):
        data = {
            'username': 'testUser',
            'password': self.password
        }

        view = HomeFormView.as_view()
        request = self.request_factory.post(
            reverse('home'), data
        )
        request.user = self.user
        setattr(request, 'session',  self.session)
        response = view(request)
        self.assertEqual(response.status_code, 302)

    def test_home_form_login_fail(self):
        data = {
            'username': 'testUser',
            'password': 'fail'
        }

        view = HomeFormView.as_view()
        request = self.request_factory.post(
            reverse('home'), data
        )
        request.user = self.user
        setattr(request, 'session',  self.session)
        setattr(request, '_messages', FallbackStorage(request))
        response = view(request)
        self.assertEqual(response.status_code, 200)

    def test_register_model(self):
        data = {
            'username': 'newUser',
            'password': self.password,
            'email': 'new@gmail.com'
        }
        view = RegisterUser.as_view()
        request = self.request_factory.post(
            reverse('register_user'), data
        )
        response = view(request)
        user = User.objects.filter(username='newUser').exists()
        self.assertEqual(response.status_code, 302)
        self.assertEqual(user, True)

    def test_register_model_duplicate_username(self):
        data = {
            'username': 'testUser',
            'password': self.password,
            'email': 'new@gmail.com'
        }
        view = RegisterUser.as_view()
        request = self.request_factory.post(
            reverse('register_user'), data
        )
        setattr(request, 'session',  self.session)
        setattr(request, '_messages', FallbackStorage(request))
        response = view(request)
        user = User.objects.filter(username='newUser').exists()
        self.assertEqual(response.status_code, 302)
        self.assertEqual(user, False)

    def test_register_model_duplicate_email(self):
        data = {
            'username': 'otherUser',
            'password': self.password,
            'email': 'testuser@gmail.com'
        }
        view = RegisterUser.as_view()
        request = self.request_factory.post(
            reverse('register_user'), data
        )
        setattr(request, 'session',  self.session)
        setattr(request, '_messages', FallbackStorage(request))
        response = view(request)
        user = User.objects.filter(username='newUser').exists()
        self.assertEqual(response.status_code, 302)
        self.assertEqual(user, False)

