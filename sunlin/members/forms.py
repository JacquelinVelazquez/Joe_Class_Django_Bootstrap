from django import forms
from .models import Article

class ArticleForm(forms.ModelForm):
    # Forzar validación, ya q "sin nombre" no debería pasar
    name = forms.CharField(
        required=True,
        label="Nombre",
        widget=forms.TextInput(
            attrs={
                "class": "form-control",
                "placeholder": "Ej. Playera",
                "maxlength": "250",
                "required": True,
            }
        ),
        error_messages={
            "required": "El nombre es obligatorio.",
        },
    )

    content = forms.CharField(
        required=False,
        label="Contenido",
        widget=forms.Textarea(
            attrs={
                "class": "form-control",
                "rows": 5,
                "placeholder": "Opcional…",
            }
        ),
    )

    class Meta:
        model = Article
        fields = ["name", "content"]

    def clean_name(self):
        name = (self.cleaned_data.get("name") or "").strip()
        if not name:
            raise forms.ValidationError("El nombre es obligatorio.")
        return name