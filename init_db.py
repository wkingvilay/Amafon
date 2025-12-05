import asyncio
import aiomysql
import re

async def init_db():
    try:
        with open('backend/amafon.sql', 'r') as f:
            content = f.read()
        
        # Remove SQL comments
        content = re.sub(r'--.*?$', '', content, flags=re.MULTILINE)
        content = re.sub(r'/\*.*?\*/', '', content, flags=re.DOTALL)
        
        conn = await aiomysql.connect(
            host='localhost',
            user='root',
            password='Qd521125.',
            port=3306
        )
        
        async with conn.cursor() as cursor:
            statements = [s.strip() for s in content.split(';') if s.strip()]
            for statement in statements:
                try:
                    await cursor.execute(statement)
                except Exception as e:
                    print(f'Warning: {e}')
            await conn.commit()
        
        print('✓ Database initialized successfully!')
        conn.close()
    except Exception as e:
        print(f'Error: {e}')

if __name__ == '__main__':
    asyncio.run(init_db())
