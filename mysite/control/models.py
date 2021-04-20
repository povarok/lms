# !/usr/bin/python
# -*- coding: utf-8 -*-

from polls.models import *
from django.contrib.postgres.fields import JSONField
from django.contrib.auth.models import User

from django.http import HttpResponseRedirect, Http404, HttpResponse
from django.db import models
from account.models import Account

class ControlTest(TrainingTest):
    is_control = models.BooleanField(default=True, editable=False)


class TestGroupConstructor(models.Model):
    name = models.CharField(u'название', max_length=255)
    tests = models.ManyToManyField(TrainingApparatus, related_name='groups', verbose_name=u'тесты')
    order = models.PositiveIntegerField()
    active = models.BooleanField(default=False)

class UserTestGroup(models.Model):
    user = models.ForeignKey(Account, verbose_name=u"Пользователь",
                             on_delete=models.CASCADE, default=None, blank=True, null=True)
    constructor = models.ForeignKey(TestGroupConstructor, verbose_name=u'Группа',
                                    on_delete=models.CASCADE, default=None, blank=True, null=True)

    @property
    def is_complete(self):
        is_complete = False
        tests = ControlTest.objects.filter(user=self.user, apparatus__groups__id__exact=self.constructor.id).filter(grade__gte=3)
        apparatus_set = set(tests.values_list('apparatus', flat=True))
        if self.constructor.active and len(apparatus_set) == self.constructor.tests.all().count(): #сделать set(values_list) по тренажерам всесто первого
            is_complete = True
            for test in tests:
                if test.grade is not None and test.grade < 3:

                    is_complete = False
        return is_complete


