from django.core.management.base import BaseCommand
from habitaciones.models import Habitacion
class Command(BaseCommand):
    help = 'Agrega habitaciones de demostración sin sobrescribir registros existentes.'
    def handle(self, *args, **options):
        for numero, tipo, capacidad, precio, estado in [(101,'individual',1,35000,'disponible'),(102,'doble',2,55000,'ocupada'),(201,'suite',2,95000,'disponible'),(202,'familiar',4,75000,'mantenimiento')]:
            Habitacion.objects.get_or_create(numero=numero, defaults=dict(tipo=tipo, capacidad=capacidad, precio_noche=precio, estado=estado, piso=numero//100, descripcion='Habitación de demostración con baño privado.'))
        self.stdout.write(self.style.SUCCESS('Datos de demostración preparados.'))
