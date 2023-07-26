import os
import sys
import pymysql


# define the flask path
app_directory = os.path.abspath(os.path.join(os.path.dirname(__file__), '../db/'))
sys.path.append(app_directory)

# Get the current directory
current_dir = os.path.dirname(__file__)
print("Current directory:",current_dir)


#testing the connection to the db
def test_mysql_connection(db_config):
    try:
        # Establish a connection to the MySQL database
        connection = pymysql.connect(
            host=db_config['host'],
            user=db_config['username'],
            password= db_config['password'],
            database= db_config['db_name']
        )
        
        # Check if the connection is successful
        assert connection is not None
        # Close the connection
        connection.close()
        
    except pymysql.Error as e:
        pytest.fail(f"Failed to connect to the database: {str(e)}")

#mysql query test
def test_mysql_query_processing(db_config):
    try:
        # Establish a connection to the MySQL database
        connection = pymysql.connect(
            host=db_config['host'],
            user=db_config['username'],
            password= db_config['password'],
            database= db_config['db_name']
        )
        
        # Test the database query processing
        cursor = connection.cursor()
        cursor.execute('SELECT 1')
        result = cursor.fetchone()
        assert result[0] == 1
        
    except pymysql.Error as e:
        pytest.fail(f"Failed to connect to the database: {str(e)}")

    finally:
        # Close the database connection
        connection.close()
