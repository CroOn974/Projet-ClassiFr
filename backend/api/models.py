from django.db import models

from django.db import models


class Associer(models.Model):
    id_associer = models.AutoField(primary_key=True)
    id_model = models.ForeignKey('Model', models.DO_NOTHING, db_column='id_model', blank=True, null=True)
    libele = models.ForeignKey('Label', models.DO_NOTHING, db_column='libele', blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'associer'
        unique_together = (('id_model', 'libele'),)


class DateCreate(models.Model):
    jour = models.DateField(primary_key=True)

    class Meta:
        managed = False
        db_table = 'date_create'


class Label(models.Model):
    libele = models.CharField(primary_key=True, max_length=50)

    class Meta:
        managed = False
        db_table = 'label'


class Model(models.Model):
    id_model = models.AutoField(primary_key=True)
    name = models.CharField(max_length=50)
    mod_file = models.CharField(max_length=255)
    accuracy = models.DecimalField(max_digits=15, decimal_places=4)
    jour = models.ForeignKey(DateCreate, models.DO_NOTHING, db_column='jour',blank=True, null=True)
    status = models.BooleanField(blank=True, null=True)
    info = models.CharField(max_length=255, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'model'

    def etatStatus(self):
        if self.status is False:
            self.status = True
        else:
            self.status = False
        self.save()


class Predict(models.Model):
    id_predict = models.AutoField(primary_key=True)
    image = models.TextField(blank=True, null=True)
    bonne_pred = models.BooleanField()
    libele = models.ForeignKey(Label, models.DO_NOTHING, db_column='libele', blank=True, null=True)
    jour = models.ForeignKey(DateCreate, models.DO_NOTHING, db_column='jour', blank=True, null=True)
    id_model = models.ForeignKey(Model, models.DO_NOTHING, db_column='id_model', blank=True, null=True)
    feedback = models.CharField(max_length=255, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'predict'

