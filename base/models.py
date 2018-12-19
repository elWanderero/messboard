from django.contrib.auth.models import AbstractUser, User as DjangoAuthUser
from django.db import models
from django.utils import timezone


# An extension of django auth's User, to be Used instead of that in this project
class User(AbstractUser):
    def __str__(self):
        return self.username

    #########################################
    #  Fields inherited from AbstractUser   #
    #########################################
    # username = models.CharField(…)
    # first_name = models.CharField(…)
    # last_name = models.CharField(…)
    # email = models.EmailField(…)
    # is_staff = models.BooleanField(…)
    # is_active = models.BooleanField(…)
    # date_joined = models.DateTimeField(…)

    ##########################################
    # Fields inherited from AbstractBaseUser #
    ##########################################
    # password = models.CharField(…)
    # last_login = models.DateTimeField(…)

    subscriptions = models.ManyToManyField("base.User", blank=True)
    date_activated = models.DateTimeField(blank=True, null=True)
    date_deactivated = models.DateTimeField(blank=True, null=True)
    public_key = models.CharField(max_length=178, blank=True, null=True)

    def subscription_usernames(self):
        return ", ".join(
            [user.username for user in self.subscriptions.only("username")])

    # class Meta(AbstractUser.Meta):
    #     swappable = 'AUTH_USER_MODEL'


class Message(models.Model):
    def __str__(self):
        txt: str = self.text.__str__()
        if len(txt) > 30:
            txt = txt[:27] + "..."
        return '{}'.format(txt)

    date_created = models.DateTimeField(default=timezone.now)
    text = models.TextField()
    date_updated = models.DateTimeField(blank=True)
    author = models.ForeignKey(User, models.DO_NOTHING)

    def save(self, *args, **kwargs):
        self.date_updated = timezone.now()
        super().save(*args, **kwargs)

    def get_absolute_url(self):
        return "messages/" + str(self.id)
        # return reversed("", args=[str(self.id)])

    class Meta:
        ordering = ["-date_created"]
