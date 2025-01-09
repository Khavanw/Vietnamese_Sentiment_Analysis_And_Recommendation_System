use SalesPhone;

SELECT * FROM dbo.comments;
SELECT * FROM dbo.phones;

-- Xóa dữ liệu từ bảng liên quan
DELETE FROM dbo.comment_phone WHERE id_comment IN (SELECT id FROM dbo.comments); 

DELETE FROM dbo.comments;
DELETE FROM dbo.phones;
