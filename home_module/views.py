from django.db.models import ExpressionWrapper, F, DecimalField, Count
from django.http import HttpRequest, HttpResponse
from django.shortcuts import render, redirect
from django.urls import reverse
from django.utils import timezone
from django.views import View
from django.views.generic import TemplateView
from product_module.models import ProductCategory, Product


# Create your views here.

class HomeView(TemplateView):
    template_name = 'home_module/home_page.html'

    def get_context_data(self, **kwargs):
        context = super(HomeView, self).get_context_data(**kwargs)
        discounted_product = Product.objects.filter(
            discount_price__isnull=False,
            start_discount__lte=timezone.now(),
            end_discount__gte=timezone.now(),
            is_active=True,
            is_deleted=False
        ).annotate(check_percent=ExpressionWrapper(
            (F('price') - F('discount_price')) / F('price') * 100, output_field=DecimalField())
        ).order_by('check_percent')
        # print(discounted_product)

        # for product in discounted_product:
        #     if product.check_discount_time():
        #         delta = product.end_discount - product.start_discount
        #         time_to_left = int(delta.total_seconds() / 60)
        #         context['discounted_product'] = product
        #         context['time_to_left'] = time_to_left
        #         dis_pro = product
        #         break
        #
        #     else:
        #         context['discounted_product'] = None
        #         product.end_discount = None
        #         product.start_discount = None
        #         product.discount_price = None
        #         product.save()
        if discounted_product:
            delta = discounted_product[0].end_discount - discounted_product[0].start_discount
            time_to_left = int(delta.total_seconds() / 60)
            context['discounted_product'] = discounted_product[0]
            context['time_to_left'] = time_to_left
        else:
            context['discounted_product'] = None

        most_viewed_product = Product.objects.filter(is_active=True, is_deleted=False).annotate(visit_count=Count('productvisit')).order_by('-visit_count')[:12]
        context['most_viewed_product'] = most_viewed_product

        mobile = Product.objects.filter(is_active=True, category__slug__iexact='mobile', is_deleted=False)[:12]
        context['mobile'] = mobile

        return context

def searching(request: HttpRequest):
    search_text = request.GET.get('q', '')
    print(search_text)
    if search_text:
        products = Product.objects.filter(name__contains=search_text, is_active=True, is_deleted=False) or Product.objects.filter(slug__contains=search_text, is_active=True, is_deleted=False)
        context = {
            'products': products,
            'search_text': search_text
        }
        return render(request, 'home_module/searching_page.html', context)

    return redirect(reverse('home_page'))


def header_components(request):
    categories = ProductCategory.objects.filter(is_active=True, parent__isnull=True)
    # cat = categories[1]
    # cats = cat.productcategory_set.all()
    # print(cats)
    context = {
        'categories': categories,
    }
    return render(request, 'header_components.html', context)

def footer_components(request):
    return render(request, 'footer_components.html')