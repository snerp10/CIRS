from datetime import datetime
import mysql.connector
from mysql.connector import Error

class CrimeIncident:
    
    # constructor
    
    def __init__(self, incident_id, description, location, date, reporter):   
        self.incident_id = incident_id
        self.description = description
        self.location = location
        self.date = date
        self.reporter = reporter
        
    # return all data
    
    def __str__(self):
        return f"ID: {self.incident_id}, Desc: {self.description}, Loc: {self.location}, Date: {self.date}, Reporter: {self.reporter}"


class CrimeIncidentManager:
    
    # initialize db
    
    def __init__(self, db_config=None):
        self.db_connection = None
        self.current_user = None
        if db_config:
            self.connect_to_database(db_config)
            
    # connect to MySQL database
    def login(self, username, password):

        if self.verify_user(username, password): 
            self.current_user = username  
            print(f"User {self.current_user} logged in successfully.")
        else:
            print("Login failed.")
            
    def connect_to_database(self, config):
        try:
            self.db_connection = mysql.connector.connect(**config)
            if self.db_connection.is_connected():
                print("Connected to MySQL database for crime incidents")
        except Error as e:
            print(f"Error: {e}")
            
    # close MySQL database
    
    def close_database_connection(self):
        
        if self.db_connection and self.db_connection.is_connected():
            self.db_connection.close()
            print("MySQL connection closed")
    
    def get_next_incident_id(self):
    
        cursor = self.db_connection.cursor()
        query = "SELECT MAX(CAST(incident_id AS UNSIGNED)) FROM crime_incidents"
        cursor.execute(query)
        result = cursor.fetchone()
        cursor.close()

        if result[0] is None:
            return "1"  

        next_id = int(result[0]) + 1
        return f"{next_id}"
    
    def add_incident(self, description, location, date, reporter):
        
        if not self.db_connection or not self.db_connection.is_connected():
            print("Database connection is not available.")
            return
        try:
            cursor = self.db_connection.cursor()
            incident_id = self.get_next_incident_id()
            query = "INSERT INTO crime_incidents (incident_id, description, location, date, reporter) VALUES (%s, %s, %s, %s, %s)"
            cursor.execute(query, (incident_id, description, location, date, reporter))
            self.db_connection.commit()
            print("Incident added successfully.")
        except mysql.connector.Error as err:
            print(f"Error: {err}")  # Log the error
        finally:
        # Only close cursor if it was opened successfully
            if 'cursor' in locals():
                cursor.close()
        
    def add_incident_to_db(self, incident):

        query = "INSERT INTO crime_incidents (incident_id, description, location, date, reporter) VALUES (%s, %s, %s, %s, %s)"
        values = (incident.incident_id, incident.description, incident.location, incident.date, incident.reporter)
        cursor = self.db_connection.cursor()
        cursor.execute(query, values)
        self.db_connection.commit()
        cursor.close()

    def update_incident(self, incident_id, updated_incident):
        
        existing_incident = self.get_incident_by_id(incident_id)
        if existing_incident is None:
            print(f"Incident with ID {incident_id} does not exist.")  
            return False 
        query = "UPDATE crime_incidents SET description = %s, location = %s, date = %s, reporter = %s WHERE incident_id = %s"
        values = (updated_incident.description, updated_incident.location, updated_incident.date, updated_incident.reporter, incident_id)
        cursor = self.db_connection.cursor()
        cursor.execute(query, values)
        self.db_connection.commit()
        cursor.close()
        return True

    def delete_incident_from_db(self, incident_id):
        """Delete the incident from the database."""
        try:
            query = "DELETE FROM crime_incidents WHERE incident_id = %s"
            cursor = self.db_connection.cursor()
            cursor.execute(query, (incident_id,))
            self.db_connection.commit()  # Commit changes
            cursor.close()
            print(f"Incident with ID {incident_id} deleted from database successfully")  # Debug info
            
        except Error as e:
            print(f"Error deleting incident from database: {e}")

    def delete_all_incidents_from_db(self):
        """Delete all crime_incidents from the database."""
        query = "DELETE FROM crime_incidents"
        cursor = self.db_connection.cursor()
        cursor.execute(query)
        self.db_connection.commit()
        cursor.close()

    def get_all_incidents(self):
        
        if self.db_connection:
            cursor = self.db_connection.cursor()
            cursor.execute("SELECT incident_id, description, location, date, reporter FROM crime_incidents")
            rows = cursor.fetchall()
            incidents = [CrimeIncident(*row) for row in rows]
            cursor.close()
            return incidents
        return []
    
    def get_incident_by_id(self, incident_id):

        cursor = self.db_connection.cursor()
        query = "SELECT incident_id, description, location, date, reporter FROM crime_incidents WHERE incident_id = %s"
        cursor.execute(query, (incident_id,))
        row = cursor.fetchone()
        cursor.close()

        if row:
            return CrimeIncident(*row)
        return None
        
        
    def __del__(self):
        self.close_database_connection()
    
if __name__ == "__main__":
    try:
        connection_to_db = {
            'host': 'localhost',
            'user': 'root',     
            'password': '',   
            'database': "crime_incidents_db"    
        }
        
        manager = CrimeIncidentManager(db_config = connection_to_db)
        
        for incident in manager.get_all_incidents():
            print(incident)

    except Exception as e:
        print(f"An error occurred: {e}")