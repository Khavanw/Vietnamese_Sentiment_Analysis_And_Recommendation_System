-- Tạo cơ sở dữ liệu SalesPhone
CREATE DATABASE SalesPhone;
GO

USE SalesPhone;
GO

-- Tạo bảng users
CREATE TABLE users (
    id INT IDENTITY PRIMARY KEY,
    username VARCHAR(255) UNIQUE,
    full_name NVARCHAR(255) NOT NULL,
    password VARCHAR(255) NOT NULL,
    created_at DATETIME DEFAULT GETDATE()
);
GO

-- Tạo bảng brands (thương hiệu)
CREATE TABLE brands (
    id INT IDENTITY PRIMARY KEY,
    brand_name NVARCHAR(255) NOT NULL UNIQUE
);
GO

-- Tạo bảng phones với thông tin chi tiết hơn
CREATE TABLE phones (
    id INT IDENTITY PRIMARY KEY,
    phone_name NVARCHAR(255) NOT NULL,
    brand_id INT,
	product_id INT,
    price DECIMAL(15,2),
    ram INT, -- GB
    storage INT, -- GB
    front_camera INT, -- MP
    rear_camera INT, -- MP
    battery INT, -- mAh
    rating FLOAT DEFAULT 0,
    review_count INT DEFAULT 0,
    photo_url NVARCHAR(MAX),
    created_at DATETIME DEFAULT GETDATE(),
    FOREIGN KEY (brand_id) REFERENCES brands(id)
);
GO

-- Tạo bảng comments
CREATE TABLE comments (
    id INT IDENTITY PRIMARY KEY,
    user_id INT NOT NULL,
    phone_id INT NOT NULL,
    comment NVARCHAR(MAX),
    predict NVARCHAR(MAX), -- 0: tiêu cực, 1: trung tính, 2: tích cực
    created_at DATETIME DEFAULT GETDATE(),
    FOREIGN KEY (user_id) REFERENCES users(id),
    FOREIGN KEY (phone_id) REFERENCES phones(id)
);
GO

-- Tạo bảng comment_phone
CREATE TABLE comment_phone (
    id_phone INT NOT NULL, 
    id_comment INT NOT NULL,
    PRIMARY KEY (id_phone, id_comment),
    FOREIGN KEY (id_phone) REFERENCES phones(id),
    FOREIGN KEY (id_comment) REFERENCES comments(id)
);
GO

-- Tạo bảng recommendations
CREATE TABLE recommendations (
    id INT IDENTITY PRIMARY KEY,
    user_id INT NOT NULL,
    source_phone_id INT NOT NULL,
    recommended_phone_id INT NOT NULL,
    similarity_score FLOAT,
    created_at DATETIME DEFAULT GETDATE(),
    FOREIGN KEY (user_id) REFERENCES users(id),
    FOREIGN KEY (source_phone_id) REFERENCES phones(id),
    FOREIGN KEY (recommended_phone_id) REFERENCES phones(id)
);
GO

-- Thêm dữ liệu mẫu cho brands
INSERT INTO brands (brand_name) VALUES
(N'Benco'),
(N'HONOR'),
(N'iPhone (Apple)'),
(N'Itel'),
(N'Masstel'),
(N'Mobell'),
(N'Nokia'),
(N'OPPO'),
(N'realme'),
(N'Samsung'),
(N'Other'),
(N'Tecno'),
(N'Viettel'),
(N'vivo'),
(N'Xiaomi');
GO

-- Thêm dữ liệu mẫu cho phones
INSERT INTO phones (phone_name, brand_id, product_id, price, ram, storage, front_camera, rear_camera, battery, rating, review_count, photo_url) VALUES
(N'Benco 4G G3', 1, 330485, 380000.0, NULL, NULL, NULL, NULL, NULL, 3.7, 3, 'https://cdn.tgdd.vn/Products/Images/42/330485/benco-4g-g3-xanh-thumb-600x600.jpg');
INSERT INTO phones (phone_name, brand_id, product_id, price, ram, storage, front_camera, rear_camera, battery, rating, review_count, photo_url) VALUES
(N'HONOR X5 Plus 4GB/64GB', 2, 313306, 2290000.0, 4.0, 64.0, 5.0, NULL, NULL, 3.7, 12, 'https://cdn.tgdd.vn/Products/Images/42/313306/honor-x5-plus-xanh-thumb-600x600.jpg');
INSERT INTO phones (phone_name, brand_id, product_id, price, ram, storage, front_camera, rear_camera, battery, rating, review_count, photo_url) VALUES
(N'HONOR X8b 8GB/512GB', 2, 324893, 6390000.0, 8.0, 512.0, 50.0, NULL, NULL, 4.3, 47, 'https://cdn.tgdd.vn/Products/Images/42/324893/honor-x8b-green-thumb-1-600x600.jpg');
INSERT INTO phones (phone_name, brand_id, product_id, price, ram, storage, front_camera, rear_camera, battery, rating, review_count, photo_url) VALUES
(N'HONOR X7c 8GB/256GB', 2, 331512, 5490000.0, 8.0, 256.0, 8.0, NULL, NULL, NULL, NULL, 'https://cdn.tgdd.vn/Products/Images/42/331512/honor-x7c-white-thumb-600x600.jpg');
INSERT INTO phones (phone_name, brand_id, product_id, price, ram, storage, front_camera, rear_camera, battery, rating, review_count, photo_url) VALUES
(N'HONOR X6b', 2, 327258, 3690000.0, 6.0, 128.0, 5.0, NULL, NULL, 4.0, 4, 'https://cdn.tgdd.vn/Products/Images/42/327258/honor-x6b-purple-thumb-600x600.jpg');
INSERT INTO phones (phone_name, brand_id, product_id, price, ram, storage, front_camera, rear_camera, battery, rating, review_count, photo_url) VALUES
(N'HONOR 200 5G', 2, 329133, 12090000.0, 12.0, 256.0, 50.0, NULL, NULL, NULL, NULL, 'https://cdn.tgdd.vn/Products/Images/42/329133/honor-200-white-thumb-600x600.jpg');
INSERT INTO phones (phone_name, brand_id, product_id, price, ram, storage, front_camera, rear_camera, battery, rating, review_count, photo_url) VALUES
(N'iPhone 16 Pro Max', 3, 329149, 34490000.0, 8.0, 256.0, 12.0, NULL, NULL, 2.8, 52, 'https://cdn.tgdd.vn/Products/Images/42/329149/iphone-16-pro-max-black-thumb-600x600.jpg');
INSERT INTO phones (phone_name, brand_id, product_id, price, ram, storage, front_camera, rear_camera, battery, rating, review_count, photo_url) VALUES
(N'iPhone 16 Pro', 3, 329143, 28890000.0, 8.0, 128.0, 12.0, NULL, NULL, 2.2, 13, 'https://cdn.tgdd.vn/Products/Images/42/329143/iphone-16-pro-titan-sa-mac.png');
INSERT INTO phones (phone_name, brand_id, product_id, price, ram, storage, front_camera, rear_camera, battery, rating, review_count, photo_url) VALUES
(N'iPhone 16 Plus', 3, 329138, 25990000.0, 8.0, 128.0, 12.0, NULL, NULL, NULL, NULL, 'https://cdn.tgdd.vn/Products/Images/42/329138/iphone-16-plus-den-thumb-600x600.jpg');
INSERT INTO phones (phone_name, brand_id, product_id, price, ram, storage, front_camera, rear_camera, battery, rating, review_count, photo_url) VALUES
(N'iPhone 16', 3, 329135, 22290000.0, 8.0, 128.0, 12.0, NULL, NULL, 2.3, 3, 'https://cdn.tgdd.vn/Products/Images/42/329135/iphone-16-blue-600x600.png');
INSERT INTO phones (phone_name, brand_id, product_id, price, ram, storage, front_camera, rear_camera, battery, rating, review_count, photo_url) VALUES
(N'iPhone 15', 3, 281570, 19890000.0, 6.0, 128.0, 12.0, NULL, NULL, 4.5, 53, 'https://cdn.tgdd.vn/Products/Images/42/281570/iphone-15-hong-thumb-1-600x600.jpg');
INSERT INTO phones (phone_name, brand_id, product_id, price, ram, storage, front_camera, rear_camera, battery, rating, review_count, photo_url) VALUES
(N'iPhone 14', 3, 240259, 17490000.0, 6.0, 128.0, 12.0, 2.0, NULL, 4.4, 132, 'https://cdn.tgdd.vn/Products/Images/42/240259/iPhone-14-thumb-tim-1-600x600.jpg');
INSERT INTO phones (phone_name, brand_id, product_id, price, ram, storage, front_camera, rear_camera, battery, rating, review_count, photo_url) VALUES
(N'iPhone 15 Plus', 3, 303891, 22890000.0, 6.0, 128.0, 12.0, NULL, NULL, 4.4, 42, 'https://cdn.tgdd.vn/Products/Images/42/303891/iphone-15-plus-xanh-la-128gb-thumb-600x600.jpg');
INSERT INTO phones (phone_name, brand_id, product_id, price, ram, storage, front_camera, rear_camera, battery, rating, review_count, photo_url) VALUES
(N'iPhone 12', 3, 213031, 11590000.0, 4.0, 64.0, 12.0, 2.0, NULL, 4.1, 338, 'https://cdn.tgdd.vn/Products/Images/42/213031/iphone-12-xanh-la-new-2-600x600.jpg');
INSERT INTO phones (phone_name, brand_id, product_id, price, ram, storage, front_camera, rear_camera, battery, rating, review_count, photo_url) VALUES
(N'iPhone 11', 3, 153856, 8990000.0, 4.0, 64.0, 12.0, 2.0, NULL, 4.1, 890, 'https://cdn.tgdd.vn/Products/Images/42/153856/iphone-11-trang-600x600.jpg');
INSERT INTO phones (phone_name, brand_id, product_id, price, ram, storage, front_camera, rear_camera, battery, rating, review_count, photo_url) VALUES
(N'iPhone 13', 3, 223602, 13490000.0, 4.0, 128.0, 12.0, 2.0, NULL, 4.2, 605, 'https://cdn.tgdd.vn/Products/Images/42/223602/iphone-13-midnight-2-600x600.jpg');
INSERT INTO phones (phone_name, brand_id, product_id, price, ram, storage, front_camera, rear_camera, battery, rating, review_count, photo_url) VALUES
(N'iPhone 15 Pro Max', 3, 305658, 29590000.0, 8.0, 256.0, 12.0, NULL, NULL, 3.7, 229, 'https://cdn.tgdd.vn/Products/Images/42/305658/iphone-15-pro-max-black-thumbnew-600x600.jpg');
INSERT INTO phones (phone_name, brand_id, product_id, price, ram, storage, front_camera, rear_camera, battery, rating, review_count, photo_url) VALUES
(N'iPhone 14 Plus', 3, 245545, 20090000.0, 6.0, 128.0, 12.0, 2.0, NULL, 4.4, 127, 'https://cdn.tgdd.vn/Products/Images/42/245545/iPhone-14-plus-thumb-xanh-1-600x600.jpg');
INSERT INTO phones (phone_name, brand_id, product_id, price, ram, storage, front_camera, rear_camera, battery, rating, review_count, photo_url) VALUES
(N'iPhone 15 Pro', 3, 303831, 28490000.0, 8.0, 256.0, 12.0, NULL, NULL, 4.5, 49, 'https://cdn.tgdd.vn/Products/Images/42/303831/iphone-15-pro-black-thumbnew-600x600.jpg');
INSERT INTO phones (phone_name, brand_id, product_id, price, ram, storage, front_camera, rear_camera, battery, rating, review_count, photo_url) VALUES
(N'Itel it9211', 4, 329839, 490000.0, NULL, NULL, NULL, NULL, NULL, 4.0, 4, 'https://cdn.tgdd.vn/Products/Images/42/329839/itel-it9211-xanh-thumb-600x600.jpg');
INSERT INTO phones (phone_name, brand_id, product_id, price, ram, storage, front_camera, rear_camera, battery, rating, review_count, photo_url) VALUES
(N'Itel it9310', 4, 329840, 650000.0, NULL, NULL, NULL, NULL, NULL, 4.0, 17, 'https://cdn.tgdd.vn/Products/Images/42/329840/itel-it9310-vang-thumb-600x600.jpg');
INSERT INTO phones (phone_name, brand_id, product_id, price, ram, storage, front_camera, rear_camera, battery, rating, review_count, photo_url) VALUES
(N'Itel it2600', 4, 328399, 490000.0, NULL, NULL, NULL, NULL, NULL, NULL, NULL, 'https://cdn.tgdd.vn/Products/Images/42/328399/itel-it2600-black-thumb-1-600x600.jpg');
INSERT INTO phones (phone_name, brand_id, product_id, price, ram, storage, front_camera, rear_camera, battery, rating, review_count, photo_url) VALUES
(N'Masstel Fami 50 4G', 5, 323546, 600000.0, NULL, NULL, NULL, NULL, NULL, 3.9, 7, 'https://cdn.tgdd.vn/Products/Images/42/323546/masstel-fami-50-green-thumb-600x600.jpg');
INSERT INTO phones (phone_name, brand_id, product_id, price, ram, storage, front_camera, rear_camera, battery, rating, review_count, photo_url) VALUES
(N'Masstel IZI 10 4G', 5, 265311, 410000.0, NULL, NULL, NULL, NULL, NULL, 4.1, 272, 'https://cdn.tgdd.vn/Products/Images/42/265311/masstel-izi-10-4g-xanh-thumb-600x600.jpg');
INSERT INTO phones (phone_name, brand_id, product_id, price, ram, storage, front_camera, rear_camera, battery, rating, review_count, photo_url) VALUES
(N'Masstel IZI T6 4G', 5, 322877, 500000.0, NULL, NULL, NULL, NULL, NULL, 3.8, 22, 'https://cdn.tgdd.vn/Products/Images/42/322877/masstel-izi-t6-green-thumb-600x600.jpg');
INSERT INTO phones (phone_name, brand_id, product_id, price, ram, storage, front_camera, rear_camera, battery, rating, review_count, photo_url) VALUES
(N'Masstel Lux 10', 5, 299611, 420000.0, NULL, NULL, NULL, NULL, NULL, 3.8, 112, 'https://cdn.tgdd.vn/Products/Images/42/299611/masstel-lux-10-xanh-duong-thumb-600x600.jpg');
INSERT INTO phones (phone_name, brand_id, product_id, price, ram, storage, front_camera, rear_camera, battery, rating, review_count, photo_url) VALUES
(N'Masstel Fami 60S 4G', 5, 322876, 700000.0, NULL, NULL, NULL, NULL, NULL, 3.4, 7, 'https://cdn.tgdd.vn/Products/Images/42/322876/masstel-fami-60s-blue-thumb-600x600.jpg');
INSERT INTO phones (phone_name, brand_id, product_id, price, ram, storage, front_camera, rear_camera, battery, rating, review_count, photo_url) VALUES
(N'Mobell M239', 6, 284122, 500000.0, NULL, NULL, NULL, NULL, NULL, 3.9, 171, 'https://cdn.tgdd.vn/Products/Images/42/284122/mobell-m239-xanh-thumb-1-600x600.jpg');
INSERT INTO phones (phone_name, brand_id, product_id, price, ram, storage, front_camera, rear_camera, battery, rating, review_count, photo_url) VALUES
(N'Mobell F209 4G', 6, 299998, 620000.0, NULL, NULL, NULL, NULL, NULL, 3.7, 49, 'https://cdn.tgdd.vn/Products/Images/42/299998/mobell-f209-gold-600x600.jpg');
INSERT INTO phones (phone_name, brand_id, product_id, price, ram, storage, front_camera, rear_camera, battery, rating, review_count, photo_url) VALUES
(N'Mobell F309 4G', 6, 304608, 760000.0, NULL, NULL, NULL, NULL, NULL, 4.3, 61, 'https://cdn.tgdd.vn/Products/Images/42/304608/mobell-f309-trang-thumb-600x600.jpg');
INSERT INTO phones (phone_name, brand_id, product_id, price, ram, storage, front_camera, rear_camera, battery, rating, review_count, photo_url) VALUES
(N'Mobell Rock 4 4G', 6, 288631, 790000.0, NULL, NULL, NULL, NULL, NULL, 4.0, 102, 'https://cdn.tgdd.vn/Products/Images/42/288631/mobell-rock-4-xanh-la-thumb-600x600.jpg');
INSERT INTO phones (phone_name, brand_id, product_id, price, ram, storage, front_camera, rear_camera, battery, rating, review_count, photo_url) VALUES
(N'Mobell M539 4G', 6, 288630, 700000.0, NULL, NULL, NULL, NULL, NULL, 4.0, 104, 'https://cdn.tgdd.vn/Products/Images/42/288630/mobell-m539-vang-thumb-600x600.jpg');
INSERT INTO phones (phone_name, brand_id, product_id, price, ram, storage, front_camera, rear_camera, battery, rating, review_count, photo_url) VALUES
(N'Mobell M331 4G', 6, 314697, 550000.0, NULL, NULL, NULL, NULL, NULL, 3.6, 28, 'NULL');
INSERT INTO phones (phone_name, brand_id, product_id, price, ram, storage, front_camera, rear_camera, battery, rating, review_count, photo_url) VALUES
(N'Nokia 105 4G Pro', 7, 311033, 680000.0, NULL, NULL, NULL, NULL, NULL, 3.3, 50, 'https://cdn.tgdd.vn/Products/Images/42/311033/nokia-105-4g-den-thumb-600x600.jpg');
INSERT INTO phones (phone_name, brand_id, product_id, price, ram, storage, front_camera, rear_camera, battery, rating, review_count, photo_url) VALUES
(N'Nokia 220 4G', 7, 207956, 990000.0, NULL, NULL, NULL, NULL, NULL, 3.5, 38, 'https://cdn.tgdd.vn/Products/Images/42/207956/nokia-220-4g-cam-thumb-600x600.jpg');
INSERT INTO phones (phone_name, brand_id, product_id, price, ram, storage, front_camera, rear_camera, battery, rating, review_count, photo_url) VALUES
(N'Nokia 110 4G Pro', 7, 311034, 750000.0, NULL, NULL, NULL, NULL, NULL, 3.5, 30, 'https://cdn.tgdd.vn/Products/Images/42/311034/nokia-110-4g-tim-thumb-600x600.jpg');
INSERT INTO phones (phone_name, brand_id, product_id, price, ram, storage, front_camera, rear_camera, battery, rating, review_count, photo_url) VALUES
(N'Nokia HMD 105 4G', 7, 329676, 650000.0, NULL, NULL, NULL, NULL, NULL, 4.0, 7, 'https://cdn.tgdd.vn/Products/Images/42/329676/nokia-hmd-105-4g-pink-thumb-600x600.jpg');
INSERT INTO phones (phone_name, brand_id, product_id, price, ram, storage, front_camera, rear_camera, battery, rating, review_count, photo_url) VALUES
(N'Nokia 3210 4G', 7, 326477, 1590000.0, NULL, NULL, NULL, NULL, NULL, 3.8, 19, 'https://cdn.tgdd.vn/Products/Images/42/326477/nokia-3210-4g-yellow-thumb-600x600.jpg');
INSERT INTO phones (phone_name, brand_id, product_id, price, ram, storage, front_camera, rear_camera, battery, rating, review_count, photo_url) VALUES
(N'Nokia 105', 7, 240194, 610000.0, NULL, NULL, NULL, NULL, NULL, 3.5, 364, 'NULL');
INSERT INTO phones (phone_name, brand_id, product_id, price, ram, storage, front_camera, rear_camera, battery, rating, review_count, photo_url) VALUES
(N'OPPO Find X8 5G 16GB/512GB', 8, 322128, 22990000.0, 16.0, 512.0, 32.0, 3.0, NULL, NULL, NULL, 'https://cdn.tgdd.vn/Products/Images/42/322128/oppo-find-x8-black-thumb-600x600.jpg');
INSERT INTO phones (phone_name, brand_id, product_id, price, ram, storage, front_camera, rear_camera, battery, rating, review_count, photo_url) VALUES
(N'OPPO Find X8 Pro 5G 16GB/512GB', 8, 322129, 29990000.0, 16.0, 512.0, 32.0, 4.0, NULL, NULL, NULL, 'https://cdn.tgdd.vn/Products/Images/42/322129/oppo-find-x8-pro-white-thumb-600x600.jpg');
INSERT INTO phones (phone_name, brand_id, product_id, price, ram, storage, front_camera, rear_camera, battery, rating, review_count, photo_url) VALUES
(N'OPPO A3x', 8, 328449, 3290000.0, 4.0, 64.0, 5.0, NULL, NULL, 4.2, 36, 'https://cdn.tgdd.vn/Products/Images/42/328449/oppo-a3x-red-thumb-600x600.jpg');
INSERT INTO phones (phone_name, brand_id, product_id, price, ram, storage, front_camera, rear_camera, battery, rating, review_count, photo_url) VALUES
(N'OPPO A3', 8, 328453, 4990000.0, 6.0, 128.0, 5.0, NULL, NULL, NULL, NULL, 'https://cdn.tgdd.vn/Products/Images/42/328453/oppo-a3-purple-thumb-1-600x600.jpg');
INSERT INTO phones (phone_name, brand_id, product_id, price, ram, storage, front_camera, rear_camera, battery, rating, review_count, photo_url) VALUES
(N'OPPO A18 4GB/64GB', 8, 313153, 3290000.0, 4.0, 64.0, 5.0, NULL, NULL, 4.0, 32, 'https://cdn.tgdd.vn/Products/Images/42/313153/oppo-a18-xanh-thumb-1-2-3-600x600.jpg');
INSERT INTO phones (phone_name, brand_id, product_id, price, ram, storage, front_camera, rear_camera, battery, rating, review_count, photo_url) VALUES
(N'OPPO Reno12 F 5G', 8, 327190, 9190000.0, 12.0, 256.0, 32.0, NULL, NULL, 3.2, 23, 'https://cdn.tgdd.vn/Products/Images/42/327190/oppo-reno12-f-5g-orange-thumb-600x600.jpg');
INSERT INTO phones (phone_name, brand_id, product_id, price, ram, storage, front_camera, rear_camera, battery, rating, review_count, photo_url) VALUES
(N'OPPO Reno12 5G 12GB/256GB Hồng', 8, 321892, 11990000.0, 12.0, 256.0, 32.0, NULL, NULL, 3.8, 5, 'NULL');
INSERT INTO phones (phone_name, brand_id, product_id, price, ram, storage, front_camera, rear_camera, battery, rating, review_count, photo_url) VALUES
(N'OPPO A38', 8, 320836, 4490000.0, 6.0, 128.0, 5.0, NULL, NULL, 4.0, 26, 'https://cdn.tgdd.vn/Products/Images/42/320836/oppo-a38-black-thumb-600x600.jpg');
INSERT INTO phones (phone_name, brand_id, product_id, price, ram, storage, front_camera, rear_camera, battery, rating, review_count, photo_url) VALUES
(N'OPPO Reno11 Pro 5G 12GB/512GB', 8, 314210, 11990000.0, 12.0, 512.0, 32.0, NULL, NULL, 4.8, 8, 'NULL');
INSERT INTO phones (phone_name, brand_id, product_id, price, ram, storage, front_camera, rear_camera, battery, rating, review_count, photo_url) VALUES
(N'OPPO Reno10 Pro+ 5G 12GB/256GB', 8, 306980, 19990000.0, 12.0, 256.0, 32.0, NULL, NULL, 3.8, 13, 'NULL');
INSERT INTO phones (phone_name, brand_id, product_id, price, ram, storage, front_camera, rear_camera, battery, rating, review_count, photo_url) VALUES
(N'OPPO A60', 8, 323543, 5290000.0, 8.0, 128.0, 8.0, NULL, NULL, 3.9, 59, 'https://cdn.tgdd.vn/Products/Images/42/323543/oppo-a60-blue-thumb-600x600.jpg');
INSERT INTO phones (phone_name, brand_id, product_id, price, ram, storage, front_camera, rear_camera, battery, rating, review_count, photo_url) VALUES
(N'OPPO Reno12 F 8GB/256GB', 8, 328306, 8190000.0, 8.0, 256.0, 32.0, NULL, NULL, 2.4, 5, 'NULL');
INSERT INTO phones (phone_name, brand_id, product_id, price, ram, storage, front_camera, rear_camera, battery, rating, review_count, photo_url) VALUES
(N'OPPO Reno12 5G', 8, 327191, 11990000.0, 12.0, 256.0, 32.0, NULL, NULL, 3.9, 8, 'https://cdn.tgdd.vn/Products/Images/42/327191/oppo-reno12-5g-sliver-thumb-1-600x600.jpg');
INSERT INTO phones (phone_name, brand_id, product_id, price, ram, storage, front_camera, rear_camera, battery, rating, review_count, photo_url) VALUES
(N'OPPO Reno12 Pro 5G 12GB/512GB', 8, 322124, 17990000.0, 12.0, 512.0, 50.0, NULL, NULL, 5.0, 3, 'NULL');
INSERT INTO phones (phone_name, brand_id, product_id, price, ram, storage, front_camera, rear_camera, battery, rating, review_count, photo_url) VALUES
(N'OPPO A79 5G 8GB/256GB', 8, 316776, 7490000.0, 8.0, 256.0, 8.0, NULL, NULL, 3.5, 32, 'NULL');
INSERT INTO phones (phone_name, brand_id, product_id, price, ram, storage, front_camera, rear_camera, battery, rating, review_count, photo_url) VALUES
(N'OPPO A78 8GB/256GB', 8, 309847, 6490000.0, 8.0, 256.0, 8.0, NULL, NULL, 3.8, 114, 'NULL');
INSERT INTO phones (phone_name, brand_id, product_id, price, ram, storage, front_camera, rear_camera, battery, rating, review_count, photo_url) VALUES
(N'OPPO Find N3 Flip 5G 12GB/256GB Đen/Vàng đồng', 8, 309835, 22990000.0, 12.0, 256.0, 32.0, NULL, NULL, NULL, NULL, 'NULL');
INSERT INTO phones (phone_name, brand_id, product_id, price, ram, storage, front_camera, rear_camera, battery, rating, review_count, photo_url) VALUES
(N'OPPO Find N3 5G 16GB/512GB', 8, 302953, 41990000.0, 16.0, 512.0, NULL, NULL, NULL, NULL, NULL, 'NULL');
INSERT INTO phones (phone_name, brand_id, product_id, price, ram, storage, front_camera, rear_camera, battery, rating, review_count, photo_url) VALUES
(N'OPPO A58', 8, 311354, 5490000.0, 8.0, 128.0, 8.0, NULL, NULL, 3.7, 82, 'https://cdn.tgdd.vn/Products/Images/42/311354/oppo-a58-4g-green-thumb-600x600.jpg');
INSERT INTO phones (phone_name, brand_id, product_id, price, ram, storage, front_camera, rear_camera, battery, rating, review_count, photo_url) VALUES
(N'realme Note 50', 9, 321434, 2490000.0, 3.0, 64.0, 5.0, NULL, NULL, 3.5, 32, 'https://cdn.tgdd.vn/Products/Images/42/321434/realme-note-50-blue-thumb-600x600.jpg');
INSERT INTO phones (phone_name, brand_id, product_id, price, ram, storage, front_camera, rear_camera, battery, rating, review_count, photo_url) VALUES
(N'realme Note 60', 9, 329328, 3090000.0, 4.0, 64.0, 5.0, NULL, NULL, NULL, NULL, 'https://cdn.tgdd.vn/Products/Images/42/329328/realme-note-60-black-thumb-600x600.jpg');
INSERT INTO phones (phone_name, brand_id, product_id, price, ram, storage, front_camera, rear_camera, battery, rating, review_count, photo_url) VALUES
(N'realme C65', 9, 323002, 3590000.0, 8.0, 256.0, 8.0, NULL, NULL, 4.3, 12, 'https://cdn.tgdd.vn/Products/Images/42/323002/realme-c65-purple-thumb-600x600.jpg');
INSERT INTO phones (phone_name, brand_id, product_id, price, ram, storage, front_camera, rear_camera, battery, rating, review_count, photo_url) VALUES
(N'realme C67', 9, 319658, 3790000.0, 8.0, 128.0, 8.0, NULL, NULL, 3.9, 23, 'https://cdn.tgdd.vn/Products/Images/42/319658/realme-c67-xanh-thumb-600x600.jpg');
INSERT INTO phones (phone_name, brand_id, product_id, price, ram, storage, front_camera, rear_camera, battery, rating, review_count, photo_url) VALUES
(N'realme C53 8GB/256GB', 9, 317624, 3590000.0, 8.0, 256.0, 8.0, NULL, NULL, 3.4, 27, 'https://cdn.tgdd.vn/Products/Images/42/317624/realme-c53-gold-thumb-600x600.jpeg');
INSERT INTO phones (phone_name, brand_id, product_id, price, ram, storage, front_camera, rear_camera, battery, rating, review_count, photo_url) VALUES
(N'realme C65s', 9, 328625, 4690000.0, 8.0, 128.0, 8.0, NULL, NULL, 3.3, 7, 'https://cdn.tgdd.vn/Products/Images/42/328625/realme-c65s-green-thumb-600x600.jpg');
INSERT INTO phones (phone_name, brand_id, product_id, price, ram, storage, front_camera, rear_camera, battery, rating, review_count, photo_url) VALUES
(N'realme 12', 9, 319466, 7790000.0, 8.0, 256.0, 16.0, NULL, NULL, 3.0, 8, 'https://cdn.tgdd.vn/Products/Images/42/319466/realme-12-green-thumb-600x600.jpg');
INSERT INTO phones (phone_name, brand_id, product_id, price, ram, storage, front_camera, rear_camera, battery, rating, review_count, photo_url) VALUES
(N'realme C60 4GB/64GB', 9, 322919, 2790000.0, 4.0, 64.0, 5.0, NULL, NULL, 4.3, 3, 'NULL');
INSERT INTO phones (phone_name, brand_id, product_id, price, ram, storage, front_camera, rear_camera, battery, rating, review_count, photo_url) VALUES
(N'realme C61', 9, 327975, 3490000.0, 4.0, 128.0, 5.0, NULL, NULL, NULL, NULL, 'https://cdn.tgdd.vn/Products/Images/42/327975/realme-c61-gold-thumb-600x600.jpg');
INSERT INTO phones (phone_name, brand_id, product_id, price, ram, storage, front_camera, rear_camera, battery, rating, review_count, photo_url) VALUES
(N'realme 13+ 5G', 9, 330620, 9290000.0, 8.0, 256.0, 16.0, NULL, NULL, NULL, NULL, 'https://cdn.tgdd.vn/Products/Images/42/330620/realme-13-plus-tim-thumb-600x600.jpg');
INSERT INTO phones (phone_name, brand_id, product_id, price, ram, storage, front_camera, rear_camera, battery, rating, review_count, photo_url) VALUES
(N'Samsung Galaxy S24 Ultra 5G', 10, 307174, 29990000.0, 12.0, 256.0, 12.0, NULL, NULL, 4.0, 101, 'https://cdn.tgdd.vn/Products/Images/42/307174/samsung-galaxy-s24-ultra-grey-thumbnew-600x600.jpg');
INSERT INTO phones (phone_name, brand_id, product_id, price, ram, storage, front_camera, rear_camera, battery, rating, review_count, photo_url) VALUES
(N'Samsung Galaxy A16', 10, 331207, 5890000.0, 8.0, 128.0, 13.0, NULL, NULL, NULL, NULL, 'https://cdn.tgdd.vn/Products/Images/42/331207/samsung-galaxy-a16-green-thumbnew-600x600.jpg');
INSERT INTO phones (phone_name, brand_id, product_id, price, ram, storage, front_camera, rear_camera, battery, rating, review_count, photo_url) VALUES
(N'Samsung Galaxy A16 5G', 10, 331204, 6990000.0, 8.0, 256.0, 13.0, NULL, NULL, NULL, NULL, 'https://cdn.tgdd.vn/Products/Images/42/331204/samsung-galaxy-a16-5g-gold-thumbnew-600x600.jpg');
INSERT INTO phones (phone_name, brand_id, product_id, price, ram, storage, front_camera, rear_camera, battery, rating, review_count, photo_url) VALUES
(N'Samsung Galaxy A55 5G', 10, 322096, 10990000.0, 12.0, 256.0, 32.0, NULL, NULL, 3.8, 67, 'https://cdn.tgdd.vn/Products/Images/42/322096/samsung-galaxy-a55-5g-xanh-thumb-1-600x600.jpg');
INSERT INTO phones (phone_name, brand_id, product_id, price, ram, storage, front_camera, rear_camera, battery, rating, review_count, photo_url) VALUES
(N'Samsung Galaxy A06', 10, 328752, 2890000.0, 4.0, 64.0, 8.0, NULL, NULL, NULL, NULL, 'https://cdn.tgdd.vn/Products/Images/42/328752/samsung-galaxy-a06-blue-thumb-1-600x600.jpg');
INSERT INTO phones (phone_name, brand_id, product_id, price, ram, storage, front_camera, rear_camera, battery, rating, review_count, photo_url) VALUES
(N'Samsung Galaxy S23 FE 5G', 10, 306994, 10390000.0, 8.0, 128.0, 10.0, NULL, NULL, 3.0, 78, 'https://cdn.tgdd.vn/Products/Images/42/306994/samsung-galaxy-s23-fe-mint-thumbnew-600x600.jpg');
INSERT INTO phones (phone_name, brand_id, product_id, price, ram, storage, front_camera, rear_camera, battery, rating, review_count, photo_url) VALUES
(N'Samsung Galaxy Z Fold6 5G', 10, 320721, 41990000.0, 12.0, 256.0, 10.0, NULL, NULL, 4.9, 25, 'https://cdn.tgdd.vn/Products/Images/42/320721/samsung-galaxy-z-fold6-xam-thumbn-600x600.jpg');
INSERT INTO phones (phone_name, brand_id, product_id, price, ram, storage, front_camera, rear_camera, battery, rating, review_count, photo_url) VALUES
(N'Samsung Galaxy A35 5G', 10, 321772, 8290000.0, 8.0, 256.0, 13.0, NULL, NULL, 3.4, 46, 'https://cdn.tgdd.vn/Products/Images/42/321772/samsung-galaxy-a35-5g-xanh-thumb-1-600x600.jpg');
INSERT INTO phones (phone_name, brand_id, product_id, price, ram, storage, front_camera, rear_camera, battery, rating, review_count, photo_url) VALUES
(N'Samsung Galaxy S24 FE 5G', 10, 322789, 16990000.0, 8.0, 128.0, 10.0, NULL, NULL, 5.0, 11, 'https://cdn.tgdd.vn/Products/Images/42/322789/samsung-galaxy-s24-fe-mint-thumb-1-600x600.jpg');
INSERT INTO phones (phone_name, brand_id, product_id, price, ram, storage, front_camera, rear_camera, battery, rating, review_count, photo_url) VALUES
(N'Samsung Galaxy Z Flip6 5G', 10, 320722, 26990000.0, 12.0, 256.0, 10.0, NULL, NULL, 5.0, 15, 'https://cdn.tgdd.vn/Products/Images/42/320722/samsung-galaxy-z-flip6-xanh-thumbn-600x600.jpg');
INSERT INTO phones (phone_name, brand_id, product_id, price, ram, storage, front_camera, rear_camera, battery, rating, review_count, photo_url) VALUES
(N'Samsung Galaxy M55 5G', 10, 327372, 10190000.0, 12.0, 256.0, 50.0, NULL, NULL, 4.3, 6, 'https://cdn.tgdd.vn/Products/Images/42/327372/samsung-galaxy-m55-5g-black-thumb-600x600.jpg');
INSERT INTO phones (phone_name, brand_id, product_id, price, ram, storage, front_camera, rear_camera, battery, rating, review_count, photo_url) VALUES
(N'Samsung Galaxy S24 5G', 10, 319665, 19990000.0, 8.0, 256.0, 12.0, NULL, NULL, 3.9, 45, 'https://cdn.tgdd.vn/Products/Images/42/319665/TimerThumb/samsung-galaxy-s24-thumbkm1.jpg');
INSERT INTO phones (phone_name, brand_id, product_id, price, ram, storage, front_camera, rear_camera, battery, rating, review_count, photo_url) VALUES
(N'Samsung Galaxy S24+ 5G', 10, 307172, 20990000.0, 12.0, 256.0, 12.0, NULL, NULL, 4.2, 12, 'https://cdn.tgdd.vn/Products/Images/42/307172/samsung-galaxy-s24-plus-violet-thumbnew-600x600.jpg');
INSERT INTO phones (phone_name, brand_id, product_id, price, ram, storage, front_camera, rear_camera, battery, rating, review_count, photo_url) VALUES
(N'Samsung Galaxy A15 8GB/256GB', 10, 316075, 4990000.0, 8.0, 256.0, 13.0, NULL, NULL, 3.2, 104, 'NULL');
INSERT INTO phones (phone_name, brand_id, product_id, price, ram, storage, front_camera, rear_camera, battery, rating, review_count, photo_url) VALUES
(N'Samsung Galaxy A15 5G 8GB/256GB', 10, 319584, 5090000.0, 8.0, 256.0, 13.0, NULL, NULL, 3.3, 72, 'NULL');
INSERT INTO phones (phone_name, brand_id, product_id, price, ram, storage, front_camera, rear_camera, battery, rating, review_count, photo_url) VALUES
(N'Samsung Galaxy A05s', 10, 317530, 3790000.0, 6.0, 128.0, 13.0, NULL, NULL, 3.1, 72, 'https://cdn.tgdd.vn/Products/Images/42/317530/samsung-galaxy-a05s-sliver-thumbnew-600x600.jpg');
INSERT INTO phones (phone_name, brand_id, product_id, price, ram, storage, front_camera, rear_camera, battery, rating, review_count, photo_url) VALUES
(N'Samsung Galaxy A25 5G', 10, 319904, 6490000.0, 8.0, 128.0, 13.0, NULL, NULL, 3.3, 47, 'https://cdn.tgdd.vn/Products/Images/42/319904/samsung-galaxy-a25-5g-xanh-duong-thumb-600x600.jpg');
INSERT INTO phones (phone_name, brand_id, product_id, price, ram, storage, front_camera, rear_camera, battery, rating, review_count, photo_url) VALUES
(N'Samsung Galaxy S23 Ultra 5G 8GB/256GB', 10, 249948, 20990000.0, 8.0, 256.0, 12.0, NULL, NULL, 4.4, 149, 'NULL');
INSERT INTO phones (phone_name, brand_id, product_id, price, ram, storage, front_camera, rear_camera, battery, rating, review_count, photo_url) VALUES
(N'Samsung Galaxy M35 5G 8GB/256GB', 10, 323563, 7990000.0, 8.0, 256.0, 13.0, NULL, NULL, 3.7, 41, 'NULL');
INSERT INTO phones (phone_name, brand_id, product_id, price, ram, storage, front_camera, rear_camera, battery, rating, review_count, photo_url) VALUES
(N'Samsung Galaxy M15 5G', 10, 325073, 4290000.0, 4.0, 128.0, 13.0, NULL, NULL, 4.0, 9, 'https://cdn.tgdd.vn/Products/Images/42/325073/samsung-galaxy-m15-5g-blue-thumb-1-600x600.jpg');
INSERT INTO phones (phone_name, brand_id, product_id, price, ram, storage, front_camera, rear_camera, battery, rating, review_count, photo_url) VALUES
(N'TCL 406s 4GB/64GB', 11, 324994, 1890000.0, 4.0, 64.0, 5.0, NULL, NULL, 4.2, 9, 'https://cdn.tgdd.vn/Products/Images/42/324994/tcl-406s-blue-thumb-600x600.jpg');
INSERT INTO phones (phone_name, brand_id, product_id, price, ram, storage, front_camera, rear_camera, battery, rating, review_count, photo_url) VALUES
(N'Tecno Spark GO 1 3GB/64GB', 12, 329865, 1990000.0, 3.0, 64.0, 8.0, NULL, NULL, NULL, NULL, 'https://cdn.tgdd.vn/Products/Images/42/329865/tecno-spark-go-1-white-thumb-600x600.jpg');
INSERT INTO phones (phone_name, brand_id, product_id, price, ram, storage, front_camera, rear_camera, battery, rating, review_count, photo_url) VALUES
(N'Tecno Spark 20C 8GB/128GB', 12, 325155, 2490000.0, 8.0, 128.0, 8.0, NULL, NULL, 3.4, 5, 'https://cdn.tgdd.vn/Products/Images/42/325155/tecno-spark-20c-thumb-600x600.jpg');
INSERT INTO phones (phone_name, brand_id, product_id, price, ram, storage, front_camera, rear_camera, battery, rating, review_count, photo_url) VALUES
(N'Tecno Spark Go 2024 3GB/64GB', 12, 325154, 1890000.0, 3.0, 64.0, 8.0, NULL, NULL, 4.0, 29, 'https://cdn.tgdd.vn/Products/Images/42/325154/tecno-spark-go-2024-yellow-thumb-600x600.jpg');
INSERT INTO phones (phone_name, brand_id, product_id, price, ram, storage, front_camera, rear_camera, battery, rating, review_count, photo_url) VALUES
(N'Viettel Sumo 4G T2', 13, 330028, 550000.0, NULL, NULL, NULL, NULL, NULL, NULL, NULL, 'https://cdn.tgdd.vn/Products/Images/42/330028/viettel-sumo-4g-t2-black-thumb-600x600.jpg');
INSERT INTO phones (phone_name, brand_id, product_id, price, ram, storage, front_camera, rear_camera, battery, rating, review_count, photo_url) VALUES
(N'vivo V40 Lite 8GB/256GB', 14, 329959, 8190000.0, 8.0, 256.0, 32.0, NULL, NULL, 3.0, 3, 'https://cdn.tgdd.vn/Products/Images/42/329959/vivo-v40-lite-bac-thumb-600x600.jpg');
INSERT INTO phones (phone_name, brand_id, product_id, price, ram, storage, front_camera, rear_camera, battery, rating, review_count, photo_url) VALUES
(N'vivo Y100', 14, 302197, 6490000.0, 8.0, 256.0, 8.0, NULL, NULL, 3.6, 17, 'https://cdn.tgdd.vn/Products/Images/42/302197/vivo-y100-xanh-thumb-1-600x600.jpg');
INSERT INTO phones (phone_name, brand_id, product_id, price, ram, storage, front_camera, rear_camera, battery, rating, review_count, photo_url) VALUES
(N'vivo Y03', 14, 322996, 3290000.0, 4.0, 128.0, 5.0, NULL, NULL, 3.9, 11, 'https://cdn.tgdd.vn/Products/Images/42/322996/vivo-y03-xanh-thumb-1-600x600.jpg');
INSERT INTO phones (phone_name, brand_id, product_id, price, ram, storage, front_camera, rear_camera, battery, rating, review_count, photo_url) VALUES
(N'vivo Y36 8GB/256GB', 14, 307203, 5190000.0, 8.0, 256.0, 16.0, NULL, NULL, 4.2, 196, 'https://cdn.tgdd.vn/Products/Images/42/307203/vivo-y36-xanh-thumbnew-600x600.jpg');
INSERT INTO phones (phone_name, brand_id, product_id, price, ram, storage, front_camera, rear_camera, battery, rating, review_count, photo_url) VALUES
(N'vivo Y28', 14, 326016, 5490000.0, 8.0, 128.0, 8.0, NULL, NULL, 3.5, 21, 'https://cdn.tgdd.vn/Products/Images/42/326016/vivo-y28-vang-thumb-600x600.jpg');
INSERT INTO phones (phone_name, brand_id, product_id, price, ram, storage, front_camera, rear_camera, battery, rating, review_count, photo_url) VALUES
(N'vivo Y19s', 14, 331200, 4190000.0, 6.0, 128.0, 5.0, NULL, NULL, NULL, NULL, 'https://cdn.tgdd.vn/Products/Images/42/331200/vivo-y19s-bac-thumb-600x600.jpg');
INSERT INTO phones (phone_name, brand_id, product_id, price, ram, storage, front_camera, rear_camera, battery, rating, review_count, photo_url) VALUES
(N'vivo V30 5G 12GB/512GB', 14, 319214, 11990000.0, 12.0, 512.0, 50.0, NULL, NULL, 4.2, 13, 'NULL');
INSERT INTO phones (phone_name, brand_id, product_id, price, ram, storage, front_camera, rear_camera, battery, rating, review_count, photo_url) VALUES
(N'vivo Y18', 14, 327254, 3490000.0, 4.0, 128.0, 8.0, NULL, NULL, NULL, NULL, 'https://cdn.tgdd.vn/Products/Images/42/327254/vivo-y18-nau-thumb-600x600.jpg');
INSERT INTO phones (phone_name, brand_id, product_id, price, ram, storage, front_camera, rear_camera, battery, rating, review_count, photo_url) VALUES
(N'vivo V30e 5G', 14, 325136, 10490000.0, 12.0, 256.0, 32.0, NULL, NULL, 3.8, 5, 'https://cdn.tgdd.vn/Products/Images/42/325136/vivo-v30e-nau-thumb-1-600x600.jpg');
INSERT INTO phones (phone_name, brand_id, product_id, price, ram, storage, front_camera, rear_camera, battery, rating, review_count, photo_url) VALUES
(N'vivo Y03T 4GB/128GB', 14, 329005, 3290000.0, 4.0, 128.0, 5.0, NULL, NULL, NULL, NULL, 'NULL');
INSERT INTO phones (phone_name, brand_id, product_id, price, ram, storage, front_camera, rear_camera, battery, rating, review_count, photo_url) VALUES
(N'Xiaomi Redmi Note 13', 15, 309831, 4390000.0, 8.0, 128.0, 16.0, NULL, NULL, 3.2, 252, 'https://cdn.tgdd.vn/Products/Images/42/309831/xiaomi-redmi-note-13-gold-thumb-600x600.jpg');
INSERT INTO phones (phone_name, brand_id, product_id, price, ram, storage, front_camera, rear_camera, battery, rating, review_count, photo_url) VALUES
(N'Xiaomi Redmi Note 13 Pro', 15, 314206, 5990000.0, 8.0, 128.0, 16.0, NULL, NULL, 3.3, 68, 'https://cdn.tgdd.vn/Products/Images/42/314206/xiaomi-redmi-note-13-green-thumb-600x600.jpg');
INSERT INTO phones (phone_name, brand_id, product_id, price, ram, storage, front_camera, rear_camera, battery, rating, review_count, photo_url) VALUES
(N'Xiaomi Redmi 13', 15, 325800, 3790000.0, 6.0, 128.0, 13.0, NULL, NULL, 3.5, 54, 'https://cdn.tgdd.vn/Products/Images/42/325800/redmi-13-blue-thumb-600x600.jpg');
INSERT INTO phones (phone_name, brand_id, product_id, price, ram, storage, front_camera, rear_camera, battery, rating, review_count, photo_url) VALUES
(N'Xiaomi 14T 5G', 15, 329938, 11990000.0, 12.0, 256.0, 32.0, NULL, NULL, 4.1, 17, 'https://cdn.tgdd.vn/Products/Images/42/329938/xiaomi-14t-grey-thumb-600x600.jpg');
INSERT INTO phones (phone_name, brand_id, product_id, price, ram, storage, front_camera, rear_camera, battery, rating, review_count, photo_url) VALUES
(N'Xiaomi 14T Pro 5G', 15, 329940, 15490000.0, 12.0, 256.0, 32.0, NULL, NULL, 3.3, 7, 'https://cdn.tgdd.vn/Products/Images/42/329940/xiaomi-14t-pro-blue-thumb-600x600.jpg');
INSERT INTO phones (phone_name, brand_id, product_id, price, ram, storage, front_camera, rear_camera, battery, rating, review_count, photo_url) VALUES
(N'Xiaomi Redmi A3', 15, 320734, 2090000.0, 3.0, 64.0, 5.0, NULL, NULL, 3.5, 21, 'https://cdn.tgdd.vn/Products/Images/42/320734/xiaomi-redmi-a3-xanh-l%C3%A1-thumb-600x600.jpg');
INSERT INTO phones (phone_name, brand_id, product_id, price, ram, storage, front_camera, rear_camera, battery, rating, review_count, photo_url) VALUES
(N'Xiaomi Redmi Note 13 Pro 5G', 15, 319670, 7790000.0, 8.0, 256.0, 16.0, NULL, NULL, 3.5, 222, 'https://cdn.tgdd.vn/Products/Images/42/319670/xiaomi-redmi-note-13-pro-5g-xanhla-thumb-600x600.jpg');
INSERT INTO phones (phone_name, brand_id, product_id, price, ram, storage, front_camera, rear_camera, battery, rating, review_count, photo_url) VALUES
(N'Xiaomi 14 5G', 15, 298538, 21490000.0, 12.0, 512.0, 32.0, NULL, NULL, 4.0, 33, 'https://cdn.tgdd.vn/Products/Images/42/298538/xiaomi-14-green-thumbnew-600x600.jpg');
INSERT INTO phones (phone_name, brand_id, product_id, price, ram, storage, front_camera, rear_camera, battery, rating, review_count, photo_url) VALUES
(N'Xiaomi Redmi 14C', 15, 329008, 3090000.0, 6.0, 128.0, 13.0, NULL, NULL, 2.9, 7, 'https://cdn.tgdd.vn/Products/Images/42/329008/xiaomi-redmi-14c-blue-1-600x600.jpg');
INSERT INTO phones (phone_name, brand_id, product_id, price, ram, storage, front_camera, rear_camera, battery, rating, review_count, photo_url) VALUES
(N'Xiaomi 14T 5G 12GB/512GB Xanh', 15, 329892, 12990000.0, 12.0, 512.0, 32.0, NULL, NULL, NULL, NULL, 'NULL');
INSERT INTO phones (phone_name, brand_id, product_id, price, ram, storage, front_camera, rear_camera, battery, rating, review_count, photo_url) VALUES
(N'Xiaomi POCO M6 6GB/128GB', 15, 327343, 3490000.0, 6.0, 128.0, 13.0, NULL, NULL, 2.8, 12, 'NULL');
INSERT INTO phones (phone_name, brand_id, product_id, price, ram, storage, front_camera, rear_camera, battery, rating, review_count, photo_url) VALUES
(N'Xiaomi 14 Ultra 5G 16GB/512GB', 15, 313889, 29990000.0, 16.0, 512.0, 32.0, 4.0, NULL, 4.4, 8, 'NULL');
GO


INSERT INTO users (username, full_name, password) VALUES
('user1', N'Nguyễn Văn A', '123'),
('user2', N'Trần Thị B', '123'),
('user3', N'Lê Văn C', '123'),
('user4', N'Phạm Thị D', '123');
GO