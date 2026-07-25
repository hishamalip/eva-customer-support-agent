from langchain_core.tools import tool
from typing import List, Dict
from vector_store import FlowerShopVectorStore
import json


# Setup customer database(dummy data for the example)
CUSTOMER_DATABASE = [
    {"name": "John Doe", "dob": "1990-01-01", "customer_id": "CUST001", "first_line_address": "123 Main St", "phone_number": "7712345678", "email": "john.doe@example.com"},
    {"name": "Jane Smith", "dob": "1985-05-15", "customer_id": "CUST002", "first_line_address": "456 High St", "phone_number": "7723456789", "email": "jane.smith@example.com"},
]

ORDERS_DATABASE = [
    {"order_id": "ORD1", "customer_id": "CUST001", "status": "Processing", "items": ["Red Roses Bouquet"], "quantity": [1]},
    {"order_id": "ORD2", "customer_id": "CUST002", "status": "Shipped", "items": ["Mixed Tulips", "Vase"], "quantity": [3, 1]},
]

with open('inventory.json', 'r') as f:
    INVENTORY_DATABASE = json.load(f)


# Initialize the vector store instance for querying FAQ and inventory data
vector_store = FlowerShopVectorStore()

@tool
def query_knowledge_base(query: str) -> List[Dict[str, str]]:
    """
    Looks up information in a knowledge base to help with answering customer questions and getting information on business processes.

    Args:
        query (str): The question or query to look up in the knowledge base.

    Return:
        List[Dict[str, str]]: Potentially relevant question and answer pairs from the knowledge base.
    """
    return vector_store.query_faqs(query)


@tool
def search_for_product_recommendations(description: str) -> List[Dict[str, str]]:
    """
    Looks up information in a knowledge base to help with product recommendation for customers. For example: 
    
    "Boquets suiable for birthdays, may be with red flowers"
    "A large boquet for a wedding"
    "A cheap boquet with wildflowers"

    Args:
        description (str): Description of product features

    Return:
        List[Dict[str, str]]: Potentially relevant products.
    """
    return vector_store.query_inventory(description)


@tool
def data_protection_check(name: str, email: str, year_of_birth: int, month_of_birth: int, day_of_birth: int) -> str:
    """
    Perform a data protection check against a customer to retrieve customer details.

    Args:
        name (str): Customer first and last name
        email (str): Customer email address
        year_of_birth (int): The year the customer was born
        month_of_birth (int): The month the customer was born
        day_of_birth (int): The day the customer was born

    Returns:
        str: Customer details (name, postcode, dob, customer_id, first_line_address, email)
    """
    for customer in CUSTOMER_DATABASE:
        if (customer['name'].lower() == name.lower() and
            customer['email'].lower() == email.lower() and
            int(customer['dob'][0:4]) == year_of_birth and
            int(customer["dob"][5:7]) == month_of_birth and
            int(customer["dob"][8:10]) == day_of_birth):
            return f"DPA check passed - Retrieved customer details:\n{customer}"

    return "DPA check failed, no customer with these details found"


@tool
def create_new_customer(first_name: str, surname: str, year_of_birth: int, month_of_birth: int, day_of_birth: int, first_line_of_address: str, phone_number: str, email: str) -> str:
    """
    Creates a customer profile, so that they can place orders.

    Args:
        first_name (str): Customers first name
        surname (str): Customers surname
        year_of_birth (int): Year customer was born
        month_of_birth (int): Month customer was born
        day_of_birth (int): Day customer was born
        first_line_address (str): Customer's first line of address
        phone_number (str): Customer's phone number
        email (str): Customer's email address

    Returns:
        str: Confirmation that the profile has been created or any issues with the inputs
    """
    if len(phone_number) != 10:
        return "Phone number must be 10 digits"

    customer_id = len(CUSTOMER_DATABASE) + 1
    CUSTOMER_DATABASE.append({
        'name': first_name + ' ' + surname,
        'dob': f'{year_of_birth}-{month_of_birth:02}-{day_of_birth:02}',
        'first_line_address': first_line_of_address,
        'phone_number': phone_number,
        'email': email,
        'customer_id': f'CUST{customer_id}'
    })
    return f"Customer registered, with customer_id {f'CUST{customer_id}'}"


@tool
def retrieve_existing_customer_orders(customer_id: str) -> List[Dict]:
    """
    Retrieves the orders associated with the customer, including their status, items and ids

    Args:
        customer_id (str): Customer unique id associated with the order

    Returns:
        List[Dict]: All the orders associated with the customer_id passed in
    """
    customer_orders = [order for order in ORDERS_DATABASE if order['customer_id'] == customer_id]
    if not customer_orders:
        return f"No orders associated with this customer id: {customer_id}"

    return customer_orders


@tool
def place_order(items: Dict[str, int], customer_id: str) -> str:
    """
    Places an order for the requested items, and for the required quantities.

    Args:
        items (Dict[str, int]): Dictionary of items to order, with item id as the key and the quantity of that item as the value.
        customer_id (str): The customer to place the order for

    Returns:
        str: Message indicating that the order has been placed, or, it hasnt been placed due to an issue 
    
    Example arguments:
        items = {"P005": 3, "P012": 5}
        customer_id = "CUST001"
    """
    # Check that the item ids are valid and the quantities of items are valid
    availability_messages = []
    valid_item_ids = {item['id'] for item in INVENTORY_DATABASE}

    for item_id, quantity in items.items():
        if item_id not in valid_item_ids:
            availability_messages.append(f'Item with id {item_id} is not found in the inventory')
        else:
            inventory_item = next(item for item in INVENTORY_DATABASE if item['id'] == item_id) # Get the inventory item details
            if quantity > inventory_item['quantity']:
                availability_messages.append(f'There is insufficient quantity in the inventory for this item {inventory_item["name"]}\nAvailable: {inventory_item["quantity"]}\nRequested: {quantity}')
    if availability_messages:
        return "Order cannot be placed due to the following issues: \n" + '\n'.join(availability_messages)

    # Place the order (in pretend database)
    order_id = f"ORD{len(ORDERS_DATABASE) + 1}"
    ORDERS_DATABASE.append(
        {
            'order_id': order_id,
            'customer_id': customer_id,
            'status': 'Waiting for payment',
            'items': list(items.keys()),
            'quantity': list(items.values())
        }
    )

    # Update the inventory
    for item_id, quantity in items.items():
        inventory_item = next(item for item in INVENTORY_DATABASE if item['id'] == item_id) # Get the inventory item details
        inventory_item['quantity'] -= quantity

    return f"Order with id {order_id} has been placed successfully"
