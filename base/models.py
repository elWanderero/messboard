from django.db import models


class User(models.Model):
    def __str__(self):
        return self.name

    name = models.CharField(unique=True, max_length=32)
    created = models.DateTimeField(auto_now_add=True)
    deactivated = models.DateTimeField(blank=True, null=True)
    active = models.BooleanField()
    public_key = models.CharField(max_length=178, blank=True, null=True)
    email = models.CharField(max_length=40, blank=True, null=True)

    class Meta:
        managed = True
        db_table = "user"


class Message(models.Model):
    def __str__(self):
        txt: str = self.text.__str__()
        if len(txt) > 20:
            txt = txt[:17] + "..."
        return '{} "{}"'.format(self.id, txt)

    created = models.DateTimeField(auto_now_add=True)
    text = models.TextField()
    updated = models.DateTimeField(auto_now=True)
    # db_column="createdby" option to force column
    # name, default adds _id for foreign keys
    createdby = models.ForeignKey(User, models.DO_NOTHING, related_name="username")

    class Meta:
        managed = True
        db_table = "message"
