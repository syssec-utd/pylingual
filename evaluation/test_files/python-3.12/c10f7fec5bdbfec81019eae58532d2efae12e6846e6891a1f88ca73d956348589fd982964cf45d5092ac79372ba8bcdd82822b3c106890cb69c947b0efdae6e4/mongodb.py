from .connect import Connect

def get_db(db_name='stockdb'):
    client = Connect.get_connection()
    return client[db_name]