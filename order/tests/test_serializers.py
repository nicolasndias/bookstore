from django.test import TestCase

from order.factories import UserFactory
from order.models import Order
from order.serializers.order_serializer import OrderSerializer
from product.factories import ProductFactory


class OrderSerializerTests(TestCase):
    def test_expected_fields_and_nested_products(self):
        product = ProductFactory(title="Mouse", price=100)
        order = Order.objects.create(user=UserFactory())
        order.product.add(product)
        data = OrderSerializer(order).data
        self.assertEqual(set(data.keys()), {"id", "product", "total", "user"})
        self.assertEqual(data["product"][0]["title"], product.title)
        self.assertEqual(data["total"], 100)

    def test_create_order_with_products(self):
        user = UserFactory()
        product1 = ProductFactory(price=100)
        product2 = ProductFactory(price=50)
        serializer = OrderSerializer(data={"user": user.id, "products_id": [product1.id, product2.id]})
        self.assertTrue(serializer.is_valid(), serializer.errors)
        order = serializer.save()
        self.assertEqual(order.user, user)
        self.assertEqual(set(order.product.all()), {product1, product2})
        self.assertEqual(OrderSerializer(order).data["total"], 150)

    def test_invalid_product_id(self):
        user = UserFactory()
        serializer = OrderSerializer(data={"user": user.id, "products_id": [999999]})
        self.assertFalse(serializer.is_valid())
        self.assertIn("products_id", serializer.errors)

    def test_required_fields(self):
        serializer = OrderSerializer(data={})
        self.assertFalse(serializer.is_valid())
        self.assertIn("user", serializer.errors)
        self.assertIn("products_id", serializer.errors)
