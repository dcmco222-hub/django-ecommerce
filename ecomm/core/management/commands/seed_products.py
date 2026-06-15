from django.core.management.base import BaseCommand
from core.models import Category, Product
from random import randint, choice


class Command(BaseCommand):
    help = "Seed products"

    def handle(self, *args, **kwargs):

        data = {

            "Electronics": [
                "iPhone 15 Pro",
                "Samsung Galaxy S24",
                "MacBook Air M3",
                "Dell XPS 13",
                "AirPods Pro",
                "Apple Watch Series 9",
                "JBL Flip 6",
                "Sony WH-1000XM5",
                "iPad Air",
                "Logitech MX Master 3S",
                "Anker Power Bank",
                "Canon EOS R50",
                "GoPro Hero 12",
                "Lenovo ThinkPad X1",
                "ASUS Zenbook"
            ],

            "Gaming": [
                "PlayStation 5",
                "Xbox Series X",
                "Nintendo Switch OLED",
                "Steam Deck",
                "ROG Ally",
                "DualSense Controller",
                "Gaming Keyboard",
                "Gaming Mouse",
                "Gaming Chair",
                "Elgato Stream Deck"
            ],

            "Fashion": [
                "Oversized Hoodie",
                "Denim Jacket",
                "Cargo Pants",
                "Leather Sneakers",
                "Polo Shirt",
                "Running Shoes",
                "Wrist Watch",
                "Sunglasses",
                "Leather Belt",
                "Backpack",
                "Beanie",
                "Joggers",
                "Flannel Shirt",
                "Chelsea Boots",
                "Formal Shoes"
            ],

            "Home & Kitchen": [
                "Air Fryer",
                "Rice Cooker",
                "Microwave Oven",
                "Electric Kettle",
                "Coffee Maker",
                "Standing Fan",
                "Vacuum Cleaner",
                "Toaster",
                "Water Dispenser",
                "Blender"
            ],

            "Books": [
                "Atomic Habits",
                "Deep Work",
                "Clean Code",
                "Rich Dad Poor Dad",
                "The Psychology of Money",
                "The Lean Startup",
                "Zero To One",
                "Think and Grow Rich",
                "The Pragmatic Programmer",
                "7 Habits of Highly Effective People"
            ]
        }

        for category_name, products in data.items():

            category, created = Category.objects.get_or_create(
                name=category_name,
                slug=category_name.lower().replace(" ", "-")
            )

            for product_name in products:

                Product.objects.get_or_create(

                    name=product_name,

                    defaults={

                        "category": category,

                        "slug": (
                            product_name.lower()
                            .replace(" ", "-")
                            .replace("&", "")
                        ),

                        "description":
                            f"Premium quality {product_name}. "
                            f"Perfect for everyday use.",

                        "price": randint(
                            5000,
                            500000
                        ),

                        "stock": randint(
                            5,
                            100
                        ),

                        "available": True,

                        # IMPORTANT
                        "image": "products/default.jpg",
                    }
                )

        self.stdout.write(
            self.style.SUCCESS(
                "Products seeded successfully!"
            )
        )