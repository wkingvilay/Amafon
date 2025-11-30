from databases import Database

# Connection String
# You need to replace this with whatever your local MYSQL server is
# DATABASE_URL = "mysql+aiomysql://username:password@host:port/databaseName"

DATABASE_URL = "mysql+aiomysql://root:X__xingaling3@localhost:3306/amafon"
database = Database(DATABASE_URL)
