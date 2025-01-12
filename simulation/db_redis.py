import redis
import json
from datetime import datetime

# Connect to Redis
redis_host = "localhost"
redis_port = 6379
redis_db = 0

try:
    # Create a Redis connection
    r = redis.StrictRedis(host=redis_host, port=redis_port, db=redis_db, decode_responses=True)

    # Helper function to add data to Redis
    def create_inventory_item(item_id, item_name, company_name, category, stock_quantity, reorder_level):
        inventory_key = f"inventory:{item_id}"
        inventory_data = {
            "item_id": item_id,
            "item_name": item_name,
            "company_name": company_name,
            "category": category,
            "stock_quantity": stock_quantity,
            "reorder_level": reorder_level,
            "created_at": str(datetime.now()),
            "updated_at": str(datetime.now())
        }
        r.hset(inventory_key, mapping=inventory_data)  # Store the item in Redis as a hash

    def create_inventory_transaction(transaction_id, item_id, transaction_type, quantity, notes):
        transaction_key = f"transaction:{transaction_id}"
        transaction_data = {
            "transaction_id": transaction_id,
            "item_id": item_id,
            "transaction_type": transaction_type,
            "quantity": quantity,
            "transaction_date": str(datetime.now()),
            "notes": notes
        }
        r.hset(transaction_key, mapping=transaction_data)  # Store the transaction in Redis as a hash

    def create_sale(sale_id, item_id, quantity, price):
        sale_key = f"sale:{sale_id}"
        sale_data = {
            "sale_id": sale_id,
            "item_id": item_id,
            "quantity": quantity,
            "sale_date": str(datetime.now()),
            "price": price
        }
        r.hset(sale_key, mapping=sale_data)  # Store the sale in Redis as a hash

    def create_prediction(prediction_id, item_id, predicted_depletion_date, current_quantity, confidence):
        prediction_key = f"prediction:{prediction_id}"
        prediction_data = {
            "prediction_id": prediction_id,
            "item_id": item_id,
            "predicted_depletion_date": str(predicted_depletion_date),
            "current_quantity": current_quantity,
            "confidence": confidence,
            "created_at": str(datetime.now())
        }
        r.hset(prediction_key, mapping=prediction_data)  # Store the prediction in Redis as a hash

    # Sample data (these would typically come from elsewhere)
    create_inventory_item(1, "Item A", "Company A", "Category 1", 100, 20)
    create_inventory_transaction(1, 1, "restock", 50, "Restocked due to low stock")
    create_sale(1, 1, 10, 19.99)
    create_prediction(1, 1, "2025-01-01", 80, 0.95)

    print("Data inserted successfully into Redis!")

except Exception as e:
    print(f"Error: {e}")
