import mysql.connector
#write methods to add data base here;

def getAllDatabaseName():
    
    host = 'localhost'
    user = 'root'
    password = 'root@123'

    # Establish a connection to the MySQL server
    connection = mysql.connector.connect(
        host=host,
        user=user,
        password=password
    )

    # Create a cursor object to execute SQL queries
    cursor = connection.cursor()

    # Execute a query to retrieve the list of databases
    cursor.execute("SHOW DATABASES")

    # Fetch all the rows
    databases = cursor.fetchall()
    all_database_names=[]
    # Display the list of databases
    for db in databases:
        all_database_names.append(db[0])
    
    # Close the cursor and connection
    cursor.close()
    connection.close()
    if 'information_schema' in all_database_names:
        all_database_names.remove('information_schema')

    if 'performance_schema' in all_database_names:
        all_database_names.remove('performance_schema')

    if 'mysql' in all_database_names:
        all_database_names.remove('mysql')

    if 'sys' in all_database_names:
        all_database_names.remove('sys')

    if 'temp_db' in all_database_names:
        all_database_names.remove('temp_db')

    return all_database_names