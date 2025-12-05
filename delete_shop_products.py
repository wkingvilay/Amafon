import aiomysql
import asyncio

async def delete_all_products():
    # Database connection details
    connection = await aiomysql.connect(
        host='localhost',
        port=3306,
        user='root',
        password='1518',
        db='amafondb'
    )
    
    try:
        async with connection.cursor() as cursor:
            # First, delete all order items that reference products
            print("Deleting all order items...")
            await cursor.execute("DELETE FROM OrderItems")
            deleted_order_items = cursor.rowcount
            print(f"Deleted {deleted_order_items} order items")
            
            # Then delete all products
            print("\nDeleting all products...")
            await cursor.execute("DELETE FROM Products")
            deleted_products = cursor.rowcount
            print(f"Deleted {deleted_products} products")
            
            # Reset the auto-increment counter
            print("\nResetting product ID counter...")
            await cursor.execute("ALTER TABLE Products AUTO_INCREMENT = 1")
            
            # Commit the changes
            await connection.commit()
            
            print("\n✅ All products and related order items deleted successfully!")
            print("The database is now clean.")
            
    except Exception as e:
        print(f"\n❌ Error: {e}")
        await connection.rollback()
    finally:
        connection.close()

if __name__ == "__main__":
    asyncio.run(delete_all_products())
