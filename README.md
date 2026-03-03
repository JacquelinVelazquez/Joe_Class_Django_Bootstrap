# Joe_Class_Django_Bootstrap

Este repositorio contiene el proyecto Django Sunlin con una mejora específica: la integración de Bootstrap 5 y jQuery para que los errores de validación en formularios se vean claros y estéticos, sin quitar la validación real del servidor (Django).
La idea principal es que:
- Django valida en el servidor (lo importante y obligatorio).
- Bootstrap mejora la UI (inputs en rojo, mensajes debajo, alertas).
- jQuery apoya con validación visual (solo estética: marcar vacíos, quitar rojo al escribir).

Permite crear y editar artículos. Si el usuario intenta guardar un artículo con campos vacíos:
- El input se marca en rojo (`is-invalid`)
- Aparece el error debajo (`invalid-feedback`)
- Se muestra una alerta general arriba (Bootstrap + `django.contrib.messages`)

> Nota: La validación real sigue siendo del lado del servidor (Django). jQuery se usa como apoyo **estético** del lado del cliente.
> Django (servidor) es quien manda en la validación real.
> jQuery solo ayuda visualmente (no sustituye la validación del servidor).
> Bootstrap se encarga del diseño (formularios, botones, alerts).

## Requisitos técnicos (mínimo)
- Python + pip
- Django
- VS Code (opcional)

## Estructura:
```text
Joe_Class_Django/
├─ .gitignore
├─ README.md
└─ sunlin/
   ├─ manage.py
   ├─ sunlin/
   │  ├─ settings.py
   │  ├─ urls.py
   │  └─ ...
   └─ members/
      ├─ views.py
      ├─ forms.py
      ├─ models.py
      └─ templates/
         └─ members/
            ├─ base.html
            ├─ new_article_form.html
            └─ edit_article_form.html
```

## Instalación y ejecución (paso a paso)
### 1) Clonar el repositorio
```bash
git clone https://github.com/JacquelinVelazquez/Joe_Class_Django_Bootstrap.git
cd Joe_Class_Django_Bootstrap
```
### 2) Crear y activar entorno virtual
Windows (PowerShell):
```bash
python -m venv venv
.\venv\Scripts\Activate.ps1
```

### 3) Instalar Django
```bash
pip install django
```

### 4) Migraciones (base de datos)
```bash
cd sunlin
python manage.py makemigrations
python manage.py migrate
```

### 5) Ejecutar el servidor
```bash
python manage.py runserver
```
- Abre en tu navegador:
  http://127.0.0.1:8000/

## Modificaciones
### 1) sunlin/members/models.py — campos obligatorios (validación servidor)
```python
name = models.CharField(max_length=250)
content = models.TextField()
```
El servidor ya no permite guardar artículos sin nombre o sin contenido.

### 2) sunlin/members/forms.py — widgets Bootstrap + mensajes personalizados
Se agregaron:
- required=True
- error_messages personalizados
- widget con class="form-control" para que Bootstrap aplique diseño
```python
name = forms.CharField(
    required=True,
    error_messages={'required': 'El nombre es obligatorio.'},
    widget=forms.TextInput(attrs={'class': 'form-control'})
)
```

### 3) sunlin/members/views.py — mensajes con django.contrib.messages

Se integraron alertas generales (éxito/error):
- messages.success() cuando se guarda correctamente
- messages.error() cuando hay errores
```python
from django.contrib import messages

if form.is_valid():
    form.save()
    messages.success(request, "Artículo creado correctamente.")
else:
    messages.error(request, "Hay errores en el formulario.")
```

### 4) templates/members/base.html
Se creó un template base para centralizar:
- Bootstrap 5 (CDN)
- jQuery (CDN)
- Render de messages como alertas Bootstrap
- Script jQuery para validación estética (marcar vacíos con is-invalid)
```python
<!-- 1) Bootstrap (UI) -->
<link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.2/dist/css/bootstrap.min.css" rel="stylesheet">

<!-- 2) Django messages renderizados como alerts de Bootstrap -->
{% if messages %}
  {% for message in messages %}
    <div class="alert alert-{{ message.tags }} alert-dismissible fade show" role="alert">
      {{ message }}
      <button type="button" class="btn-close" data-bs-dismiss="alert"></button>
    </div>
  {% endfor %}
{% endif %}

<!-- 3) jQuery + validación estética (marca campos vacíos con is-invalid) -->
<script src="https://code.jquery.com/jquery-3.6.0.min.js"></script>
<script>
  $('form').on('submit', function () {
    let valid = true;
    $('input, textarea').each(function () {
      $(this).toggleClass('is-invalid', $(this).val().trim() === '');
      if ($(this).val().trim() === '') valid = false;
    });
    return valid;
  });
</script>
```

### 5) new_article_form.html y edit_article_form.html — errores debajo del input
Antes se usaba {{ form.as_p }} (sin control del layout), pero ahora se renderiza campo por campo y se imprime el error con Bootstrap:
```python
{% if form.name.errors %}
  <div class="invalid-feedback d-block">
    {{ form.name.errors.0 }}
  </div>
{% endif %}
```

## Validación
Abre la vista de “nuevo artículo”
- Da click en Guardar dejando name vacío
    Debe pasar:
    - input en rojo (is-invalid)
    - mensaje debajo (invalid-feedback)
    - alerta arriba con messages.error

- Llena correctamente y guarda.
    Debe pasar:
    - alerta verde con messages.success
