from .database import get_db

# This file is for shared dependencies across modules.
# For example, a dependency to get the current user with specific permissions.

# from fastapi import Depends, HTTPException
# from app.core.security import get_current_user
# from app.models.db import User
# async def get_current_active_admin_user(current_user: User = Depends(get_current_user)):
#     ...