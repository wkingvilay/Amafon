from database import database
from schemas.users import Role

# Returns all the information for a select number of users
async def get_users(skip: int = 0, limit: int = 10):
    query="""
        SELECT * FROM Users 
        LIMIT :limit OFFSET :skip;
    """
    return await database.fetch_all(query=query, values={'limit':limit, 'skip':skip})

# Returns all the information for a specific user based on user_id
async def get_user(user_id: int):
    query = """
    SELECT * FROM Users
    WHERE user_id = :user_id
    """
    row = await database.fetch_one(query=query, values={"user_id": user_id})
    return dict(row) if row else None

# Creates a new user
async def create_user(name: str, email: str, password: str, role: Role):
    query = """
    INSERT INTO Users (name, email, password, role)
    VALUES (:name, :email, :password, :role)
    """
    try:
        user_id = await database.execute(query=query, values={
            "name": name,
            "email": email,
            "password": password,
            "role": role
        })
        return user_id
    except Exception:
        # Raise clear error if code already exists (email already in use)
        raise ValueError(f"Account with email already exists.")

# Updates an existing user based on user_id
async def update_user(name: str, email: str, password: str, role: Role, user_id: int):
    query = """
    UPDATE Users SET
    name = :name, email = :email, password= :password, role = :role
    WHERE user_id = :user_id
    """
    try:
        await database.execute(query=query, values={
            "name": name,
            "email": email,
            "password": password,
            "role": role,
            "user_id": user_id
        })
        return True
    except Exception:
        # Raise clear error if code already exists (email already in use)
        raise ValueError(f"Error updating user")

# Deletes a user based on user_id
async def delete_user(user_id: int):
    query = "DELETE FROM Users WHERE user_id = :user_id"
    return await database.execute(query=query, values={"user_id": user_id})

# Attempts to log in based on credentials
async def login_user(email: str, password: str):
    query = """
    SELECT * FROM Users WHERE email = :email AND password = :password
    """
    row = await database.fetch_one(query=query, values={"email": email, "password": password})
    return dict(row) if row else None