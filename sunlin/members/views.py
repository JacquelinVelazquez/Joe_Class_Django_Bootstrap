from django.shortcuts import render, redirect, get_object_or_404
from django.views import View
from django.views.generic import ListView, DetailView
from django.contrib import messages
from .models import Article
from .forms import ArticleForm


class ArticleView(View):
    def get(self, request):
        return render(request, "articles.html", {"data": "hey data"})


class ArticleListView(ListView):
    model = Article
    template_name = "members/article_list.html"          
    context_object_name = "article_list"


class ArticleDetailView(DetailView):
    model = Article
    template_name = "members/article_detail.html"   
    context_object_name = "article"


class NewArticleForm(View):
    def get(self, request):
        form = ArticleForm()
        return render(request, "members/new_article_form.html", {"form": form})

    def post(self, request):
        form = ArticleForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Artículo creado correctamente.")            
            return redirect("all_articles")

        # marcar campos con error en rojo (Bootstrap)
        for field_name in form.errors:
            if field_name in form.fields:
                widget = form.fields[field_name].widget
                existing = widget.attrs.get("class", "")
                if "is-invalid" not in existing:
                    widget.attrs["class"] = (existing + " is-invalid").strip()

        messages.error(request, "Revisa los campos marcados en rojo.")
        return render(request, "members/new_article_form.html", {"form": form})


class EditArticleForm(View):
    def get(self, request, pk):
        article = get_object_or_404(Article, pk=pk)
        form = ArticleForm(instance=article)
        return render(request, "members/edit_article_form.html", {"form": form, "article": article})
    def post(self, request, pk):
        article = get_object_or_404(Article, pk=pk)
        form = ArticleForm(request.POST, instance=article)
        if form.is_valid():
            form.save()
            messages.success(request, "Cambios guardados.")
            return redirect("article_detail", pk=article.pk)

        for field_name in form.errors:
            if field_name in form.fields:
                widget = form.fields[field_name].widget
                existing = widget.attrs.get("class", "")
                if "is-invalid" not in existing:
                    widget.attrs["class"] = (existing + " is-invalid").strip()

        messages.error(request, "Revisa los campos marcados en rojo.")
        return render(request, "members/edit_article_form.html", {"form": form, "article": article})