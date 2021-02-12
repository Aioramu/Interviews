from django.db import models

# Create your models here.
from django.db import models


class Question(models.Model):
     qtext = models.CharField(max_length=200)
     pub_date = models.DateTimeField('date published')

     def __str__(self):
        return self.qtext

class Choice(models.Model):
    question = models.ForeignKey(Question,  related_name='choices',on_delete=models.CASCADE)
    ctext = models.CharField(max_length=200)
    votes = models.IntegerField(default=0)
    class Meta:
        unique_together = ['ctext', 'votes']
    def __str__(self):
        return '%s: %d' % (self.ctext, self.votes)

class SpecId(models.Model):
    choice=models.ForeignKey(Choice,on_delete=models.CASCADE)
    user_id=models.IntegerField(default=0)
    class Meta:
        unique_together = ['choice', 'user_id']
    def __str__(self):
        return str(self.id)
