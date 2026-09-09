import random
import string

from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login
from django.db.models import Q
from django.shortcuts import render, redirect
from django.contrib import messages

from .models import Pareja, MiembroPareja, Seccion, Nota, Archivo


def inicio(request):
    if request.user.is_authenticated:
        return redirect('dashboard')
    return render(request, 'parejas/inicio.html')


def generar_codigo():
    return ''.join(random.choices(string.ascii_uppercase + string.digits, k=8))


@login_required
def dashboard(request):
    pareja = None
    try:
        miembro = MiembroPareja.objects.get(usuario=request.user)
        pareja = miembro.pareja
    except MiembroPareja.DoesNotExist:
        pareja = None

    secciones = Seccion.objects.filter(pareja=pareja) if pareja else []
    notas = Nota.objects.filter(pareja=pareja) if pareja else []
    archivos = Archivo.objects.filter(pareja=pareja) if pareja else []

    return render(request, 'parejas/dashboard.html', {
        'pareja': pareja,
        'secciones': secciones,
        'notas': notas[:5],
        'archivos': archivos[:5],
    })


@login_required
def crear_pareja(request):
    if request.method == 'POST':
        clave = request.POST.get('clave_union', '').strip()
        if not clave:
            messages.error(request, 'Debes poner una clave de unión.')
            return redirect('crear_pareja')

        codigo = generar_codigo()
        while Pareja.objects.filter(codigo=codigo).exists():
            codigo = generar_codigo()

        pareja = Pareja.objects.create(
            codigo=codigo,
            clave_union=clave,
            creador=request.user,
        )
        MiembroPareja.objects.create(pareja=pareja, usuario=request.user)
        messages.success(request, f'Pareja creada. Código: {codigo}')
        return redirect('dashboard')

    return render(request, 'parejas/crear_pareja.html')


@login_required
def unirse_pareja(request):
    if request.method == 'POST':
        codigo = request.POST.get('codigo', '').strip()
        clave = request.POST.get('clave_union', '').strip()

        try:
            pareja = Pareja.objects.get(codigo=codigo)
        except Pareja.DoesNotExist:
            messages.error(request, 'Ese código no existe.')
            return redirect('unirse_pareja')

        if pareja.clave_union != clave:
            messages.error(request, 'La clave de unión no coincide.')
            return redirect('unirse_pareja')

        if MiembroPareja.objects.filter(pareja=pareja, usuario=request.user).exists():
            messages.info(request, 'Ya formas parte de esta pareja.')
            return redirect('dashboard')

        MiembroPareja.objects.create(pareja=pareja, usuario=request.user)
        messages.success(request, 'Te has unido a la pareja correctamente.')
        return redirect('dashboard')

    return render(request, 'parejas/unirse_pareja.html')


@login_required
def crear_seccion(request):
    if request.method == 'POST':
        nombre = request.POST.get('nombre', '').strip()
        descripcion = request.POST.get('descripcion', '').strip()

        if not nombre:
            messages.error(request, 'El nombre de la sección es obligatorio.')
            return redirect('crear_seccion')

        miembro = MiembroPareja.objects.filter(usuario=request.user).first()
        if not miembro:
            messages.error(request, 'Primero debes entrar a una pareja.')
            return redirect('dashboard')

        Seccion.objects.create(
            pareja=miembro.pareja,
            nombre=nombre,
            descripcion=descripcion,
            creado_por=request.user,
        )
        messages.success(request, 'Sección creada correctamente.')
        return redirect('dashboard')

    return render(request, 'parejas/crear_seccion.html')


@login_required
def notas(request):
    miembro = MiembroPareja.objects.filter(usuario=request.user).first()
    if not miembro:
        return redirect('dashboard')

    if request.method == 'POST':
        texto = request.POST.get('texto', '').strip()
        if texto:
            Nota.objects.create(pareja=miembro.pareja, autor=request.user, texto=texto)
            messages.success(request, 'Nota enviada.')
        return redirect('notas')

    lista_notas = Nota.objects.filter(pareja=miembro.pareja)
    return render(request, 'parejas/notas.html', {'notas': lista_notas})


@login_required
def subir_archivo(request):
    miembro = MiembroPareja.objects.filter(usuario=request.user).first()
    if not miembro:
        return redirect('dashboard')

    secciones = Seccion.objects.filter(pareja=miembro.pareja)

    if request.method == 'POST':
        seccion_id = request.POST.get('seccion')
        archivo = request.FILES.get('archivo')
        tipo = request.POST.get('tipo', 'foto')

        if not seccion_id or not archivo:
            messages.error(request, 'Debes elegir una sección y subir un archivo.')
            return redirect('subir_archivo')

        seccion = Seccion.objects.filter(id=seccion_id, pareja=miembro.pareja).first()
        if not seccion:
            messages.error(request, 'Sección no válida.')
            return redirect('subir_archivo')

        Archivo.objects.create(
            pareja=miembro.pareja,
            seccion=seccion,
            usuario=request.user,
            archivo=archivo,
            tipo=tipo,
        )
        messages.success(request, 'Archivo subido correctamente.')
        return redirect('dashboard')

    return render(request, 'parejas/subir_archivo.html', {'secciones': secciones})


@login_required
def galerias(request):
    miembro = MiembroPareja.objects.filter(usuario=request.user).first()
    if not miembro:
        return redirect('dashboard')

    archivos = Archivo.objects.filter(pareja=miembro.pareja).order_by('-fecha_subida')
    favoritos = archivos.filter(favorito=True)
    return render(request, 'parejas/galeria.html', {'archivos': archivos, 'favoritos': favoritos})


@login_required
def toggle_favorito(request, archivo_id):
    miembro = MiembroPareja.objects.filter(usuario=request.user).first()
    if not miembro:
        return redirect('dashboard')

    archivo = Archivo.objects.filter(id=archivo_id, pareja=miembro.pareja).first()
    if archivo:
        archivo.favorito = not archivo.favorito
        archivo.save()
        messages.success(request, 'Estado de favorito actualizado.')
    else:
        messages.error(request, 'No se encontró ese archivo.')

    return redirect('galeria')


def registro(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('dashboard')
    else:
        form = UserCreationForm()
    return render(request, 'registration/registro.html', {'form': form})