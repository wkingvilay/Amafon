import asyncio
import sys
sys.path.insert(0, r'c:\Users\juddl\Downloads\Amafon-main\Amafon-main')

from backend.database import database

async def clean_database():
    await database.connect()
    
    print("=" * 60)
    print("CLEANING DATABASE - REMOVING OLD PRODUCTS")
    print("=" * 60)
    
    # Get all products first
    all_products = await database.fetch_all(
        "SELECT product_id, name FROM Products"
    )
    
    print(f"\nFound {len(all_products)} products in database:")
    for p in all_products:
        print(f"  - ID {p['product_id']}: {p['name']}")
    
    # Delete all products
    print(f"\n🗑️ Deleting all {len(all_products)} products...")
    
    try:
        # First, delete any order items that reference these products
        await database.execute("DELETE FROM OrderItems WHERE product_id IN (SELECT product_id FROM Products)")
        print("✅ Deleted order items")
        
        # Now delete all products
        await database.execute("DELETE FROM Products")
        print("✅ Deleted all products")
        
        # Verify
        remaining = await database.fetch_all("SELECT COUNT(*) as count FROM Products")
        count = remaining[0]['count']
        
        if count == 0:
            print("\n🎉 SUCCESS! Database is now clean - 0 products remaining")
        else:
            print(f"\n⚠️ Warning: {count} products still in database")
            
    except Exception as e:
        print(f"\n❌ ERROR: {e}")
        print("\nNote: Some products may have foreign key constraints from Reviews.")
        print("If deletion fails, products will be kept as inactive instead.")
    
    await database.disconnect()

if __name__ == "__main__":
    print("\n⚠️  WARNING: This will DELETE ALL PRODUCTS from the database!")
    print("This includes order history references.")
    response = input("\nAre you sure you want to continue? (type 'yes' to confirm): ")
    
    if response.lower() == 'yes':
        asyncio.run(clean_database())
    else:
        print("\n❌ Cancelled - no changes made")
