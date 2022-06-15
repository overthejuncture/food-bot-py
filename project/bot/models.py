from django.db import models

class Choise(models.Model):
    text = models.CharField(max_length=200)
    active = models.BooleanField(default = True)
    users = models.ManyToManyField('User', through="ChoiseUser")

    def __str__(self):
        return self.text

class User(models.Model):
    telegram_id = models.TextField()
    choises = models.ManyToManyField('Choise', through="ChoiseUser")

    def __str__(self):
        return "{id} {telegram_id}".format(id=self.id, telegram_id=self.telegram_id)

class ChoiseUser(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    choise = models.ForeignKey(Choise, on_delete=models.CASCADE)

    def __str__(self) -> str:
        return "{user_id} {choise_id}".format(self.user_id, self.choise_id)