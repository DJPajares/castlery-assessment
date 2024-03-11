import os
import csv
import json
import requests


def get_item_details(item_id):
  url = f"https://fakestoreapi.com/products/{item_id}"
  response = requests.get(url)
  return response.json()


def process_order_details(csv_file):
  orders = {}
  dump_folder = 'orders'
  os.makedirs(dump_folder, exist_ok=True)

  with open(csv_file, 'r') as file:
    reader = csv.reader(file, delimiter='|')
    current_order = None

    for row in reader:
      if row[0].strip() == 'Header':
        order_number = row[1].strip()
        customer_name = row[2].strip()
        delivery_postal = row[3].strip()
        current_order = {
            "order_number": order_number,
            "customer_name": customer_name,
            "delivery_postal": delivery_postal,
            "item_lines": [],
            "total_price": 0,
            "unique_items": 0
        }
        orders[order_number] = current_order

      elif row[0].strip() == 'Line':
        item_id = row[2].strip()
        quantity = int(row[3].strip())

        item_details = get_item_details(item_id)
        item_name = item_details['title']
        price = item_details['price']

        current_order["item_lines"].append({
            "item_id": item_id,
            "item_name": item_name,
            "price": price,
            "quantity": quantity
        })

        current_order["total_price"] += price * quantity
        current_order["unique_items"] += 1

  for order_number, order_data in orders.items():
    json_filename = f"{dump_folder}/order{order_number}.json"
    with open(json_filename, 'w') as json_file:
      json.dump(order_data, json_file, indent=4)
    print(f"JSON file '{json_filename}' created.")


# Run
process_order_details('Order Details.csv')
