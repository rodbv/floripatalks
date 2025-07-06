# create a textchoice for vote up and down and use on talkvote model

from django.db import models


class VoteChoices(models.IntegerChoices):
    UP = 1, "Up"
    DOWN = -1, "Down"
