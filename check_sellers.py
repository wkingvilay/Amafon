import aiomysql
import asyncio

async def check_sellers():
    connection = await aiomysql.connect(
        host='localhost',
        port=3306,
        user='root',
        password='1518',
        db='amafondb'
    )
    
    try:
        async with connection.cursor() as cursor:
            await cursor.execute("SELECT * FROM Sellers")
            rows = await cursor.fetchall()
            
            if rows:
                print(f"Found {len(rows)} seller(s):")
                for row in rows:
                    print(f"  {row}")
            else:
                print("No sellers found in database!")
                
            # Check users too
            print("\nChecking Users table:")
            await cursor.execute("SELECT user_id, username, email FROM Users")
            users = await cursor.fetchall()
            if users:
                print(f"Found {len(users)} user(s):")
                for user in users:
                    print(f"  {user}")
            
    finally:
        connection.close()

asyncio.run(check_sellers())
