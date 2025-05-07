from django.shortcuts import render
from reports.forms import ReporteForm
from supplies.models import Insumo
from django.views.generic import TemplateView, ListView
from django.template.loader import render_to_string
from django.http import HttpResponse
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer
from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet
# from weasyprint import HTML
from django.contrib.auth.decorators import login_required, user_passes_test
from django.utils.decorators import method_decorator
from users.models import User
from supplies.models import Insumo
from sales.models import Venta


def is_admin_or_surpervisor(user):
    return user.is_authenticated and user.is_admin_or_supervisor

# Create your views here.

class ReportesView(TemplateView):
    template_name = 'reports/reportes.html'
    form_class = ReporteForm

    @method_decorator(login_required)
    @method_decorator(user_passes_test(is_admin_or_surpervisor))
    def get(self, request, *args, **kwargs):
        form = self.form_class()
        return render(request, self.template_name, {'form': form})
    
    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)

        if form.is_valid():
            mostrar_insumos = form.cleaned_data['mostrar_insumos']
            mostrar_usuarios = form.cleaned_data['mostrar_usuarios']
            mostrar_ventas = form.cleaned_data['mostrar_ventas']

            # Datos dinámicos
            insumos = Insumo.objects.all() if mostrar_insumos else []
            usuarios = User.objects.all() if mostrar_usuarios else []
            ventas = Venta.objects.select_related('insumo', 'vendedor').all() if mostrar_ventas else []

            # Respuesta HTTP para descargar PDF
            response = HttpResponse(content_type='application/pdf')
            response['Content-Disposition'] = 'attachment; filename="reporte_personalizado.pdf"'

            # Crear el PDF
            doc = SimpleDocTemplate(response, pagesize=letter)
            elementos = []

            styles = getSampleStyleSheet()
            style_title = styles['Heading2']
            style_title.alignment = 1  # Centrado

            # Tabla de Insumos
            if mostrar_insumos:
                title = Paragraph("Reporte de Insumos", style_title)
                elementos.append(title)
                elementos.append(Spacer(1, 12))
                data = [['ID', 'Nombre', 'Cantidad Disponible', 'Precio Unitario']]
                for insumo in insumos:
                    data.append([
                        str(insumo.id),
                        insumo.nombre,
                        str(insumo.cantidad_disponible),
                        f"${insumo.precio_unitario:.2f}"
                    ])
                tabla = Table(data)
                tabla.setStyle(TableStyle([
                    ('BACKGROUND', (0, 0), (-1, 0), colors.lightblue),
                    ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
                    ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
                    ('FONTSIZE', (0, 0), (-1, 0), 12),
                    ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
                    ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
                    ('GRID', (0, 0), (-1, -1), 1, colors.black),
                ]))
                elementos.append(tabla)

            # Tabla de Usuarios
            if mostrar_usuarios:

                title = Paragraph("Reporte de Usuarios", style_title)
                elementos.append(title)
                elementos.append(Spacer(1, 12))

                data = [['ID', 'Email', 'Nombre Completo', 'Rol']]
                for usuario in usuarios:
                    rol = "Administrador" if usuario.is_administrador else (
                        "Supervisor" if usuario.is_supervisor else "Vendedor"
                        )
                    data.append([
                        str(usuario.id),
                        usuario.email,
                        f"{usuario.first_name} {usuario.last_name}".strip() or "Sin nombre",
                        rol
                    ])
                tabla = Table(data)
                tabla.setStyle(TableStyle([
                    ('BACKGROUND', (0, 0), (-1, 0), colors.lightgreen),
                    ('TEXTCOLOR', (0, 0), (-1, 0), colors.black),
                    ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
                    ('FONTSIZE', (0, 0), (-1, 0), 12),
                    ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
                    ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
                    ('GRID', (0, 0), (-1, -1), 1, colors.black),
                ]))
                elementos.append(tabla)

            # Tabla de Ventas
            if mostrar_ventas:

                title = Paragraph("Reporte de Ventas", style_title)
                elementos.append(title)
                elementos.append(Spacer(1, 12))

                data = [['ID', 'Fecha de Venta', 'Insumo', 'Vendedor', 'Cantidad Vendida', 'Total']]
                for venta in ventas:
                    data.append([
                        str(venta.id),
                        venta.fecha_venta.strftime("%d/%m/%Y %H:%M"),
                        venta.insumo.nombre,
                        venta.vendedor.email,
                        str(venta.cantidad_vendida),
                        f"${venta.total_venta:.2f}"
                    ])
                tabla = Table(data)
                tabla.setStyle(TableStyle([
                    ('BACKGROUND', (0, 0), (-1, 0), colors.lightcoral),
                    ('TEXTCOLOR', (0, 0), (-1, 0), colors.black),
                    ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
                    ('FONTSIZE', (0, 0), (-1, 0), 12),
                    ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
                    ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
                    ('GRID', (0, 0), (-1, -1), 1, colors.black),
                ]))
                elementos.append(tabla)

            doc.build(elementos)
            return response

        return render(request, self.template_name, {'form': form})
    
    
    

# def es_admin_o_supervisor(user):
#     return user.groups.filter(name__in=['Administrador', 'Supervisor']).exists()

# @login_required
# @user_passes_test(es_admin_o_supervisor)
# def generar_reporte_pdf(request):
#     insumos = Insumo.objects.all()
#     bodega = Bodega.objects.all()
#     prestamos = PrestamoEspacio.objects.all()
    
#     html_string = render_to_string('reports/reporte_pdf.html', {
#         'insumos': insumos,
#         'bodega': bodega,
#         'prestamos': prestamos
#     })

#     html = HTML(string=html_string)
#     pdf = html.write_pdf()

#     response = HttpResponse(pdf, content_type='application/pdf')
#     response['Content-Disposition'] = 'inline; filename="reportesList.pdf"'
#     return response
