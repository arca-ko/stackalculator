import os
import sqlalchemy as sql

# extract DB information from environmental variables
DATABASE = os.environ.get("DATABASE", "")
DB_USER = os.environ.get("DB_USER", "")
DB_PASS = os.environ.get("DB_PASS", "")
MYSQL_IP = os.environ.get("MYSQL_IP", "")

# MySQL database preperations.
engine = sql.create_engine(f"mysql+pymysql://{DB_USER}:{DB_PASS}@{MYSQL_IP}/{DATABASE}", echo=True)
metadata_obj = sql.MetaData()

table_names = ""
i=1
connected = False
while not connected:
    try:
        inspector = sql.inspect(engine)
        table_names = inspector.get_table_names()
        connected = True
    except Exception as e:
        print(f"Tries to connect to the server: {i}")
        i+=1

if table_names:
    """Try to extract table records in case of existence."""
    stack_table = sql.Table("stack", metadata_obj, autoload_with=engine)
    transaction_table = sql.Table("transaction", metadata_obj, autoload_with=engine)
else:
    try:
        """Create tables in case they don't exist."""
        stack_table = sql.Table(
                "stack",
                metadata_obj,
                sql.Column("transaction_id", sql.Integer, primary_key=True, autoincrement=True),
                sql.Column("stack_id", sql.Integer),
                sql.Column("num_value", sql.Integer)
        )

        transaction_table = sql.Table(
                "transaction",
                metadata_obj,
                sql.Column("transaction_id", sql.Integer, primary_key=True, autoincrement=True),
                sql.Column("query", sql.String(100))
        )
        metadata_obj.create_all(engine)

    except Exception as e:
        print(f"\nUnsuccessful table creation. \nError: {e}\n")

# Function definitions
def query_exec(query):
    try:
        with engine.connect() as conn:
            result = conn.execute(query)
            conn.commit()
        return result
    except Exception as e:
        return f"Unsuccessful transaction. Cause of failure: {e}"

def db_insert(id, result):
    stmt = sql.insert(stack_table).values(stack_id = id, num_value = result)
    query_exec(stmt)
    query_exec(sql.insert(transaction_table).values(query = f"{stmt}"))

def fetch_stack_from_db():
    """Fetch the stack from the database and return it as a dictionary."""
    query = sql.select(stack_table)
    result = query_exec(query)

    if isinstance(result, str):
        return {}

    stack_data = {}
    for row in result:
        if row.stack_id not in stack_data:
            stack_data[row.stack_id] = []
        stack_data[row.stack_id].append(row.num_value)

    return stack_data


stack = fetch_stack_from_db() # In-memory stack initialization

def peek(id):
    try:
        return stack[id][-1], 200
    except IndexError:
        return "Stack underflow.", 403
    except KeyError:
        return "Stack not found", 404

def push(id, n):
    if id not in stack.keys():
        stack[id] = []
    stack[id].append(int(n))
    db_insert(id, n)
    return stack[id][-1]

def pop(id, index=-1):
    try:
        result = stack[id].pop(index)
        stmt = sql.text(f"DELETE FROM stack WHERE stack_id = {id} AND num_value = {result} ORDER BY transaction_id DESC LIMIT 1")
        query_exec(stmt)
        query_exec(sql.insert(transaction_table).values(query = f"{stmt}"))
        return result, 200
    except IndexError:
        return "Stack underflow.", 403
    except KeyError:
        return "Stack not found", 404

def add(id):
    if len(stack[id]) < 2:
        return "Stack underflow.", 403
    result = pop(id)[0] + pop(id)[0]
    stack[id].append(result)
    db_insert(id, result)
    return result

def subtract(id):
    if len(stack[id]) < 2:
        return "Stack underflow.", 403
    result = int(pop(id, -2)[0]) - int(pop(id)[0])
    stack[id].append(result)
    db_insert(id, result)
    return result

def multiply(id):
    if len(stack[id]) < 2:
        return "Stack underflow.", 403
    result = int(pop(id)[0]) * int(pop(id)[0])
    stack[id].append(result)
    db_insert(id, result)
    return result

def divide(id):
    if len(stack[id]) < 2:
        return "Stack underflow.", 403
    result = int(pop(id, -2)[0]) / int(pop(id)[0])
    stack[id].append(result)
    db_insert(id, result)
    return result

