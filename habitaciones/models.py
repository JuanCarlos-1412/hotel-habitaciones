from decimal import Decimal
from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator

class Habitacion(models.Model):
    TIPOS = [('individual', 'Individual'), ('doble', 'Doble'), ('suite', 'Suite'), ('familiar', 'Familiar')]
    ESTADOS = [('disponible', 'Disponible'), ('ocupada', 'Ocupada'), ('mantenimiento', 'En mantenimiento')]
    numero = models.PositiveIntegerField('Número', unique=True, validators=[MinValueValidator(1), MaxValueValidator(9999)])
    tipo = models.CharField('Tipo', max_length=20, choices=TIPOS)
    capacidad = models.PositiveSmallIntegerField('Capacidad', validators=[MinValueValidator(1), MaxValueValidator(10)])
    precio_noche = models.DecimalField('Precio por noche CLP', max_digits=10, decimal_places=2, validators=[MinValueValidator(Decimal('0.01'))])
    piso = models.PositiveSmallIntegerField('Piso', default=1, validators=[MinValueValidator(0), MaxValueValidator(100)])
    estado = models.CharField('Estado', max_length=20, choices=ESTADOS, default='disponible')
    descripcion = models.TextField('Descripción', max_length=500, blank=True)
    creada = models.DateTimeField(auto_now_add=True)
    actualizada = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'habitaciones'
        ordering = ['numero']
        constraints = [
            models.CheckConstraint(check=models.Q(numero__gte=1, numero__lte=9999), name='numero_valido'),
            models.CheckConstraint(check=models.Q(capacidad__gte=1, capacidad__lte=10), name='capacidad_valida'),
            models.CheckConstraint(check=models.Q(precio_noche__gt=0), name='precio_positivo'),
            models.CheckConstraint(check=models.Q(piso__gte=0, piso__lte=100), name='piso_valido'),
            models.CheckConstraint(check=models.Q(tipo__in=['individual','doble','suite','familiar']), name='tipo_valido'),
            models.CheckConstraint(check=models.Q(estado__in=['disponible','ocupada','mantenimiento']), name='estado_valido'),
        ]
    def __str__(self):
        return f'Habitación {self.numero}'
