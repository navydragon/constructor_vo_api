from django.db import models
from django.contrib.auth.models import AbstractUser

USER = 'user'
MODERATOR = 'moderator'
ADMIN = 'admin'

POSSIBLE_ROLES = [
    (USER, USER),
    (ADMIN, ADMIN)
]
