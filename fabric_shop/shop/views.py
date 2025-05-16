from django.shortcuts import render, get_object_or_404, redirect
from django.shortcuts import render
from .models import SliderImage, Category, Subcategory, Product, ProductComment
from rapidfuzz import fuzz
from django.conf import settings
from .forms import ProductCommentForm
from django.core.paginator import Paginator





def home(request):
    slides = SliderImage.objects.order_by('order')
    categories = Category.objects.all()
    context = {
        'slides': slides,
        'active_page': 'home',
        'categories': categories,
        'MEDIA_URL': settings.MEDIA_URL,
    }
    return render(request, 'shop/home.html', context)


def category_detail(request, slug):
    category = get_object_or_404(Category, slug=slug)
    subcategories = category.subcategories.all()
    return render(request, 'shop/category_detail.html', {
        'category': category,
        'subcategories': subcategories
    })

def subcategory_detail(request, slug):
    subcategory = get_object_or_404(Subcategory, slug=slug)
    products = subcategory.products.all()
    return render(request, 'shop/subcategory_detail.html', {
        'subcategory': subcategory,
        'products': products
    })


def product_detail(request, slug):
    product = get_object_or_404(Product, slug=slug)
    variants = product.variants.all() if product.has_variants else []

    show_color = any(v.color for v in variants)
    show_size = any(v.size for v in variants)

    unique_colors = sorted(set(v.color for v in variants if v.color))
    unique_sizes = sorted(set(v.size for v in variants if v.size))

    selected_color = request.GET.get("color", "")
    selected_size = request.GET.get("size", "")

    # Обробка коментарів
    comments = ProductComment.objects.filter(product=product)
    paginator = Paginator(comments, 5)
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)

    if request.method == "POST" and request.user.is_authenticated:
        form = ProductCommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.product = product
            comment.user = request.user
            comment.save()
            return redirect('shop:product_detail', slug=slug)
    else:
        form = ProductCommentForm()

    context = {
        'product': product,
        'variants': variants,
        'show_color': show_color,
        'show_size': show_size,
        'unique_colors': unique_colors,
        'unique_sizes': unique_sizes,
        'selected_color': selected_color,
        'selected_size': selected_size,
        'form': form,
        'page_obj': page_obj,
    }

    return render(request, 'shop/product_detail.html', context)





def search(request):
    query = request.GET.get('q', '').strip()
    products = []

    if query:
        all_products = Product.objects.all()
        matched = []

        for product in all_products:
            name_score = fuzz.partial_ratio(query.lower(), product.name.lower())
            description_words = product.description.split() if product.description else []
            desc_score = max(
                [fuzz.partial_ratio(query.lower(), word.lower()) for word in description_words],
                default=0
            )
            max_score = max(name_score, desc_score)

            if max_score > 80:
                matched.append((product, max_score))

        # Сортуємо за max_score у зворотному порядку
        matched.sort(key=lambda x: x[1], reverse=True)

        # Витягуємо продукти зі списку кортежів
        products = [item[0] for item in matched]

    return render(request, 'shop/search_results.html', {
        'query': query,
        'products': products,
    })