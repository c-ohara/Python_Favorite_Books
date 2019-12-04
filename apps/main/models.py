from __future__ import unicode_literals
from django.db import models
import re, bcrypt

class UserManager(models.Manager):
    def register_validator(self, postData):
        errors = {}
        email_check = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
        if len(postData['first_name']) < 2:
            errors['first_name'] = "First name must have at least 2 characters."
        if len(postData['last_name']) < 2:
            errors['last_name'] = "Last name must have at least 2 characters."
        if not email_check.match(postData['email']):
            errors['email'] = "Not a valid email address."
        elif User.objects.filter(email=postData['email']).all():
            errors['email'] = "Email address already in use."
        if postData['password'] != postData['pwcheck']:
            errors['password'] = "Password confirmation does not match."
        elif len(postData['password']) < 8:
            errors['password'] = "Password must be at least 8 characters."
        return errors
    
    def login_validator(self, postData):
        errors = {}
        if not User.objects.filter(email=postData["email"]).all():
            errors['email'] = "Account not found. Did you use a different email address?"
        elif not bcrypt.checkpw(postData["password"].encode(), User.objects.get(email=postData["email"]).password.encode()):
            errors["login"] = "Invalid email/password combination"
        return errors

    def add_book_validator(self, postData):
        errors = {}
        if len(postData['title']) < 2:
            errors['title'] = "Book Title needs at least 2 characters."
        if len(postData['description']) < 10:
            errors['description'] = "Description must have at least 10 characters."
        return errors

class User(models.Model):
    first_name = models.CharField(max_length=45)
    last_name = models.CharField(max_length=45)
    email = models.CharField(max_length=45)
    password = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add = True)
    updated_at = models.DateTimeField(auto_now = True)
    objects = UserManager()

class Book(models.Model):
    title = models.CharField(max_length = 255)
    description = models.TextField()
    uploaded_by = models.ForeignKey(User, related_name = "books")
    fave_users = models.ManyToManyField(User, related_name = "fave_books")
    created_at = models.DateTimeField(auto_now_add = True)
    updated_at = models.DateTimeField(auto_now = True)