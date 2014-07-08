# -*- coding: utf-8 -*-

import uuid
from django.test import TestCase
from django.test.client import RequestFactory
from django.test.client import Client
from django.core.urlresolvers import reverse
from django.contrib.auth.models import User

from apps.sp.views.website.Home import HomeFormView


class HomeTest(TestCase):

    def setUp(self):
        self.request_factory = RequestFactory()
        self.client = Client()
        self.create_user()

    def create_user(self):
        self.user = User()
        self.user.username = 'testUser'
        self.user.set_password(uuid.uuid4().hex)
        self.user.email = 'testuser@gmail.com'
        self.user.save()

    def test_home_form_view(self):

        view = HomeFormView.as_view()
        request = self.request_factory.get(
            reverse('home')
        )
        request.user = self.user
        response = view(request)
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.get('location'), reverse('dashboard_view'))
