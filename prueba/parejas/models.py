from django.db import models
from django.contrib.auth.models import User


class Pareja(models.Model):
    codigo = models.CharField(max_length=12, unique=True)
    clave_union = models.CharField(max_length=100)
    creador = models.ForeignKey(User, on_delete=models.CASCADE, related_name='pareja_creada')
    fecha_creacion = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.codigo


class MiembroPareja(models.Model):
    pareja = models.ForeignKey(Pareja, on_delete=models.CASCADE, related_name='miembros')
    usuario = models.ForeignKey(User, on_delete=models.CASCADE, related_name='parejas')
    fecha_union = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('pareja', 'usuario')

    def __str__(self):
        return f"{self.usuario.username} - {self.pareja.codigo}"


class Seccion(models.Model):
    pareja = models.ForeignKey(Pareja, on_delete=models.CASCADE, related_name='secciones')
    nombre = models.CharField(max_length=100)
    descripcion = models.TextField(blank=True, null=True)
    creado_por = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    fecha_creacion = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['nombre']

    def __str__(self):
        return self.nombre


class Archivo(models.Model):
    TIPO_CHOICES = [
        ('foto', 'Foto'),
        ('video', 'Video'),
    ]

    pareja = models.ForeignKey(Pareja, on_delete=models.CASCADE, related_name='archivos')
    seccion = models.ForeignKey(Seccion, on_delete=models.CASCADE, related_name='archivos')
    usuario = models.ForeignKey(User, on_delete=models.CASCADE, related_name='archivos_subidos')
    archivo = models.FileField(upload_to='parejas_archivos/')
    tipo = models.CharField(max_length=10, choices=TIPO_CHOICES)
    favorito = models.BooleanField(default=False)
    fecha_subida = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.usuario.username} - {self.tipo}"


class Nota(models.Model):
    pareja = models.ForeignKey(Pareja, on_delete=models.CASCADE, related_name='notas')
    autor = models.ForeignKey(User, on_delete=models.CASCADE, related_name='notas_escritas')
    texto = models.TextField()
    fecha = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-fecha']

    def __str__(self):
        return f"Nota de {self.autor.username}"