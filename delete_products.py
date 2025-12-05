import asyncio
import sys
sys.path.insert(0, r'c:\Users\juddl\Downloads\Amafon-main\Amafon-main')

from backend.database import database

async def delete_all():
    await database.connect()
    
    # Delete order items first (foreign key constraint)
    await database.execute("DELETE FROM OrderItems")
    print("✅ Deleted OrderItems")
    
    # Delete all products
    await database.execute("DELETE FROM Products")
    print("✅ Deleted Products")
    
    # Verify
    count = await database.fetch_val("SELECT COUNT(*) FROM Products")
    print(f"\n✅ Done! Products remaining: {count}")
    
    await database.disconnect()

asyncio.run(delete_all())
