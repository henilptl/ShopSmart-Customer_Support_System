"""Synthetic knowledge sources for the specialist handlers.

In production these would be swapped for real systems: ORDERS_DB for an
order-management API, PRODUCTS_DB for a catalog service, and the policy
strings for a RAG retriever over the help centre.
"""

ORDERS_DB = {
    "ORD-1001": {
        "customer": "Priya Sharma",
        "item": "Samsung Galaxy S24",
        "amount": "₹74,999",
        "status": "In Transit",
        "city": "Mumbai",
        "expected_delivery": "2 days",
    },
    "ORD-1002": {
        "customer": "Rahul Verma",
        "item": "Sony WH-1000XM5 Headphones",
        "amount": "₹24,990",
        "status": "Delivered",
        "city": "Delhi",
        "expected_delivery": "Delivered on 8 Apr",
    },
    "ORD-1003": {
        "customer": "Anita Desai",
        "item": "Apple MacBook Air M3",
        "amount": "₹1,14,900",
        "status": "Processing",
        "city": "Bangalore",
        "expected_delivery": "5 days",
    },
    "ORD-1004": {
        "customer": "Vikram Patel",
        "item": "Boat Airdopes 141",
        "amount": "₹1,299",
        "status": "Shipped",
        "city": "Ahmedabad",
        "expected_delivery": "3 days",
    },
    "ORD-1005": {
        "customer": "Meera Krishnan",
        "item": "LG 55-inch OLED TV",
        "amount": "₹1,39,990",
        "status": "Delayed",
        "city": "Chennai",
        "expected_delivery": "Under review",
    },
}

PRODUCTS_DB = {
    "Samsung Galaxy S24": {
        "price": "₹74,999",
        "rating": "4.5/5",
        "category": "Smartphones",
        "stock": "In Stock",
        "highlights": "6.2-inch AMOLED, Snapdragon 8 Gen 3, 50MP Camera",
    },
    "Sony WH-1000XM5": {
        "price": "₹24,990",
        "rating": "4.7/5",
        "category": "Headphones",
        "stock": "In Stock",
        "highlights": "Industry-leading ANC, 30hr battery, Multipoint",
    },
    "Apple MacBook Air M3": {
        "price": "₹1,14,900",
        "rating": "4.8/5",
        "category": "Laptops",
        "stock": "Limited Stock",
        "highlights": "M3 chip, 18hr battery, 13.6-inch Liquid Retina",
    },
    "Boat Airdopes 141": {
        "price": "₹1,299",
        "rating": "4.1/5",
        "category": "Earbuds",
        "stock": "In Stock",
        "highlights": "42hr playback, IPX4, Low Latency Mode",
    },
    "LG 55-inch OLED TV": {
        "price": "₹1,39,990",
        "rating": "4.6/5",
        "category": "TVs",
        "stock": "In Stock",
        "highlights": "4K OLED, Dolby Vision, webOS, 120Hz",
    },
}

RETURN_POLICY = """ShopSmart Return Policy:
- 7-day no-questions-asked return for electronics
- 15-day return window for clothing and accessories
- Refund processed within 5-7 business days to original payment method
- Damaged products: Instant replacement or full refund
- Return pickup scheduled within 24 hours of request
- Non-returnable: Innerwear, customized items, perishables"""

BILLING_POLICY = """ShopSmart Billing Policy:
- Payment methods: UPI, Credit/Debit Cards, Net Banking, ShopSmart Wallet, EMI options
- Failed payment: Amount auto-refunded within 3-5 business days
- Double charge: Report within 48 hours for immediate reversal
- EMI available on orders above ₹3,000 via partner banks
- GST invoice available for all orders in the Order Details section
- ShopSmart Wallet refunds are instant"""


def format_order_context() -> str:
    """Flatten ORDERS_DB into a compact block for prompt injection."""
    return "\n".join(
        f"- {oid}: {info['item']} | {info['amount']} | Status: {info['status']} "
        f"| City: {info['city']} | ETA: {info['expected_delivery']}"
        for oid, info in ORDERS_DB.items()
    )


def format_product_context() -> str:
    """Flatten PRODUCTS_DB into a compact block for prompt injection."""
    return "\n".join(
        f"- {name}: {info['price']} | {info['rating']} | {info['stock']} | {info['highlights']}"
        for name, info in PRODUCTS_DB.items()
    )
