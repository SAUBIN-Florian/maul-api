import csv
from django.shortcuts import redirect
from django.contrib.auth.decorators import user_passes_test

from rest_framework.viewsets import ReadOnlyModelViewSet
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.decorators import authentication_classes, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.authentication import JWTAuthentication

from .models import Brand, Category, Product
from .serializers import BrandSerializer, CategorySerializer, ProductSerializer


@user_passes_test(lambda user: user.is_superuser, login_url="admin/")
def insert_data(request):

    """Populate database with csv file"""
    with open("../maul_data.csv", "r") as file:
        reader = csv.reader(file, delimiter="\t")

        # Skip the first line (header row)
        next(reader)

        print("Inserting data...")
        for row in reader:
            count = 0
            new_brand = row[4].capitalize()
            new_categories = row[5].split(",")

            if Brand.objects.filter(name=new_brand).exists():
                brand = Brand.objects.get(name=new_brand)
            else:
                brand = Brand.objects.create(name=new_brand)

            categories = []
            for cat in new_categories:
                if Category.objects.filter(name=cat).exists():
                    categories.append(Category.objects.get(name=cat))
                else:
                    categories.append(Category.objects.create(name=cat))

            if row[0].isdigit():
                product = Product.objects.create(
                    ean=row[0],
                    name=row[2],
                    link_url=row[1],
                    img_url=row[7],
                    quantity=row[3],
                    brand=brand,
                )
                product.categories.add(*categories)
                count += 1

        print("Database all set !")
        return redirect("retail:index")


@authentication_classes([JWTAuthentication])
@permission_classes([IsAuthenticated])
class APIIndex(APIView):
    def get(self, request):
        version = "1.0.0"
        data = {
            "version": version,
            "number_of_products": Product.objects.count(),
            "number_of_brands": Brand.objects.count(),
            "number_of_categories": Category.objects.count(),
            "info": "This API was created to allow developers to access "
                    "products present in retails in France, classified by brands and categories."
        }
        return Response(data)


@authentication_classes([JWTAuthentication])
@permission_classes([IsAuthenticated])
class BrandApiView(ReadOnlyModelViewSet):

    serializer_class = BrandSerializer

    def get_queryset(self):
        brands = Brand.objects.all()
        queryset = brands[:100]

        brand_name = self.request.GET.get("name")
        if brand_name is not None:
            queryset = brands.filter(name__contains=brand_name)

        return queryset


@authentication_classes([JWTAuthentication])
@permission_classes([IsAuthenticated])
class CategoryApiView(ReadOnlyModelViewSet):

    serializer_class = CategorySerializer

    def get_queryset(self):
        categories = Category.objects.all()
        queryset = categories[:100]

        category_name = self.request.GET.get("name")
        if category_name is not None:
            queryset = categories.filter(name__contains=category_name)

        return queryset


@authentication_classes([JWTAuthentication])
@permission_classes([IsAuthenticated])
class ProductApiView(ReadOnlyModelViewSet):

    serializer_class = ProductSerializer

    def get_queryset(self):
        products = Product.objects.all()
        queryset = products[:100]

        # Query products by EAN ex: https://my_api/api/product/?ean=my_product_ean/
        product_ean = self.request.GET.get("ean")
        if product_ean is not None:
            queryset = products.filter(ean__exact=product_ean)

        # Query products by name ex: https://my_api/api/product/?name=my_product_name/
        product_name = self.request.GET.get("name")
        if product_name is not None:
            queryset = products.filter(name__contains=product_name)

        # Query products by brand ex: https://my_api/api/product/?brand=my_product_brand/
        product_brand = self.request.GET.get("brand")
        if product_brand is not None:
            queryset = products.filter(brand__name__exact=product_brand)

        # Query products by list of categories ex: https://my_api/api/product/?categories=my_product_categories_list/
        product_category = self.request.GET.get("categories")
        if product_category is not None:
            cat_list = product_category.split(",")
            queryset = products.filter(categories__name__in=cat_list)

        return queryset
