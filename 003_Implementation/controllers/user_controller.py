from fastapi import Response, status

from db_operations import DbConnector


def get_users(response: Response):
    '''Retrieve all user records'''
    
    users = []

    # Create instance of DB Connector
    db_connector = DbConnector()

    # Connect to DB
    conn = db_connector.create_connection()
    
    # Verify DB Connection    
    if not db_connector.verify_connection():
        response.status_code = status.HTTP_503_SERVICE_UNAVAILABLE
        response.body = response.render("Database connection error.")
        return response
    
    # Fetch existing users from DB
    with conn.cursor() as cursor:
        query = "SELECT * FROM users order by user_id desc"
        cursor.execute(query)
        users = cursor.fetchall()
    
    # Close DB connection
    db_connector.close_connection()

    # Return the list of users
    return  {"users": users}
