from django.contrib.auth import get_user_model
from accounts.models import Employee, Company, EmployeeShift, CompanyPosition
from attendance.models import Attendance, LeaveModel
from django.core.exceptions import ObjectDoesNotExist


User = get_user_model()

db_routes_for_company = {
    "SSL E commerce": "ssl_e_commerce",
    "AamarPay": "aamarpay"
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
            # print(lst)
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


class DbRouters:

    def db_for_read(self, model, **hints):
        print("DB FOR READ")
        print("Model ", model)

        
        return 'default'

    def db_for_write(self, model, **hints):
        print("DB FOR WRITE")
        print("Hints", hints)
        print("Model ", model)
        
        return 'default'

    def allow_relations(self, model, **hints):
        print("DB FOR RELATIONS")
        print("Hints", hints)
        print("Model ", model)
        
        return 'default'

    def allow_migrate(self, model, **hints):
        print("DB FOR MIGRATE")
        print("Hints", hints)
        print("Model ", model)
        
        return 'default'


