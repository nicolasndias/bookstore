from django.test import TestCase

from product.factories import CategoryFactory, ProductFactory
from product.serializers import CategorySerializer, ProductSerializer


class CategorySerializerTests(TestCase):
    def test_expected_fields(self):
        category = CategoryFactory(title="Books")
        data = CategorySerializer(category).data
        self.assertEqual(set(data.keys()), {"id", "title", "slug", "description", "active"})

    def test_valid_category_data(self):
        serializer = CategorySerializer(data={
            "title": "Fiction", "slug": "fiction", "description": "Fiction books", "active": True
        })
        self.assertTrue(serializer.is_valid(), serializer.errors)

    def test_required_fields(self):
        serializer = CategorySerializer(data={})
        self.assertFalse(serializer.is_valid())
        self.assertIn("title", serializer.errors)
        self.assertIn("slug", serializer.errors)


class ProductSerializerTests(TestCase):
    def test_expected_fields_and_nested_category(self):
        category = CategoryFactory(title="Books")
        product = ProductFactory(title="Book", price=50, category=[category])
        data = ProductSerializer(product).data
        self.assertEqual(set(data.keys()), {"id", "title", "description", "price", "active", "category"})
        self.assertEqual(data["category"][0]["title"], category.title)

    def test_create_product_with_categories(self):
        category1 = CategoryFactory()
        category2 = CategoryFactory()
        serializer = ProductSerializer(data={
            "title": "New book", "price": 30, "categories_id": [category1.id, category2.id]
        })
        self.assertTrue(serializer.is_valid(), serializer.errors)
        product = serializer.save()
        self.assertEqual(product.title, "New book")
        self.assertEqual(set(product.category.all()), {category1, category2})

    def test_invalid_category_id(self):
        serializer = ProductSerializer(data={"title": "Book", "price": 20, "categories_id": [999999]})
        self.assertFalse(serializer.is_valid())
        self.assertIn("categories_id", serializer.errors)

    def test_title_is_required(self):
        serializer = ProductSerializer(data={"price": 20})
        self.assertFalse(serializer.is_valid())
        self.assertIn("title", serializer.errors)
