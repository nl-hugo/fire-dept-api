from django.db import models


class CapCode(models.Model):
    capcode = models.CharField(max_length=10, primary_key=True)
    omschrijving = models.CharField(max_length=500)

    def __str__(self):
        return '{} - {}'.format(self.capcode, self.omschrijving)

    class Meta:
        ordering = ['capcode']


class Alarmering(models.Model):
    id = models.CharField(max_length=20, primary_key=True)
    melding = models.CharField(max_length=500)
    tekstmelding = models.CharField(max_length=500)
    dienstid = models.CharField(max_length=2)
    dienst = models.CharField(max_length=20)
    regioid = models.CharField(max_length=2)
    regio = models.CharField(max_length=200)
    plaats = models.CharField(max_length=200, null=True, blank=True)
    postcode = models.CharField(max_length=20, null=True, blank=True)
    straat = models.CharField(max_length=200, null=True, blank=True)
    datum = models.DateField()
    tijd = models.TimeField()
    lat = models.CharField(max_length=20, null=True, blank=True)
    lon = models.CharField(max_length=20, null=True, blank=True)
    prio1 = models.CharField(max_length=1)
    brandinfo = models.CharField(max_length=50, null=True, blank=True)
    grip = models.CharField(max_length=1)
    capcodes = models.ManyToManyField(
        CapCode, null=True, blank=True, related_name='alarmeringen')
    capstring = models.CharField(max_length=200)
    details = models.CharField(max_length=200)
    subitems = models.ManyToManyField(
        'self', null=True, blank=True, related_name='alarmeringen')

    def __str__(self):
        return '{}'.format(self.id)

    class Meta:
        ordering = ['-id']
