import threading
from django.db import connection

thread = threading.local()

db_routes_for_company = {
    "SSL E commerce": "ssl_e_commerce",
    "AamarPay": "aamarpay",
    "127.0.0.1:8000": "default",
    "localhost:8000": "default",
}


class MultiDbMiddleware:
    
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        hostname = request.META["HTTP_HOST"]
        db = db_routes_for_company[hostname]
        setattr(thread, "Db", db)
        print("Set the db to ",getattr(thread, "Db"))
        response = self.get_response(request)
        return response


def get_db_name_from_router():
    return getattr(thread, "Db")


def set_db_for_router(db):
    setattr(thread, "Db", db)
    return True
