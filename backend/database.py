from databases import Database

# Connection String
# You need to replace this with whatever your local MYSQL server is
# DATABASE_URL = "mysql+aiomysql://username:password@host:port/databaseName"

DATABASE_URL = "mysql+aiomysql://root:1518@localhost:3306/amafondb"
database = Database(DATABASE_URL)
