from blog.models import Post, Category
from Marketing.forms import SubscriberForm
from django.db.models import Count, Q

def counting_categories():
    queryset = Post\
        .objects.values('category__name')\
        .annotate(Count('category'))
    return queryset


def get_context(request):
    posts = Post.objects.all().order_by('-date_posted')
    form = SubscriberForm(request.POST or None)
    categories = Category.objects.all()
    latest_posts = posts[:4]
    category_counting = counting_categories()
    context = {'posts': posts,
               'categories': categories,
               'latest_posts': latest_posts,
               'category_counting': counting_categories,
               'form': form,
               }
    return context


def process_post_request(request, form):
    if form.is_valid():
        form.save()
        messages.success(request, "Thank You for your subcription to the newsletter")
        return redirect('/')