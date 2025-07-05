from inventory import get_all_products, get_low_stock

def generate_summary():
    products = get_all_products()
    total_value = sum(p[2] * p[3] for p in products)
    return {
        "total_products": len(products),
        "inventory_value": total_value,
        "low_stock": get_low_stock()
    }
