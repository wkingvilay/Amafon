import asyncio
import sys
sys.path.insert(0, r'c:\Users\juddl\Downloads\Amafon-main\Amafon-main')

from backend.database import database

async def check_seller():
    await database.connect()
    
    # Check if seller exists
    seller = await database.fetch_one('SELECT * FROM Sellers WHERE seller_id = 1')
    
    if seller:
        print("✅ Seller ID 1 EXISTS:")
        print(dict(seller))
    else:
        print("❌ Seller ID 1 DOES NOT EXIST")
        print("\nChecking all sellers:")
        sellers = await database.fetch_all('SELECT * FROM Sellers')
        if sellers:
            for s in sellers:
                print(f"  - Seller ID {s['seller_id']}: {s['store_name']}")
        else:
            print("  No sellers in database!")
    
    await database.disconnect()

if __name__ == "__main__":
    asyncio.run(check_seller())
