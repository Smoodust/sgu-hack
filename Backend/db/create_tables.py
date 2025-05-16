import psycopg2
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT
from config import user, password, host, port, database

def create_tables():
    try:
        # Connect to PostgreSQL
        connection = psycopg2.connect(
            user=user,
            password=password,
            host=host,
            port=port,
            database=database
        )
        connection.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)
        cursor = connection.cursor()

        # Create logs table
        create_logs_table = """
        CREATE TABLE IF NOT EXISTS logs (
            id SERIAL PRIMARY KEY,
            branch VARCHAR(255) NOT NULL,
            arch VARCHAR(255) NOT NULL,
            name VARCHAR(255) NOT NULL,
            hash VARCHAR(255) NOT NULL,
            version VARCHAR(100) NOT NULL,
            url TEXT NOT NULL,
            updated TIMESTAMP NOT NULL,
            tbfs_since TIMESTAMP NOT NULL
        )
        """
        cursor.execute(create_logs_table)
        print("Table 'logs' created successfully")

    except (Exception, psycopg2.Error) as error:
        print(f"Error while creating table: {error}")

    finally:
        if connection:
            cursor.close()
            connection.close()
            print("PostgreSQL connection closed")

