rom django.db import models

class User(models.Model):
    firstname = models.CharField(max_length=30)
    lastname = models.CharField(max_length=50)
    country = models.CharField(max_length=50)
    email = models.EmailField(max_length=50)
    phone = models.CharField(max_length=30)
    password = models.CharField(max_length=128)
    GENDER_CHOICES = (
        ('M', 'Male'),
        ('F', 'Female'),
        ('X', 'X')
        )
    gender = models.CharField(max_length=1, choices= GENDER_CHOICES)
    conjoint = models.OneToOneField('self', on_delete=models.CASCADE, blank= True, null=True)
    def __str__(self):
        return self.firstname+' '+self.lastname

class Message(models.Model):
    author = models.ForeignKey('User', on_delete=models.CASCADE)
    content = models.TextField()
    publication_date = models.DateField(null=True)
    def __str__(self):
        if len(self.content) > 20:
            return self.content[:19] + "..."
        else:
            return self.content

class Friend(models.Model):
    adding = models.EmailField(max_length=50) 
    added = models.EmailField(max_length=50)
    def __str__(self):
        return self.adding
