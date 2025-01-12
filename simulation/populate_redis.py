import redis
from faker import Faker
import random
import hashlib

# Establishing the Redis connection
r = redis.Redis(host='localhost', port=6379, db=0)

# Initialize Faker to generate fake data
faker = Faker()

# Lists of categories, companies, and item names
categories = ['Electronics', 'Clothing', 'Groceries', 'Furniture', 'Toys', 'Sports', 'Books', 'Beauty']
companies = ['Apple', 'Samsung', 'Nike', 'Sony', 'LG', 'Adidas', 'IKEA', 'Amazon', 'Walmart']

item_names = {
    'Electronics': ['Laptop', 'Smartphone', 'Tablet', 'Headphones', 'Smartwatch', 'TV', 'Camera', 'Speaker'],
    'Clothing': ['T-shirt', 'Jeans', 'Jacket', 'Sweater', 'Skirt', 'Dress', 'Shoes', 'Scarf'],
    'Groceries': ['Rice', 'Wheat Flour', 'Sugar', 'Salt', 'Tea', 'Coffee', 'Milk', 'Butter'],
    'Furniture': ['Sofa', 'Chair', 'Table', 'Cupboard', 'Bed', 'Dresser', 'Shelf', 'Armchair'],
    'Toys': ['Lego', 'Action Figure', 'Doll', 'Puzzle', 'Board Game', 'Teddy Bear', 'Car Toy', 'Drone'],
    'Sports': ['Football', 'Basketball', 'Tennis Racket', 'Baseball Bat', 'Golf Club', 'Badminton Racket', 'Soccer Ball', 'Table Tennis Paddle'],
    'Books': ['Novel', 'Textbook', 'Magazine', 'Biography', 'Cookbook', 'Comic', 'Poetry', 'Guidebook'],
    'Beauty': ['Shampoo', 'Conditioner', 'Lipstick', 'Perfume', 'Body Lotion', 'Face Mask', 'Nail Polish', 'Hair Gel']
}

def generate_item_id(category, item_name, company_name):
    """
    Generate a consistent unique item_id based on category, item name, and company name.
    """
    unique_string = f"{category}:{item_name}:{company_name}"
    return hashlib.sha256(unique_string.encode()).hexdigest()[:16]  # Truncate for brevity

# Function to populate the inventory in Redis
def populate_inventory(r):
    # Clear the existing inventory (redis doesn't have a "truncate", so we manually remove keys)
    for key in r.scan_iter("inventory:*"):
        r.delete(key)

    # Loop through each category
    for category in categories:
        # Get the list of items for this category
        items_in_category = item_names.get(category, [])

        # For each item, link it to all brands
        for item_name in items_in_category:
            for company_name in companies:
                # Generate a unique item_id for each item-brand combination
                item_id = generate_item_id(category, item_name, company_name)

                # Generate a unique key for each item
                item_key = f"inventory:{item_id}"

                # Generate random stock quantity and reorder level
                stock_quantity = random.randint(10, 1000)
                reorder_level = random.randint(5, 100)

                # Use a hash in Redis to store the item's data
                r.hset(item_key, mapping={
                    "item_id": item_id,
                    "category": category,
                    "item_name": item_name,
                    "company_name": company_name,
                    "stock_quantity": stock_quantity,
                    "reorder_level": reorder_level
                })

    print(f"Inventory populated with {sum(len(items) * len(companies) for items in item_names.values())} items.")

# Call the function to populate the inventory
populate_inventory(r)
