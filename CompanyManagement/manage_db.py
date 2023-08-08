from django.contrib.auth import get_user_model
from accounts.models import Employee, Company, EmployeeShift, CompanyPosition
from attendance.models import Attendance, LeaveModel
from django.core.exceptions import ObjectDoesNotExist
from .middleware import get_db_name_from_router


User = get_user_model()

db_routes_for_company = {
    "SSL E commerce": "ssl_e_commerce",
    "AamarPay": "aamarpay",
    "127.0.0.1": "default",
    "localhost": "default",
}


class_grouped_lst = [
    [User, "company", "name"], 
    [User, "employee", "company", ],
    [Company, ],
    [Employee, "company", ],
    [EmployeeShift, "company", ],
    [CompanyPosition, "company", ],
    [Attendance, "employee", "company", ],
    [LeaveModel, "employee", "company", ],
]


def get_company_from_object(obj):
    if type(obj) == Company:
        return obj.name
    
    for lst in class_grouped_lst:

        if type(obj) == lst[0]:
            company_name = algo_get_company_name_via_recurring(obj, lst)
            if company_name is None:
                continue
            return company_name
        continue


def algo_get_company_name_via_recurring(obj, lst, a=1):
    obj_attribute = lst[a]
    try:

        new_obj = getattr(obj, obj_attribute)
    except ObjectDoesNotExist:
        return None
    if type(new_obj) != Company:
        return algo_get_company_name_via_recurring(new_obj, lst, a+1)
    return new_obj.name


class DbRouter:

    def db_for_read(self, model, **hints):
        db_name = get_db_name_from_router()
        return db_name

    def db_for_write(self, model, **hints):
        db_name = get_db_name_from_router()
        return db_name

    def allow_relations(self, model, **hints):
        db_name = get_db_name_from_router()
        return db_name

    def allow_migrate(self, model, **hints):
        db_name = get_db_name_from_router()
        return db_name


