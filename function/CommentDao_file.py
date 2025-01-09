import pyodbc
from function.Comment_file import Comment
from function.User_file import User
from function.PhoneDao_file import PhoneDao
import traceback

class CommentDao:
    def __init__(self):
        self.connection_string = 'DRIVER={ODBC Driver 17 for SQL Server};SERVER=ADMIN-PC;DATABASE=SalesPhone;Trusted_Connection=yes;Encrypt=no'

    # Thêm bình luận mới vào bảng 'comment'
    def insert_comment(self, user: User, comment: Comment, phone_id: int):
        """Thêm comment mới"""
        try:
            # Lấy internal id của phone từ product_id
            phoneDao = PhoneDao()
            internal_id = phoneDao.get_internal_id_by_product_id(phone_id)
            
            if internal_id is None:
                print(f"No internal ID found for product_id: {phone_id}")
                return
                
            conn = pyodbc.connect("DRIVER={ODBC Driver 17 for SQL Server};SERVER=ADMIN-PC;DATABASE=SalesPhone;Trusted_Connection=yes;Encrypt=no")
            cursor = conn.cursor()
            
            cursor.execute(
                "INSERT INTO comments(user_id, phone_id, comment) VALUES (?, ?, ?)",
                (user.getUserId, internal_id, comment.getComment)
            )
            
            cursor.commit()
            cursor.close()
            conn.close()
            
        except Exception as e:
            print(f"Error inserting comments: {e}")
            traceback.print_exc()

    # Lấy tất cả các bình luận từ bảng 'comment'
    def get_comment_by_user(self):
        try:
            with pyodbc.connect(self.connection_string) as conn:
                with conn.cursor() as cursor:
                    cursor.execute("SELECT id, comment FROM comments")
                    comments = cursor.fetchall()
                    return comments
        except pyodbc.Error as e:
            print("Error fetching comments: ", e)
            return []

    def get_comments_by_phone(self, phone_id):
        try:
            with pyodbc.connect(self.connection_string) as conn:
                with conn.cursor() as cursor:
                    cursor.execute("SELECT id, comment FROM comments WHERE phone_id = ?", (phone_id,))
                    comments = cursor.fetchall()
                    return comments
        except pyodbc.Error as e:
            print("Error fetching comments: ", e)
            return []
        
    #  Lấy ID của bình luận mới nhất.
    def get_comment_id_by_user(self):
        try:
            with pyodbc.connect(self.connection_string) as conn:
                with conn.cursor() as cursor:
                    cursor.execute("SELECT TOP 1 id FROM comments ORDER BY id DESC")
                    comment_id = cursor.fetchone()
                    return comment_id[0] if comment_id else None
        except pyodbc.Error as e:
            print("Error fetching comments ID: ", e)
            return None
        
    # Lấy thống kê về số lượng bình luận theo cảm xúc (Positive, Negative, Neutral) cho từng loại điện thoại.
    def statistical(self):
        try:
            with pyodbc.connect(self.connection_string) as conn:
                with conn.cursor() as cursor:
                    cursor.execute("""
                        SELECT 
                            phones.phone_name,
                            COUNT(CASE WHEN comments.predict = 2 THEN 1 END) AS number_of_positives,
                            COUNT(CASE WHEN comments.predict = 0 THEN 1 END) AS number_of_negatives,
                            COUNT(CASE WHEN comments.predict = 1 THEN 1 END) AS number_of_neutrals
                        FROM 
                            phones
                        JOIN 
                            comment_phone ON phones.id = comment_phone.id_phone 
                        JOIN 
                            comments ON comments.id = comment_phone.id_comment
                        GROUP BY 
                            phones.phone_name;
                    """)
                    result = cursor.fetchall()
                    return result
        except pyodbc.Error as e:
            print("Error fetching statistics: ", e)
            return []
        
    # Cập nhật cảm xúc của bình luận.
    def update_comment(self, comment: Comment):
        if comment is not None:
            try:
                with pyodbc.connect(self.connection_string) as conn:
                    with conn.cursor() as cursor:
                        cursor.execute("UPDATE comments SET predict = ? WHERE id = ?", (comment.getPredict, comment.getId))
                        conn.commit()
            except pyodbc.Error as e:
                print("Error updating comment: ", e)
        else:
            print("Comment not found.")
