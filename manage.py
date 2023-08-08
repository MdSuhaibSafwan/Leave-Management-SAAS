#!/usr/bin/env python
"""Django's command-line utility for administrative tasks."""
import os
import sys
from django.db import connection
from CompanyManagement.middleware import set_db_for_router


def main():
    """Run administrative tasks."""
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'CompanyManagement.settings')
    try:
        from django.core.management import execute_from_command_line
    except ImportError as exc:
        raise ImportError(
            "Couldn't import Django. Are you sure it's installed and "
            "available on your PYTHONPATH environment variable? Did you "
            "forget to activate a virtual environment?"
        ) from exc
    
    args = sys.argv
    print(args)
    db_name = args[-1]
    db_name = db_name.split("=")[1] # this is for now later implement regular expressions
    del args[-1]    
    set_db_for_router(db=db_name)
    execute_from_command_line(args)


if __name__ == '__main__':
    main()
