from django.views import generic
from django.shortcuts import render
from product.models import Product, ProductVariant, ProductVariantPrice, Variant, ProductImage
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from django.http import Http404

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework.authentication import SessionAuthentication
from product.serializers import ProductVariantPriceSerializer, ProductVariantSerializer, ProductImageSerializer, ProductSerializer, VariantSerializer

class CreateProductView(generic.TemplateView):
    template_name = 'products/create.html'

    def get_context_data(self, **kwargs):
        context = super(CreateProductView, self).get_context_data(**kwargs)
        variants = Variant.objects.filter(active=True).values('id', 'title')
        context['product'] = True
        context['variants'] = list(variants.all())
        return context
    

class ProductListView(generic.TemplateView):
    template_name = 'products/list.html'
    products_per_page = 2

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        all_products = Product.objects.all()

        title = self.request.GET.get('title')
        pro_variant = self.request.GET.get('product_variant')
        price_from = self.request.GET.get('price_from')
        price_to = self.request.GET.get('price_to')
        date = self.request.GET.get('date')


        if title:
            all_products = Product.objects.filter(title__icontains=title)
        elif pro_variant:
            all_products = Product.objects.filter(productvariant__variant_title=pro_variant)
        elif price_from:
            all_products = Product.objects.filter(productvariantprice__price__gte=float(price_from))
        elif price_to:
            all_products = Product.objects.filter(productvariantprice__price__lte=float(price_to))
        elif date:
            all_products = Product.objects.filter(created_at__date = date)


        paginator = Paginator(all_products, self.products_per_page)
        page_number = self.request.GET.get('page')

        try:
            page_obj = paginator.get_page(page_number)
        except EmptyPage:
            raise Http404("Page not found")
        
        context['products'] = page_obj
        context['page_obj'] = page_obj
        context['products_count'] = all_products.count()
        return context



    

class ProductSaveAPIView(APIView):
    permission_classes = [IsAuthenticated, IsAdminUser]
    authentication_classes = [SessionAuthentication]
    def post(self, request):
        # Get the data from the request
        data = request.data

        # Extract the required data from the payload
        product_data = {
            'title': data['title'],
            'sku': data['sku'],
            'description': data['description'],
        }
        product_images_data = data.get('product_image', [])
        product_variant_data = data.get('product_variant', [])
        product_variant_prices_data = data.get('product_variant_prices', [])


        # Create the Product object
        product_serializer = ProductSerializer(data=product_data)

        if product_serializer.is_valid():
            product_instance = product_serializer.save()

            if product_images_data:
                # Create ProductImage objects
                for image_data in product_images_data:
                    image_data['product'] = product_instance.id
                    product_image_serializer = ProductImageSerializer(data=image_data)
                    if product_image_serializer.is_valid():
                        product_image_serializer.save()
            if product_variant_data:
                # Create ProductVariant and ProductVariantPrice objects
                for variant_data in product_variant_data:
                    variant_data['product'] = product_instance.id
                    variant_serializer = ProductVariantSerializer(data=variant_data)
                    if variant_serializer.is_valid():
                        variant_instance = variant_serializer.save()

                        for price_data in product_variant_prices_data:
                            price_data['product'] = product_instance.id
                            price_data['product_variant'] = variant_instance.id
                            product_variant_price_serializer = ProductVariantPriceSerializer(data=price_data)
                            if product_variant_price_serializer.is_valid():
                                product_variant_price_serializer.save()

            return Response(product_serializer.data, status=status.HTTP_201_CREATED)

        return Response(product_serializer.errors, status=status.HTTP_400_BAD_REQUEST)