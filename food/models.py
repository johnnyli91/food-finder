# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone


class Restaurant(models.Model):
    name = models.CharField(max_length=200, null=True)
    street_address = models.CharField(max_length=1000, null=True)
    city = models.CharField(max_length=200, null=True)
    state = models.CharField(max_length=100, null=True)
    zip_code = models.CharField(max_length=100, null=True)
    phone_number = models.CharField(max_length=100, null=True)
    image = models.URLField(null=True)
    place_id = models.CharField(max_length=100)

    def __unicode__(self):
        return self.name


class Result(models.Model):
    user = models.ForeignKey(User)
    restaurant = models.ForeignKey(Restaurant)
    result_date = models.DateField(default=timezone.now)
    rating = models.IntegerField(null=True)

    def __unicode__(self):
        return "{} - {}".format(self.user.username, self.restaurant.name)
