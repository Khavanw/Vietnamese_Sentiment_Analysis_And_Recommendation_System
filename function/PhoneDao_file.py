import pyodbc
from function.Phone_file import Phone
from function.Comment_file import Comment
import traceback

class PhoneDao:
    # Thực hiện truy vấn SQL để lấy tất cả các hàng từ bảng 'phone'
    def get_list_phone(self):
        """Lấy danh sách điện thoại với product_id"""
        try:
            conn = pyodbc.connect('DRIVER={ODBC Driver 17 for SQL Server};SERVER=ADMIN-PC;DATABASE=SalesPhone;Trusted_Connection=yes;Encrypt=no')
            cursor = conn.cursor()
            cursor.execute("""
                SELECT p.product_id, p.phone_name, b.brand_name, p.price, p.rating, p.review_count,
                       p.ram, p.storage, p.rear_camera, p.front_camera, p.photo_url
                FROM phones p
                JOIN brands b ON p.brand_id = b.id
            """)
            phone_row = cursor.fetchall()
            cursor.close()
            conn.close()
            return phone_row
        except Exception as e:
            print(f"Lỗi khi lấy danh sách điện thoại: {e}")
            traceback.print_exc()
            return []
    
    # Thực hiện truy vấn SQL để lấy thông tin của một điện thoại cụ thể dựa trên 'phone_id'
    def get_phone(self, phone_id):
        """Lấy thông tin chi tiết của một điện thoại dựa trên product_id"""
        try:
            conn = pyodbc.connect('DRIVER={ODBC Driver 17 for SQL Server};SERVER=ADMIN-PC;DATABASE=SalesPhone;Trusted_Connection=yes;Encrypt=no')
            cursor = conn.cursor()
            cursor.execute("""
                SELECT 
                    p.id,
                    p.phone_name,
                    b.brand_name,
                    p.product_id,
                    ISNULL(p.price, 0) as price,
                    ISNULL(p.ram, 0) as ram,
                    ISNULL(p.storage, 0) as storage,
                    ISNULL(p.front_camera, 0) as front_camera,
                    ISNULL(p.rear_camera, 0) as rear_camera,
                    ISNULL(p.battery, 0) as battery,
                    ISNULL(p.rating, 0) as rating,
                    ISNULL(p.review_count, 0) as review_count,
                    ISNULL(p.photo_url, '') as photo_url
                FROM phones p
                JOIN brands b ON p.brand_id = b.id
                WHERE p.product_id = ?
            """, (phone_id,))
            phone_row = cursor.fetchone()
            
            print(f"SQL Query result for product_id {phone_id}: {phone_row}")  # Debug log
            
            cursor.close()
            conn.close()
            return phone_row
        except Exception as e:
            print(f"Lỗi khi lấy thông tin điện thoại với product_id {phone_id}: {e}")
            traceback.print_exc()
            return None
    
    # Thực hiện truy vấn SQL để lấy id của điện thoại dựa trên 'phone_name'
    def get_id_by_phone(self,phone:Phone):
        conn=pyodbc.connect("DRIVER={ODBC Driver 17 for SQL Server};SERVER=ADMIN-PC;DATABASE=SalesPhone;Trusted_Connection=yes;Encrypt=no")
        cursor=conn.cursor()
        cursor.execute("SELECT id FROM phones WHERE phone_name = ?", (phone.getPhoneName,))
        id_phone=cursor.fetchone()
        conn.close()
        return id_phone [0] if id_phone else None
    
    # Thực hiện truy vấn SQL để lấy prodcut_id của điện thoại dựa trên 'phone_name'
    def get_product_id_by_phone(self,phone:Phone):
        conn=pyodbc.connect("DRIVER={ODBC Driver 17 for SQL Server};SERVER=ADMIN-PC;DATABASE=SalesPhone;Trusted_Connection=yes;Encrypt=no")
        cursor=conn.cursor()
        cursor.execute("SELECT product_id FROM phones WHERE phone_name = ?", (phone.getPhoneName,))
        id_phone=cursor.fetchone()
        conn.close()
        return id_phone [0] if id_phone else None
    
    # Thực hiện lệnh SQL để chèn liên kết giữa 'phone' và 'comment' vào bảng 'comment_phone'
    def insert_comment_phone(self, phone, comment):
        """Thêm liên kết giữa comment và phone"""
        try:
            if phone is None:
                print("Phone object is None")
                return
            
            # Lấy internal id từ product_id
            internal_id = self.get_internal_id_by_product_id(phone.getId)
            if internal_id is None:
                print(f"No internal ID found for product_id: {phone.getId}")
                return
            
            conn = pyodbc.connect("DRIVER={ODBC Driver 17 for SQL Server};SERVER=ADMIN-PC;DATABASE=SalesPhone;Trusted_Connection=yes;Encrypt=no")
            cursor = conn.cursor()
            
            # Sử dụng internal_id thay vì product_id
            cursor.execute(
                "INSERT INTO comment_phone(id_phone, id_comment) VALUES (?, ?)",
                (internal_id, comment.getId)
            )
            
            cursor.commit()
            cursor.close()
            conn.close()
            
        except Exception as e:
            print(f"Error in insert_comment_phone: {e}")
            traceback.print_exc()
    
    def get_internal_id_by_product_id(self, product_id):
        """Lấy internal ID từ product_id"""
        try:
            conn = pyodbc.connect("DRIVER={ODBC Driver 17 for SQL Server};SERVER=ADMIN-PC;DATABASE=SalesPhone;Trusted_Connection=yes;Encrypt=no")
            cursor = conn.cursor()
            
            cursor.execute(
                "SELECT id FROM phones WHERE product_id = ?",
                (product_id,)
            )
            
            result = cursor.fetchone()
            cursor.close()
            conn.close()
            
            return result[0] if result else None
            
        except Exception as e:
            print(f"Error getting internal ID for product_id {product_id}: {e}")
            traceback.print_exc()
            return None
    
    def get_phone_id_by_comment(self, comment_id):
        conn = None
        cursor = None
        try:
            conn = pyodbc.connect(
                'DRIVER={ODBC Driver 17 for SQL Server};'
                'SERVER=ADMIN-PC;'
                'DATABASE=SalesPhone;'
                'Trusted_Connection=yes;'
                'Encrypt=no'
            )
            cursor = conn.cursor()
            
            # Sử dụng parameterized query để tránh SQL Injection
            query = """
            SELECT id_phone 
            FROM comment_phone 
            WHERE id_comment = ?
            """
            cursor.execute(query, (comment_id,))
            
            result = cursor.fetchone()
            return result[0] if result else None
        
        except pyodbc.Error as e:
            # Log error chi tiết hơn
            print(f"Database error getting phone_id by comment: {e}")
            return None
        
        except Exception as e:
            # Xử lý các ngoại lệ không mong muốn
            print(f"Unexpected error getting phone_id by comment: {e}")
            return None
        
        finally:
            # Đảm bảo đóng kết nối dù có lỗi xảy ra
            if cursor:
                cursor.close()
            if conn:
                conn.close()