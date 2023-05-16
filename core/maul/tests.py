from django.urls import reverse_lazy
from rest_framework.test import APITestCase

from .models import Brand, Category, Product


def format_datetime(value):
    """This method will format the date to be readable for the json response"""
    return value.strftime("%Y-%m-%dT%H:%M:%S.%fZ")


class TestBrand(APITestCase):
    """All tests for Brand model will go here"""
    url = reverse_lazy("brand-list")

    def test_list(self):
        brand = Brand.objects.create(name="Test brand")

        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)

        expected = [{
            "name": brand.name,
            "date_created": format_datetime(brand.date_created),
        }]

        self.assertEqual(response.json()["results"], expected)

    def test_create(self):
        self.assertFalse(Brand.objects.exists())
        response = self.client.post(self.url, data={"name": "Test created brand"})
        self.assertEqual(response.status_code, 405)
        self.assertFalse(Brand.objects.exists())


class TestCategory(APITestCase):
    """All tests for Category model will go here"""
    url = reverse_lazy("category-list")

    def test_list(self):
        category = Category.objects.create(name="Test Category")

        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)

        expected = [{
            "name": category.name,
            "date_created": format_datetime(category.date_created),
        }]

        self.assertEqual(response.json()["results"], expected)

    def test_create(self):
        self.assertFalse(Category.objects.exists())
        response = self.client.post(self.url, data={"name": "Test created category"})
        self.assertEqual(response.status_code, 405)
        self.assertFalse(Category.objects.exists())


class TestProduct(APITestCase):
    """All tests for Product model will go here"""
    list_url = reverse_lazy("product-list")

    def test_list(self):
        brand = Brand.objects.create(name="Test brand")
        category = Category.objects.create(name="Test Category")
        product = Product.objects.create(ean=355,
                                         name="Test product",
                                         link_url="test link url",
                                         img_url="test img url",
                                         quantity="Too heavy",
                                         brand=Brand.objects.get(name=brand),
                                         )
        product.categories.set(Category.objects.filter(id__in=[1, 2, 3]))

        response = self.client.get(self.list_url)
        self.assertEqual(response.status_code, 200)

        expected = [{
            "ean": product.ean,
            "name": product.name,
            "link_url": product.link_url,
            "img_url": product.img_url,
            "quantity": product.quantity,
            "brand": {
                "name": brand.name,
                "date_created": format_datetime(brand.date_created),
            },
            "categories": [{
                "name": category.name,
                "date_created": format_datetime(category.date_created),
            }],
            "date_created": format_datetime(product.date_created),
        }]

        self.assertEqual(response.json()["results"], expected)

    def test_create(self):
        self.assertFalse(Product.objects.exists())
        response = self.client.post(self.list_url, data={"name": "Test created product"})
        self.assertEqual(response.status_code, 405)
        self.assertFalse(Product.objects.exists())
