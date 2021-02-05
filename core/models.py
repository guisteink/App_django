from django.db import models
from django.contrib.auth.models import User
from django.db import IntegrityError

# Create your models here.
class Pessoa(models.Model):
    nome = models.CharField(max_length=100)
    sobrenome = models.CharField(max_length=100)
    apelido = models.CharField(max_length=100)
    idade = models.CharField(max_length=100)
    data_nascimento = models.CharField(max_length=100)
    email = models.EmailField()
    observacao = models.TextField()
    created_at = models.DateField(auto_now_add=True)
    
    # user = models.OneToOneField(User, on_delete=models.CASCADE, blank=True)
    user = models.ForeignKey(User, null=True, on_delete=models.CASCADE)

    def __str__(self):
        return str(self.id)

    class Meta: 
        db_table = "pessoa"
