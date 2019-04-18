from django.db import models
from django.contrib.auth.models import User
# from django.conf import settings.AUTH_USER_MODEL

# Create your models here.

class Profile(models.Model):
    user = models.OneToOneField(User,on_delete=models.CASCADE)
    birth_date = models.DateField(blank=True,null=True)
    photo = models.ImageField(upload_to="user/%Y/",blank=True)

    def __str__(self):
        return "{}profile".format(self.user.username)


class Contact(models.Model):
    #关注者
    user_from = models.ForeignKey(User,related_name="rel_from_set",on_delete=models.CASCADE)
    #被关注者
    user_to = models.ForeignKey(User,related_name="rel_to_set",on_delete=models.CASCADE,)
    created = models.DateTimeField(auto_now_add=True,db_index=True)

    class Meta:
        db_table = "contact"
        ordering = ("-created",)

    def __str__(self):
        return "{} follows {}".format(self.user_from,self.user_to)




