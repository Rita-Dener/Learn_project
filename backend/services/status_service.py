def get_status():
    return {
        "status": "ok",
        "message": "Backend работает",
        "service": "backend-service",
        "items_counts": 3
    }

def get_items_data():
    return [
        {"id": 1, "name": "Товар 1"},
        {"id": 2, "name": "Товар 2"},
        {"id": 3, "name": "Товар 3"}
    ]