from django.shortcuts import render, redirect, get_object_or_404
from django.db.models import Q
from django.views.decorators.http import require_http_methods
from .models import Habitacion
from .forms import CrearHabitacionForm, EditarHabitacionForm

def inicio(request):
    habitaciones = Habitacion.objects.all()
    return render(request, 'habitaciones/inicio.html', {'total': habitaciones.count(),
        'disponibles': habitaciones.filter(estado='disponible').count(),
        'ocupadas': habitaciones.filter(estado='ocupada').count(),
        'mantenimiento': habitaciones.filter(estado='mantenimiento').count(), 'ultimas': habitaciones.order_by('-creada')[:5]})

def listado(request):
    habitaciones = Habitacion.objects.all()
    q = request.GET.get('q', '').strip()
    estado = request.GET.get('estado', '')
    if q:
        filtro = Q(descripcion__icontains=q)
        if q.isdigit(): filtro |= Q(numero=int(q))
        habitaciones = habitaciones.filter(filtro)
    if estado in dict(Habitacion.ESTADOS): habitaciones = habitaciones.filter(estado=estado)
    return render(request, 'habitaciones/listado.html', {'habitaciones': habitaciones, 'q': q, 'estado': estado, 'estados': Habitacion.ESTADOS})

def detalle(request, pk):
    return render(request, 'habitaciones/detalle.html', {'habitacion': get_object_or_404(Habitacion, pk=pk)})

@require_http_methods(['GET', 'POST'])
def crear(request):
    form = CrearHabitacionForm(request.POST if request.method == 'POST' else None)
    if request.method == 'POST' and form.is_valid():
        habitacion = form.save()
        return redirect('habitaciones:detalle', pk=habitacion.pk)
    return render(request, 'habitaciones/crear.html', {'form': form})

@require_http_methods(['GET', 'POST'])
def editar(request, pk):
    habitacion = get_object_or_404(Habitacion, pk=pk)
    form = EditarHabitacionForm(request.POST if request.method == 'POST' else None, instance=habitacion)
    if request.method == 'POST' and form.is_valid():
        form.save()
        return redirect('habitaciones:detalle', pk=pk)
    return render(request, 'habitaciones/editar.html', {'form': form, 'habitacion': habitacion})

@require_http_methods(['GET', 'POST'])
def eliminar(request, pk):
    habitacion = get_object_or_404(Habitacion, pk=pk)
    if request.method == 'POST':
        habitacion.delete()
        return redirect('habitaciones:listado')
    return render(request, 'habitaciones/eliminar.html', {'habitacion': habitacion})
