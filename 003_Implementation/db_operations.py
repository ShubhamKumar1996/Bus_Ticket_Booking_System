from mysql.connector import connection
import configparser

class DbConnector:
    def __init__(self):
        self.db_config_file = 'db_config.ini'
        self.conn = None

    def create_connection(self):
        """ Connects to the MySQL server """

        # Read the configuration file to get database information
        config = configparser.ConfigParser()
        try:
            # Get the configuration parameters
            if not config.read(self.db_config_file):
                raise FileNotFoundError("DB config file is either unavailable or empty")
            else:
                self.db_config = dict(config.items(config.sections()[0]))
            
            #  Create a new connection using the provided details
            self.conn = connection.MySQLConnection(**self.db_config)
        except  Exception as e:
            print(f"db_operations:create_connection: {str(e)}")
        finally:
            return self.conn
        

    def verify_connection(self):
        if self.conn and self.conn.is_connected():
            return True
        return False

    def close_connection(self):
        self.conn.close()
