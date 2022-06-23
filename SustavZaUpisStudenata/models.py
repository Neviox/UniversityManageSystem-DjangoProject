from django.db import models
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager


class KorisniciManager(BaseUserManager):
    def create_user(self, email, password=None):
        if not email:
            raise ValueError("Users must have an email address")
        if not password:
            raise ValueError("Users must have a password")
        user_obj = self.model(
            email = self.normalize_email(email)
        )
        user_obj.set_password(password)
        #user_obj.Roles = Uloge.Titula
        user_obj.save(using=self._db)
        return user_obj
    
class Uloge(models.Model):
    
    class TitulaClass(models.TextChoices):
            ADMINISTRATOR = 'Administrator', _('Adminmistrator')
            PROFESOR = 'Profesor', _('Profesor')
            STUDENT = 'Student', _('Student')
            
    Titula = models.CharField(
    max_length=15,
    choices=TitulaClass.choices,
    default=TitulaClass.STUDENT,
)
    def __str__(self):
        return self.Titula
    
class Korisnici(AbstractBaseUser):
    Email = models.EmailField(max_length=255, unique=True, default="test@test.com")

    class StatusClass(models.TextChoices):
        NONE = 'None', _('None')
        REDOVNI = 'Redovni', _('Redovni')
        IZVANREDNI = 'Izvanredni', _('Izvanredni')
        
    Status = models.CharField(
        max_length=10,
        choices=StatusClass.choices,
        default=StatusClass.REDOVNI,
    )
    
    
    Roles = models.ForeignKey(Uloge, on_delete=models.CASCADE)
    
    
    USERNAME_FIELD = 'Email'
    # USERNAME_FIELD and password are required by default
    REQUIRED_FIELDS = []

    objects = KorisniciManager()
    
    def get_id(self):
        return self.id

    def get_status(self):
        return self.Status

    def get_name(self):
        return self.Email
   
    
    
class Predmeti(models.Model):
    Ime = models.CharField(max_length=255)
    Kod = models.CharField(max_length=16)
    Program = models.TextField()
    Bodovi = models.IntegerField()
    Sem_redovni = models.IntegerField()
    Sem_Izvanredni = models.IntegerField()
    
    
    NositeljKolegija = models.ForeignKey(Korisnici,on_delete=models.CASCADE,related_name='Nositelj',null=True)
    Upisni = models.ManyToManyField(Korisnici, through='Upisi')
    
    class Izborni(models.TextChoices):
        DA = 'Ne', _('Ne')
        NE = 'Da', _('Da')
        
    Izborni = models.CharField(
        max_length=10,
        choices=Izborni.choices,
        default=Izborni.NE
    )
    


    
    def __str__(self):
        return self.Ime

    def get_nositelj(self):
        return self.NositeljKolegija
    

class Upisi(models.Model):

    class Meta:
        unique_together = (('StudentID', 'PredmetID'),)

    StudentID = models.ForeignKey(Korisnici, on_delete=models.CASCADE)
    PredmetID = models.ForeignKey(Predmeti, on_delete=models.CASCADE)
    
    class Status(models.TextChoices):
        UPISAN = 'Upisan', _('Upisan')
        POLOZEN = 'Polozen', _('Polozen')
        IZGUBIO_POTPIS = 'Izgubio potpis', _('Izgubio potpis')
        NIJE_UPISAN = 'Nije upisan', _('Nije upisan')
        
    Status = models.CharField(
        max_length=15,
        choices=Status.choices,
        default=Status.UPISAN
    )

    def __str__(self):
        return self.Status
    
    def get_studentID(self):
        return self.StudentID
    
    def get_predmetID(self):
        return self.PredmetID


