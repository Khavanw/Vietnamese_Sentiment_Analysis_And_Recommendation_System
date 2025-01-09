import pyodbc

class BrandDao:
    def get_list_brand(self):
        conn = pyodbc.connect('DRIVER={ODBC Driver 17 for SQL Server};SERVER=ADMIN-PC;DATABASE=SalesPhone;Trusted_Connection=yes;Encrypt=no')
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM brand")
        return cursor.fetchall()
