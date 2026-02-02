from django.http import HttpRequest, Http404, HttpResponse, JsonResponse
from django.shortcuts import render, redirect
from django.template.context_processors import request
from django.urls import reverse
from django.views.generic import TemplateView, ListView, DetailView

from product_module.forms import CommentForm
from product_module.models import Product, ProductCategory, ProductSpecification, ProductSpecificationGroup, \
    ProductComment, ProductVisit
from utils.http_service import get_client_ip


# Create your views here.

class ProductListView(ListView):
    template_name = 'product_module/products_list.html'
    model = Product
    context_object_name = 'products_list'

    # def get_context_data(self, **kwargs):
    #     context = super(ProductListView, self).get_context_data(**kwargs)
    #     cat = self.kwargs['cat']
    #     query = Product.objects.filter(category__slug__iexact=cat)
    #     context['product_list'] = query
    #     return context

    def get_context_data(self, **kwargs):
        context = super(ProductListView, self).get_context_data(**kwargs)
        category_name = self.kwargs.get('cat')
        category = ProductCategory.objects.filter(slug__iexact=category_name).first()
        context['category'] = category
        return context

    def get_queryset(self):
        category_name = self.kwargs.get('cat')
        query = Product.objects.filter(category__slug__iexact=category_name, is_active=True, is_deleted=False)
        return query

# def product_list(request, cat):
#     if cat == 'mobile':
#         return render(request, 'product_module/products_list.html', {})
#
#     raise Http404()


class ProductDetailView(DetailView):
    Template_name = 'product_module/product_detail.html'
    model = Product
    context_object_name = 'product'

    def get_context_data(self, **kwargs):
        product = self.object
        context = super(ProductDetailView, self).get_context_data(**kwargs)
        specification_group = ProductSpecificationGroup.objects.filter(productspecification__product_id=self.object.id).distinct()
        context['specification_group'] = specification_group
        related_products = Product.objects.filter(brand=product.brand, category=product.category, is_active=True, is_deleted=False).exclude(pk=product.pk)[:10]
        context['related_products'] = related_products
        comments = ProductComment.objects.filter(product_id=product.id, parent__isnull=True).prefetch_related('productcomment_set').order_by('create_date')
        context['comments'] = comments
        comment_form = CommentForm()
        context['comment_form'] = comment_form
        user_ip = get_client_ip(self.request)
        user_id = None
        if self.request.user.is_authenticated:
            user_id = self.request.user.id

        has_been_visited = ProductVisit.objects.filter(ip__iexact=user_ip, product_id=product.id).exists()
        if not has_been_visited:
            new_visit = ProductVisit(ip=user_ip, product_id=product.id)
            new_visit.save()

        # print(related_products)
        return context

def add_comment(request: HttpRequest):
    if not request.user.is_authenticated:
        return JsonResponse({'error': 'auth'}, status=403)

    if request.method != 'POST':
        return JsonResponse({'error': 'method'}, status=405)

    comment_form = CommentForm(request.POST)
    if not comment_form.is_valid():
        return JsonResponse({'errors': comment_form.errors}, status=400)

    text = comment_form.cleaned_data['comment']
    product_id = request.POST.get('product_id')
    parent_id = request.POST.get('parent_id')
    new_comment = ProductComment(text=text, parent_id=parent_id, product_id=product_id, user_id=request.user.id)
    new_comment.save()
    context = {
        'comments': ProductComment.objects.filter(product_id=product_id, parent__isnull=True).prefetch_related('productcomment_set').order_by('create_date'),
        'comment_form': comment_form,
    }
    return render(request, 'product_module/includes/product_comment_partial.html', context)
    print(request.GET)
    return HttpResponse('add comment')

