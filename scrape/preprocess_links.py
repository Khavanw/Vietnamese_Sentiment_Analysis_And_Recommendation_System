import pandas as pd

file_path = "data/data_orginal/Phone_Links.csv"
df = pd.read_csv(file_path)

print(f"Kích thước tập dữ liệu gốc: {df.shape}")

df = df.drop_duplicates()

# Làm sạch cột 'price' bằng cách xóa ký hiệu tiền '₫' và dấu phẩy . sau đó chuyển đổi thành số thực
def convert_price_to_float(price_str): 
    price_str = price_str.replace('₫', '').strip()
    price_str = price_str.replace('.', '')
    return float(price_str)

df['Price'] = df['Price'].apply(convert_price_to_float)

print(f"Kích thước tập dữ liệu đã được làm sạch: {df.shape}")

output_file_path = "data/data_orginal/Cleaned_Phone_Links.csv"
df.to_csv(output_file_path, index=False)

print(f"Đã lưu tập dữ liệu đã được làm sạch vào {output_file_path}")