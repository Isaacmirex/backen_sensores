from django.db import models

class Usuario(models.Model):
    usr_id = models.AutoField(primary_key=True)
    usr_edad = models.IntegerField()
    usr_peso = models.FloatField()
    usr_altura = models.FloatField()
    usr_genero = models.CharField(max_length=20)
    usr_hijos = models.SmallIntegerField(null=True)
    usr_vive_solo = models.SmallIntegerField(null=True)
    usr_facultad = models.CharField(max_length=50)
    usr_trabaja = models.SmallIntegerField(null=True)

    class Meta:
        db_table = 'usuario'

class Encuesta(models.Model):
    ec_id = models.AutoField(primary_key=True)
    ec_pregunta_1 = models.IntegerField()
    ec_pregunta_2 = models.IntegerField()
    ec_pregunta_3 = models.IntegerField()
    ec_pregunta_4 = models.IntegerField()
    ec_pregunta_5 = models.IntegerField()
    ec_pregunta_6 = models.IntegerField()
    ec_pregunta_7 = models.IntegerField()
    ec_pregunta_8 = models.IntegerField()
    ec_pregunta_9 = models.IntegerField()
    ec_pregunta_10 = models.IntegerField()
    ec_pregunta_11 = models.IntegerField()
    ec_pregunta_12 = models.IntegerField()
    ec_pregunta_13 = models.IntegerField()
    ec_pregunta_14 = models.IntegerField()
    usr = models.ForeignKey(Usuario, on_delete=models.CASCADE, null=True, blank=True)

    class Meta:
        db_table = 'encuesta'

class Sensores(models.Model):
    sen_id = models.AutoField(primary_key=True)
    sen_emg = models.IntegerField()
    sen_temperatura = models.IntegerField()
    sen_freq_respiratoria = models.IntegerField()
    sen_freq_cardiaca = models.IntegerField()
    usr = models.ForeignKey(Usuario, on_delete=models.CASCADE)

    class Meta:
        db_table = 'sensores'
