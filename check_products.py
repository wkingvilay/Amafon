import asyncio
import sys
sys.path.insert(0, r'c:\Users\juddl\Downloads\Amafon-main\Amafon-main')

from backend.database import database

async def check_products():
    await database.connect()
    
    print("=" * 60)
    print("ALL PRODUCTS IN DATABASE:")
    print("=" * 60)
    
    all_products = await database.fetch_all(
        "SELECT product_id, seller_id, name, is_active, created_at FROM Products ORDER BY created_at DESC"
    )
    
    if all_products:
        for p in all_products:
            status = "✅ ACTIVE" if p['is_active'] else "❌ INACTIVE"
            print(f"{status} | ID: {p['product_id']} | Seller: {p['seller_id']} | Name: {p['name']} | Created: {p['created_at']}")
    else:
        print("No products found in database!")
    
    print("\n" + "=" * 60)
    print("ACTIVE PRODUCTS ONLY (what API returns):")
    print("=" * 60)
    
    active_products = await database.fetch_all(
        "SELECT product_id, seller_id, name, created_at FROM Products WHERE is_active = TRUE ORDER BY created_at DESC"
    )
    
    if active_products:
        for p in active_products:
            print(f"ID: {p['product_id']} | Seller: {p['seller_id']} | Name: {p['name']} | Created: {p['created_at']}")
    else:
        print("No active products found!")
    
    print("\n" + "=" * 60)
    print("LOOKING FOR 'PENCIL':")
    print("=" * 60)
    
    pencil_products = await database.fetch_all(
        "SELECT product_id, seller_id, name, is_active FROM Products WHERE LOWER(name) LIKE '%pencil%'"
    )
    
    if pencil_products:
        for p in pencil_products:
            status = "✅ ACTIVE" if p['is_active'] else "❌ INACTIVE (hidden from view)"
            print(f"{status} | ID: {p['product_id']} | Seller: {p['seller_id']} | Name: {p['name']}")
    else:
        print("❌ No products with 'pencil' in the name found!")
        print("\nDid you create the pencil product? If not, create it via the 'Create Listing' page.")
    
    await database.disconnect()

if __name__ == "__main__":
    asyncio.run(check_products())
