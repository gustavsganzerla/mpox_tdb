from django.db import models

# Create your models here.
class BaseSequence(models.Model):
    sequence = models.CharField(max_length=100)
    motif = models.CharField(max_length=100)
    start = models.IntegerField()
    end = models.IntegerField()
    length = models.IntegerField()
    clade = models.CharField(max_length=25)

    class Meta:
        abstract = True



class CSSR(BaseSequence):
    #	complexity	gap	component	structure
    complexity = models.IntegerField()
    gap = models.IntegerField()
    component = models.CharField(max_length=50)
    structure = models.CharField(max_length=50)

    def __str__(self):
        return f"{self.sequence}, {self.clade}, {self.length}, {self.motif}"

class ISSR(BaseSequence):
    #standard		type				match	subsitution	insertion	deletion	score
    standard = models.CharField(max_length=50)
    type = models.IntegerField()
    match = models.IntegerField()
    subsitution = models.IntegerField()
    insertion = models.IntegerField()
    deletion = models.IntegerField()
    score = models.IntegerField()

    def __str__(self):
        return f"{self.sequence}, {self.clade}, {self.length}, {self.motif}"
    


class SSR(BaseSequence):
    standard = models.CharField(max_length=50)
    type = models.IntegerField()
    repeat = models.IntegerField()

    def __str__(self):
        return f"{self.sequence}, {self.clade}, {self.length}, {self.motif}"
    

class VNTR(BaseSequence):
    type = models.IntegerField()
    repeat = models.IntegerField()

    def __str__(self):
        return f"{self.sequence}, {self.clade}, {self.length}, {self.motif}"



    
