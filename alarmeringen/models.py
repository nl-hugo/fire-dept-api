from django.db import models


class Dienst(models.Model):
    id = models.CharField(max_length=2, primary_key=True)
    omschrijving = models.CharField(max_length=20)

    def __str__(self):
        return self.omschrijving

    class Meta:
        ordering = ['id']


class CapCode(models.Model):
    capcode = models.CharField(max_length=10, primary_key=True)
    omschrijving = models.CharField(max_length=500)

    def __str__(self):
        return '{} - {}'.format(self.capcode, self.omschrijving)

    class Meta:
        ordering = ['capcode']


class Regio(models.Model):
    id = models.CharField(max_length=2, primary_key=True)
    omschrijving = models.CharField(max_length=200)

    def __str__(self):
        return self.omschrijving

    class Meta:
        ordering = ['id']


class BrandAlarmeringManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(dienst__omschrijving='Brandweer')


class Alarmering(models.Model):
    id = models.CharField(max_length=20, primary_key=True)
    melding = models.CharField(max_length=500)
    tekstmelding = models.CharField(max_length=500)
    dienst = models.ForeignKey(
        Dienst, on_delete=models.CASCADE, null=True, related_name='alarmeringen')
    regio = models.ForeignKey(
        Regio, on_delete=models.CASCADE, null=True, related_name='alarmeringen')
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
        CapCode, blank=True, related_name='alarmeringen')
    capstring = models.CharField(max_length=1000)
    details = models.CharField(max_length=200)
    parent = models.ForeignKey(
        'self', on_delete=models.CASCADE, null=True, related_name='subitems')

    objects = models.Manager()
    brand = BrandAlarmeringManager()

    def __str__(self):
        return '{}'.format(self.id)

    def set_plaats(self):
        if self.postcode is not None:
            self.plaats = self.plaats.replace(self.postcode, '').lstrip()

    def save(self, *args, **kwargs):
        self.set_plaats()
        super(Alarmering, self).save(*args, **kwargs)

    class Meta:
        ordering = ['-id']
        verbose_name_plural = 'Alarmeringen'
