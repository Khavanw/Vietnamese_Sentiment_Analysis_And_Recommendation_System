import pyodbc
from function.User_file import User

class UserDao:
    # Thực hiện một thủ tục lưu trữ (stored procedure) CheckLogin để kiểm tra thông tin đăng nhập của người dùng
    def check_login(self,user:User):
        conn = pyodbc.connect('DRIVER={ODBC Driver 17 for SQL Server};SERVER=ADMIN-PC;DATABASE=SalesPhone;Trusted_Connection=yes;Encrypt=no')
        cursor = conn.cursor()
        cursor.execute("EXEC CheckLogin @Username=?, @Password=?", (user.getUserName,user.getPassWord))
        login_success = cursor.fetchone()[0]  
        conn.close()
        return login_success
    
    # Thực hiện truy vấn SQL để lấy tên đầy đủ của người dùng từ bảng 'users', dựa trên nội dung bình luận (user.getComment).
    def get_full_name(self,user:User):
        conn = pyodbc.connect('DRIVER={ODBC Driver 17 for SQL Server};SERVER=ADMIN-PC;DATABASE=SalesPhone;Trusted_Connection=yes;Encrypt=no')
        cursor = conn.cursor()
        cursor.execute(f"select full_name From users join comments on comments.user_id=users.id where comment = N'{user.getComment}'")
        user_row = cursor.fetchone()
        conn.close()
        return user_row[0] if user_row else None
    
    # Thực hiện truy vấn SQL để lấy 'id' của người dùng dựa trên tên người dùng (user.getUserName).
    def get_user_id(self,user:User):
        conn = pyodbc.connect('DRIVER={ODBC Driver 17 for SQL Server};SERVER=ADMIN-PC;DATABASE=SalesPhone;Trusted_Connection=yes;Encrypt=no')
        cursor = conn.cursor()
        cursor.execute(f"SELECT DISTINCT(id) FROM users WHERE username = '{user.getUserName}'")
        user_row = cursor.fetchone()
        conn.close()
        return user_row[0] if user_row else None