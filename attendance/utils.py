from django.core.exceptions import ObjectDoesNotExist

def check_if_employee_or_company(user, position_lst: list=["company", "employee"]):
    for position in position_lst:
        try:
            user_position = getattr(user, position)
            return user_position
        except ObjectDoesNotExist:
            continue
        return None