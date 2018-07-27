from article.models import Article, Category

from django.views import View
from django.shortcuts import render, get_object_or_404


def get_hot_articles(number):
    return Article.objects.filter(is_public=True)[:number]


def fetch_category_articles(category_name, number):
    return Category.objects.get(name=category_name). \
               article_set.filter(is_public=True).all()[:number]


class IndexView(View):
    template_name = 'index.html'

    def get(self, request):
        context = {
            'second_articles': Article.objects.filter(is_public=True)[:6],
            'paper_articles': fetch_category_articles('物联网学报', 3),
            'session_articles': fetch_category_articles('会展', 4),
            'boss_articles': fetch_category_articles('大咖视点', 4)
        }
        return render(request, self.template_name, context)


class DetailView(View):
    template_name = 'detail.html'

    def get(self, request, pk):
        context = {
            'article': get_object_or_404(Article, is_public=True, pk=pk),
            'hot_articles': get_hot_articles(6),
            'recomment_articles': Article.objects.filter(is_public=True)[:5],
        }

        return render(request, self.template_name, context)


class ListView(View):
    template_name = 'list.html'

    def get(self, request):
        category_name = request.GET.get('category')
        category = get_object_or_404(Category, name=category_name)
        articles = category.article_set.filter(is_public=True).all()
        context = {
            'articles': articles,
            'hot_articles': get_hot_articles(6),
            'news_articles': Article.objects.filter(is_public=True)[:4],
            'tech_articles': fetch_category_articles('前沿科技', 4),
            'net_articles': fetch_category_articles('网络技术', 4),
        }
        return render(request, self.template_name, context)
