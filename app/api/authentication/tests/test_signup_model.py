from django.test import TestCase
from django.contrib.auth import get_user_model

from datetime import datetime, timedelta
import jwt
import pytest
from model_bakery import baker

from app import settings


USER_MODEL = get_user_model()


class TestUserModel(TestCase):
    def setUp(self):
        super(TestUserModel, self).setUp()

    def test_create_user(self):
        email = "email@test.com"
        username = "test_user"
        user = USER_MODEL.objects.create_user(
            email=email,
            username=username,
            password="Pass@123",
            first_name="Test",
            last_name="User",
        )
        assert user

    def test_create_super_user(self):
        email = "email@test.com"
        username = "test_user"
        user = USER_MODEL.objects.create_superuser(
            password="Pass@123",
            email=email,
            username=username,
            first_name="Test",
            last_name="User",
        )
        assert user.is_staff is True
        assert user.is_superuser is True

    def test_user_str(self):
        user = baker.make(
            USER_MODEL,
            email="email@test.com",
            username="test_user",
            first_name="Test",
            last_name="User",
        )
        assert str(user) == "email@test.com"

    def test_token(self):
        user = baker.make(
            USER_MODEL,
            email="email@test.com",
            username="test_user",
            password="Pass@123",
            first_name="Test",
            last_name="User",
        )
        token = user.token
        assert isinstance(token, str)

        decoded = jwt.decode(token, settings.SECRET_KEY, algorithms="HS256")
        assert decoded["email"] == user.email
        assert decoded["username"] == user.username
        assert decoded["id"] == user.id
        assert "exp" in decoded

    def test_no_token(self):
        user = USER_MODEL(email="test@user.com")
        if not user.email or not user.username or not user.pk:
            return None
        with pytest.raises(Exception):
            user.token
