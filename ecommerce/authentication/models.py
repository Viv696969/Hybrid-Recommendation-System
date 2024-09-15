from django.db import models
from django.contrib.auth.models import User
from django.contrib.postgres.fields import ArrayField

class Profile(models.Model):
    user=models.OneToOneField(User,on_delete=models.CASCADE)
    name=models.CharField(max_length=200,blank=False,null=False)
    mobile=models.CharField(max_length=20,blank=False,null=False)
    activity=ArrayField(models.IntegerField(),size=5,default=list)

    def __str__(self) -> str:
        return self.user.username
    
    def add_item_id(self,item_id):
        if len(self.activity)==5: #activity is full
            self.activity.pop(0)
        self.activity.append(item_id)

    



