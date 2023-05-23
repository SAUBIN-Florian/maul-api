from rest_framework.serializers import ModelSerializer

from .models import Brand, Category, Product


class BrandSerializer(ModelSerializer):

    class Meta:
        model = Brand
        fields = ["name", "date_created"]


class CategorySerializer(ModelSerializer):

    class Meta:
        model = Category
        fields = ["name", "date_created"]


class ProductSerializer(ModelSerializer):

    brand = BrandSerializer()
    categories = CategorySerializer(many=True)

    class Meta:
        model = Product
        fields = ["ean", "name", "link_url", "img_url", "quantity", "brand", "categories", "date_created"]
