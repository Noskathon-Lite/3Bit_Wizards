import time
import redis
import random
from datetime import datetime, timedelta
import json
import hashlib
from faker import Faker

# Connect to Redis
redis_host = "localhost"
redis_port = 6379
redis_db = 0
r = redis.StrictRedis(host=redis_host, port=redis_port, decode_responses=True)

# Initialize Faker
faker = Faker()

def initialize_inventory(r):
    """Initialize inventory in Redis if it doesn't exist."""
    if not list(r.scan_iter("inventory:*")):
        print("Initializing inventory...")
        for i in range(10):  # Add 10 random items
            item_id = f"item_{i + 1}"
            inventory_key = f"inventory:{item_id}"
            r.hset(inventory_key, mapping={
                "item_id": item_id,
                "item_name": faker.word(),
                "company_name": faker.company(),
                "category": random.choice(["electronics", "clothing", "toys"]),
                "stock_quantity": random.randint(50, 200),
                "reorder_level": random.randint(10, 30),
                "updated_at": str(datetime.now())
            })
        print("Inventory initialized.")

def simulate_transactions(r):
    """Simulate random transactions and update inventory in Redis."""
    keys = list(r.scan_iter("inventory:*"))  # Get all inventory keys
    if not keys:
        print("No inventory found.")
        return

    for _ in range(20):
        try:
            # Pick a random inventory item
            inventory_key = random.choice(keys)
            item_data = r.hgetall(inventory_key)

            if not item_data:
                continue

            # Extract item details
            item_id = item_data["item_id"]
            stock_quantity = int(item_data["stock_quantity"])
            transaction_type = random.choice(["sale", "restock", "adjustment"])
            quantity = random.randint(1, 20)

            if transaction_type == "sale":
                if stock_quantity >= quantity:
                    stock_quantity -= quantity
                else:
                    continue  # Skip if not enough stock
            elif transaction_type == "restock":
                stock_quantity += quantity
            elif transaction_type == "adjustment":
                adjustment = random.choice([-1, 1]) * quantity
                stock_quantity = max(0, stock_quantity + adjustment)

            # Update stock in Redis
            r.hset(inventory_key, mapping={
                "stock_quantity": stock_quantity,
                "updated_at": str(datetime.now())
            })

            # Log the transaction
            transaction_id = hashlib.md5(f"{item_id}{datetime.now()}".encode()).hexdigest()
            transaction_key = f"transaction:{transaction_id}"
            r.hset(transaction_key, mapping={
                "item_id": item_id,
                "transaction_type": transaction_type,
                "quantity": quantity,
                "notes": faker.sentence(),
                "transaction_date": str(datetime.now())
            })

        except Exception as e:
            print(f"Error in simulate_transactions: {e}")

def simulate_ml_predictions(r):
    """Simulate ML predictions and store in Redis."""
    try:
        keys = list(r.scan_iter("inventory:*"))
        if not keys:
            print("No inventory found for predictions.")
            return

        for inventory_key in keys:
            item_data = r.hgetall(inventory_key)
            if not item_data:
                continue

            # Simulate ML predictions
            item_id = item_data["item_id"]
            stock_quantity = int(item_data["stock_quantity"])
            depletion_date = datetime.now() + timedelta(days=random.randint(1, 10))
            confidence = round(random.uniform(0.7, 0.95), 2)

            # Store the prediction
            prediction_id = hashlib.md5(f"{item_id}{datetime.now()}".encode()).hexdigest()
            prediction_key = f"prediction:{prediction_id}"
            r.hset(prediction_key, mapping={
                "item_id": item_id,
                "predicted_depletion_date": depletion_date.isoformat(),
                "current_quantity": stock_quantity,
                "confidence": confidence,
                "created_at": str(datetime.now())
            })

    except Exception as e:
        print(f"Error in simulate_ml_predictions: {e}")

# Infinite loop for periodic updates
try:
    initialize_inventory(r)  # Ensure inventory exists
    while True:
        print("Simulating transactions...")
        simulate_transactions(r)

        print("Simulating ML predictions...")
        simulate_ml_predictions(r)

        print("Redis database updated. Waiting 10 seconds for the next cycle...")
        time.sleep(10)  # 10 second delay
except KeyboardInterrupt:
    print("Simulation stopped.")
except Exception as e:
    print(f"Unexpected error: {e}")
