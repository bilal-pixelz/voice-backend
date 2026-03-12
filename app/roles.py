from enum import Enum

class Role(str, Enum):
    admin = "admin"
    user = "user"

def get_role_permissions(role: Role):
    if role == Role.admin:
        return ["manage_company", "manage_users", "view_invoices", "create_invoice"]
    elif role == Role.user:
        return ["view_invoices", "create_invoice"]
    return []
