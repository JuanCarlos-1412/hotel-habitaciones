from django.test import TestCase, Client
from django.urls import reverse
from django.db import IntegrityError, transaction
from .models import Habitacion
from .forms import CrearHabitacionForm

class HabitacionTests(TestCase):
    def setUp(self):
        self.data = dict(numero=301, tipo='doble', capacidad=2, precio_noche='50000.00', piso=3, estado='disponible', descripcion='Vista al jardín')
    def test_crud_web_y_persistencia(self):
        self.assertEqual(self.client.get('/').status_code, 200)
        self.assertEqual(self.client.get('/habitaciones/crear/').status_code, 200)
        self.assertEqual(self.client.post('/habitaciones/crear/', self.data).status_code, 302)
        h = Habitacion.objects.get(numero=301)
        self.assertContains(self.client.get('/habitaciones/'), '301')
        self.assertContains(self.client.get(reverse('habitaciones:detalle', args=[h.pk])), 'Vista al jardín')
        self.assertEqual(self.client.get(reverse('habitaciones:editar', args=[h.pk])).status_code, 200)
        data = dict(self.data, precio_noche='70000.00', estado='ocupada', numero=999)
        self.client.post(reverse('habitaciones:editar', args=[h.pk]), data)
        h.refresh_from_db()
        self.assertEqual(h.numero, 301)
        self.assertEqual(h.estado, 'ocupada')
        self.assertEqual(str(h.precio_noche), '70000.00')
        url = reverse('habitaciones:eliminar', args=[h.pk])
        self.assertEqual(self.client.get(url).status_code, 200)
        self.assertTrue(Habitacion.objects.filter(pk=h.pk).exists())
        self.assertEqual(self.client.post(url).status_code, 302)
        self.assertFalse(Habitacion.objects.filter(pk=h.pk).exists())
    def test_validaciones(self):
        for campo, valor in [('numero',0), ('capacidad',0), ('capacidad',11), ('precio_noche','0'), ('precio_noche','-1'), ('piso',-1), ('tipo','invalido'), ('estado','invalido'), ('numero','texto'), ('descripcion','x'*501)]:
            with self.subTest(campo=campo, valor=valor):
                self.assertFalse(CrearHabitacionForm(dict(self.data, **{campo: valor})).is_valid())
        self.assertFalse(CrearHabitacionForm({}).is_valid())
        Habitacion.objects.create(**self.data)
        self.assertFalse(CrearHabitacionForm(self.data).is_valid())
    def test_constraint_bd(self):
        with self.assertRaises(IntegrityError), transaction.atomic():
            Habitacion.objects.create(**dict(self.data, precio_noche=0))
    def test_csrf_y_no_encontrado(self):
        c = Client(enforce_csrf_checks=True)
        self.assertEqual(c.post('/habitaciones/crear/', self.data).status_code, 403)
        self.assertEqual(self.client.get('/habitaciones/99999/').status_code, 404)
    def test_filtros(self):
        Habitacion.objects.create(**self.data)
        self.assertContains(self.client.get('/habitaciones/?q=301'), '301')
        self.assertNotContains(self.client.get('/habitaciones/?estado=ocupada'), '<td>301</td>')
