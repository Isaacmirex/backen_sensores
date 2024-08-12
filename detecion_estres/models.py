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
    usr_estresPuntos = models.SmallIntegerField(null=True)  # Nivel de estrés en puntos
    usr_estresPorcentaje = models.FloatField(null=True)  # Porcentaje de estrés según PSS-14
    usr_estresTexto = models.CharField(max_length=255, null=True, blank=True)  # Descripción basada en PSS-14

    def save(self, *args, **kwargs):
        # Convertir usr_estresPuntos a porcentaje y asignar una descripción basada en la escala PSS-14
        if self.usr_estresPuntos is not None:
            estres_maximo = 56.0  # Puntuación máxima según la PSS-14
            porcentaje_estres = (self.usr_estresPuntos / estres_maximo) * 100

            if 0 <= self.usr_estresPuntos <= 14:
                self.usr_estresPuntos_texto = f'Casi nunca o nunca está estresado. ({porcentaje_estres:.2f}%)'
            elif 15 <= self.usr_estresPuntos <= 28:
                self.usr_estresPuntos_texto = f'De vez en cuando está estresado. ({porcentaje_estres:.2f}%)'
            elif 29 <= self.usr_estresPuntos <= 42:
                self.usr_estresPuntos_texto = f'A menudo está estresado. ({porcentaje_estres:.2f}%)'
            elif 43 <= self.usr_estresPuntos <= 56:
                self.usr_estresPuntos_texto = f'Muy a menudo está estresado. ({porcentaje_estres:.2f}%)'

        super().save(*args, **kwargs)

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
    ec_total = models.IntegerField(null=True)
    usr = models.ForeignKey(Usuario, on_delete=models.CASCADE, null=True, blank=True)

    class Meta:
        db_table = 'encuesta'

class Sensores(models.Model):
    sen_id = models.AutoField(primary_key=True)
    sen_temperatura = models.IntegerField()
    sen_freq_respiratoria = models.IntegerField()
    sen_freq_cardiaca = models.IntegerField()
    usr = models.ForeignKey(Usuario, on_delete=models.CASCADE, null=True, blank=True)

    class Meta:
        db_table = 'sensores'
