from gc import get_objects

from django.shortcuts import render, redirect, get_object_or_404
from django.views import View
from django. views.generic import DetailView, UpdateView, DeleteView
from .forms import ArticleForm
from .models import Article, ArticleCategory, ArticleHistory, ArticleTag
from django.db.models import Q
from users.utils import role_required

class ArticleDetailView(DetailView):
    model = Article
    template_name = 'wiki/article_detail.html'
    context_object_name = 'article'

class ArticleUpdateView(UpdateView):
    model = Article
    template_name = 'wiki/add_article.html'

    form_class = ArticleForm

    def dispatch(self, request, *args, **kwargs):
        role = request.session.get('role')

        if role not in ['Инженер', 'Администратор']:
            return redirect('wiki')
        return super().dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        article = self.get_object()

        ArticleHistory.objects.create(
            article = article,
            title = article.title,
            content = article.content,
            edited_by_id = self.request.session.get('user_id'),
            comment = 'Редактирование статьи'
        )

        return super().form_valid(form)

class ArticleDeleteView(DeleteView):
    model = Article
    template_name = 'wiki/article_delete.html'
    success_url = '/wiki/'

    def dispatch(self, request, *args, **kwargs):
        role = request.session.get('role')

        if role not in ['Инженер', 'Администратор']:
            return redirect('wiki')
        return super().dispatch(request, *args, **kwargs)

def wiki_view(request):
    articles = Article.objects.all()
    categories = ArticleCategory.objects.all()
    tags = ArticleTag.objects.all().count()

    category_id = request.GET.get('category')
    if category_id:
        articles = articles.filter(category_id=category_id)

    search = request.GET.get('search')
    if search:
        articles = articles.filter(Q(title__icontains=search)|
                                   Q(category__name__icontains=search)|
                                   Q(tags__name__icontains=search)|
                                   Q(content__icontains=search)).distinct()

    return render(request, 'wiki/wiki_main.html', {'articles':articles,
                                                   'category':categories,
                                                   'tags_count': tags})

@role_required(['Инженер','Администратор'])
def add_article(request):
    error = ''

    if request.method == 'POST':

        form = ArticleForm(request.POST)

        if form.is_valid():

            article=form.save(commit=False)
            article.save()
            form.save_m2m()
            return redirect('wiki')

        else:
            error = 'Форма заполнена некорректно'

    form = ArticleForm()

    data = {
        'form': form,
        'error':error
    }

    return render(request, 'wiki/add_article.html',data)


def article_history(request, pk):

    article = get_object_or_404(
        Article,
        id=pk
    )

    history = article.history.all().order_by('-created_at')

    return render(
        request,
        'wiki/article_history.html',
        {
            'article': article,
            'history': history
        }
    )


def article_version(request, pk):

    version = get_object_or_404(
        ArticleHistory,
        id=pk
    )

    return render(
        request,
        'wiki/article_version.html',
        {
            'version': version
        }
    )