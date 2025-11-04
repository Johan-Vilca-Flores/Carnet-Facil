import os
from django.http import HttpResponse
from reportlab.pdfgen import canvas
from django.conf import settings
import os
from reportlab.lib.pagesizes import A4
from .models import Estudiante
from PIL import Image, ImageDraw, ImageFont
import barcode
from barcode.writer import ImageWriter
from django.shortcuts import render
from .forms import EstudianteForm
from django.shortcuts import render, get_object_or_404
from .models import Estudiante
from django.shortcuts import render, redirect
from .models import Estudiante
from reportlab.lib import colors
from reportlab.lib.colors import HexColor
from reportlab.graphics.barcode import code128

def lista_estudiantes(request):
    estudiantes = Estudiante.objects.all()
    return render(request, 'generator/lista_estudiantes.html', {'estudiantes': estudiantes})
def home(request):
    return render(request, 'generator/home.html')

def index(request):
    return render(request, 'index.html')  # o simplemente un HttpResponse
def generar_carnet(request):
    # Usaremos el primer estudiante como ejemplo
    estudiante = Estudiante.objects.last()  # Puedes cambiar esto según tu necesidad
    if not estudiante:
        return HttpResponse("No hay estudiantes registrados.")

    # Crear código de barras
    codigo_texto = f"{estudiante.dni}-{estudiante.grado}"
    barcode_class = barcode.get_barcode_class('code128')
    codigo = barcode_class(codigo_texto, writer=ImageWriter())
    barcode_path = os.path.join('generator/static/carnets', f'{estudiante.dni}_barcode.png')
    codigo.save(barcode_path.replace('.png', ''))  # guarda sin doble extensión

    # Crear carnet base (tamaño tarjeta 85x54 mm aprox → 1011x642 px a 300 dpi)
    carnet = Image.new('RGB', (1011, 642), color=(255, 255, 255))
    draw = ImageDraw.Draw(carnet)

    # Fuente básica (usa una del sistema o una ruta existente)
    font = ImageFont.load_default()

    # Escribir datos
    draw.text((50, 50), f"Nombre: {estudiante.nombre}", fill="black", font=font)
    draw.text((50, 100), f"DNI: {estudiante.dni}", fill="black", font=font)
    if estudiante.carrera:
        draw.text((50, 150), f"Carrera: {estudiante.carrera}", fill="black", font=font)
    draw.text((50, 200), f"Grado: {estudiante.grado}", fill="black", font=font)

    # Pegar el código de barras
    barcode_img = Image.open(barcode_path)
    carnet.paste(barcode_img.resize((400, 100)), (50, 300))

    # Guardar el carnet generado
    output_path = os.path.join('generator/static/carnets', f'{estudiante.dni}_carnet.png')
    carnet.save(output_path)

    return HttpResponse(f"Carnet generado correctamente: {output_path}")
def add_student(request):
    if request.method == 'POST':
        form = EstudianteForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('add_student')  # recarga la misma página
    else:
        form = EstudianteForm()
    return render(request, 'add_student.html', {'form': form})
def generar_carnet(request, estudiante_id):
    estudiante = get_object_or_404(Estudiante, id=estudiante_id)
    return render(request, 'generator/carnet.html', {'estudiante': estudiante})
def carnet_pdf(request, estudiante_id):
    from reportlab.lib import colors
    from reportlab.lib.utils import ImageReader
    import barcode
    from barcode.writer import ImageWriter
    import io

    estudiante = get_object_or_404(Estudiante, id=estudiante_id)

    # Crear respuesta PDF
    response = HttpResponse(content_type="application/pdf")
    response["Content-Disposition"] = f'inline; filename="carnet_{estudiante.dni}.pdf"'

    # Crear lienzo PDF
    p = canvas.Canvas(response, pagesize=A4)
    width, height = A4

    # 📄 Fondo personalizado
    fondo_path = os.path.join(settings.BASE_DIR, "generator/static/img/fondo.jpg")
    if os.path.exists(fondo_path):
     p.drawImage(fondo_path, 80, height - 481, width=282, height=481, mask='auto')

# 🧑 Datos del estudiante (centrado)
    p.setFont("Helvetica-Bold", 18)
    y_text = height - 320  # posición vertical del nombre
    nombre_texto = f"{estudiante.nombre}"

# Calcular ancho del texto y centrar
    text_width = p.stringWidth(nombre_texto, "Helvetica-Bold", 12)
    x_center = 80 + (230 - text_width) / 2  # 80 es donde empieza el fondo, 282 es su ancho

    p.drawString(x_center, y_text, nombre_texto)

    

    # 🖼️ Foto del estudiante (recortada en círculo real)
    if estudiante.foto:
       foto_path = os.path.join(settings.MEDIA_ROOT, str(estudiante.foto))
    if os.path.exists(foto_path):
        foto_size = 170
        x_foto = 139
        y_foto = height - 270

        # Abrir imagen y recortarla en círculo
        im = Image.open(foto_path).convert("RGBA")
        mask = Image.new("L", im.size, 0)
        draw = ImageDraw.Draw(mask)
        draw.ellipse((0, 0, im.size[0], im.size[1]), fill=255)
        im.putalpha(mask)

        # Guardar imagen temporal
        temp_io = io.BytesIO()
        im.save(temp_io, format="PNG")
        temp_io.seek(0)
        p.drawImage(ImageReader(temp_io), x_foto, y_foto, width=foto_size, height=foto_size, mask='auto')


    

    # 🧾 Generar código de barras (centrado)
    barcode_class = barcode.get_barcode_class("code128")
    codigo = barcode_class(estudiante.dni, writer=ImageWriter())
    buffer = io.BytesIO()
    codigo.write(buffer, options={"module_height": 8, "module_width": 0.3})
    buffer.seek(0)
    barcode_img = ImageReader(buffer)

   # Dimensiones del carnet
    x_inicio_fondo = 80
    ancho_carnet = 282

   # Dimensiones del código de barras
    barcode_width = 200
    barcode_height = 40

   # Calcular posición centrada
    x_center = x_inicio_fondo + (ancho_carnet - barcode_width) / 2
    y_barcode = height - 400  # posición vertical (ajústala si lo quieres más arriba o abajo)

   # Dibujar imagen centrada
    p.drawImage(barcode_img, x_center, y_barcode, width=barcode_width, height=barcode_height, mask='auto')


    # Finalizar PDF
    p.showPage()
    p.save()

    return response


from reportlab.lib.units import mm
from reportlab.lib.utils import ImageReader
from reportlab.lib import colors  # Agregado para colores

def carnets_pdf_todos(request):
    estudiantes = Estudiante.objects.all()
    if not estudiantes:
        return HttpResponse("No hay estudiantes registrados.")

    # Configurar PDF
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'inline; filename="carnets_todos.pdf"'
    p = canvas.Canvas(response, pagesize=A4)
    width, height = A4

    # Tamaño del carnet (85x54 mm)
    carnet_width = 85 * mm
    carnet_height = 54 * mm

    x_positions = [20 * mm, 115 * mm]  # 2 columnas
    y_positions = [height - (i * 60 * mm) - 80 * mm for i in range(4)]  # 4 filas

    col, row = 0, 0

    for i, estudiante in enumerate(estudiantes):
        x = x_positions[col]
        y = y_positions[row]

        # 📄 Fondo personalizado (imagen) en lugar del marco gris
        fondo_path = os.path.join(settings.BASE_DIR, "generator/static/img/fondo.jpg")  # Ruta a tu imagen de fondo
        if os.path.exists(fondo_path):
            p.drawImage(fondo_path, x, y, width=carnet_width, height=carnet_height, mask='auto')  # Dibuja la imagen de fondo escalada al tamaño del carnet
        # Marco gris encima del fondo (si no hay imagen, actúa como fallback)
        p.setStrokeColorRGB(0.2, 0.2, 0.2)
        p.rect(x, y, carnet_width, carnet_height, fill=0)

        # 🏫 Nombre de la academia (azul, agregado encima del título)
        p.setFont("Helvetica-Bold", 8)
        p.setFillColor(colors.HexColor("#014C9C"))  # Azul Harper
        p.drawString(x + 80, y + carnet_height - 10, "ACADEMIA HARPER")

        # 📘 Título del carnet
        p.setFont("Helvetica-Bold", 8)
        p.setFillColor(colors.black)
        p.drawString(x + 10, y + carnet_height - 30, "CARNET DE ESTUDIANTE")

        # 🧑 Datos del estudiante
        # 🧑 Datos del estudiante
        espaciado_vertical = 16 # Define el espacio que quieres (ej. 12 unidades)
        y_inicial = y + carnet_height - 50
        p.setFont("Helvetica", 10)  # Fuente más pequeña para que quepa
        # Línea 1
        p.drawString(x + 10, y_inicial, f"Nombre: {estudiante.nombre}")

# Línea 2 (y_inicial - 1 * espaciado_vertical)
        p.drawString(x + 10, y_inicial - espaciado_vertical, f"DNI: {estudiante.dni}")

# Línea 3 (y_inicial - 2 * espaciado_vertical)
        p.drawString(x + 10, y_inicial - (2 * espaciado_vertical), f"Carrera: {estudiante.carrera or '---'}")

# Línea 4 (y_inicial - 3 * espaciado_vertical)
        p.drawString(x + 10, y_inicial - (3 * espaciado_vertical), f"Grado: {estudiante.grado or '---'}")

        # 🖼️ Foto del estudiante (si existe) - Tamaño reducido para que quepa
        if estudiante.foto:
            foto_path = os.path.join(settings.MEDIA_ROOT, str(estudiante.foto))
            if os.path.exists(foto_path):
                p.drawImage(foto_path, x + carnet_width - 25*mm, y + carnet_height - 35*mm, width=20*mm, height=20*mm)

        # 🔵 Logo de la Academia (opcional, agregado en esquina inferior izquierda)
        logo_path = os.path.join(settings.BASE_DIR, "generator/static/img/logoo.png")
        if os.path.exists(logo_path):
            p.drawImage(logo_path, x + 5, y + 5, width=15*mm, height=15*mm, mask='auto')

        codigo_barra = code128.Code128(
        estudiante.dni,
        barHeight=10 * mm,  # Altura de las barras (ajusta a tu gusto)
        barWidth=0.5 * mm,  # Ancho de la barra más delgada (esto controla la longitud total)
        humanReadable=1     # Muestra el número DNI debajo del código
)

# Dibujamos el código de barras en el lienzo (ReportLab lo dibujará con la proporción correcta)
        p.setFont("Helvetica", 8) # Fuente más pequeña para el número de DNI
        codigo_barra.drawOn(p, x + 30, y + 20)
        # Mover posición
        col += 1
        if col >= 2:
            col = 0
            row += 1
        if row >= 4:
            p.showPage()
            row = 0
            col = 0

    p.save()
    return response
