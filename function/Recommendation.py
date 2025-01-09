import re
import torch
import traceback
import numpy as np
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from sklearn.preprocessing import MinMaxScaler
from transformers import RobertaConfig, AutoTokenizer
from sklearn.metrics.pairwise import cosine_similarity


from PhoBert.model import RobertaForAIViVN
class SentimentAnalyzer:
    def __init__(self, model, tokenizer):
        """
        Khởi tạo mô hình phân tích cảm xúc với model và tokenizer đã được khởi tạo
        """
        self.model = model  # Sử dụng model đã được khởi tạo
        self.tokenizer = tokenizer  # Sử dụng tokenizer đã được khởi tạo
    
    def predict_sentiment(self, inputs):
        """
        Dự đoán cảm xúc từ inputs tokenized
        """
        try:
            self.model.eval()
            with torch.no_grad():
                outputs = self.model(**inputs)
                logits = outputs.logits if hasattr(outputs, 'logits') else outputs
                prediction = torch.argmax(logits, dim=1).item()
                return prediction
        except Exception as e:
            print(f"Lỗi khi dự đoán sentiment: {e}")
            return None
    
    def analyze_sentiment(self, text):
        """
        Phân tích cảm xúc từ văn bản
        """
        try:
            inputs = self.tokenizer(
                text,
                padding='max_length',
                truncation=True,
                max_length=256,
                return_tensors="pt"
            )
            return self.predict_sentiment(inputs)
        except Exception as e:
            print(f"Lỗi khi phân tích cảm xúc: {e}")
            return None

class ProductSpecParser:
    @staticmethod
    def parse_specifications(specs_str):
        """Phân tích chuỗi specifications thành dict"""
        try:
            specs_str = specs_str.strip()
            if not (specs_str.startswith('{') and specs_str.endswith('}')):
                return None
                
            specs_content = specs_str[1:-1]
            pairs = re.findall(r"'([^']+)'\s*:\s*'([^']+)'", specs_content)
            
            return {key.strip(): value.strip() for key, value in pairs}
        except Exception as e:
            print(f"Lỗi khi parse specifications: {e}")
            return None

    @staticmethod
    def extract_numeric_value(text):
        """Trích xuất giá trị số từ chuỗi"""
        try:
            return int(re.search(r'\d+', text).group())
        except:
            return 0

class ProductFeatureExtractor:
    def __init__(self, sentiment_analyzer):
        self.sentiment_analyzer = sentiment_analyzer
    
    def extract_product_features(self, row):
        """Trích xuất đặc trưng từ một sản phẩm"""
        try:
            # Sử dụng Product ID trực tiếp
            product_id = int(row['Product ID']) if row.get('Product ID') is not None else 0
            
            specs_dict = ProductSpecParser.parse_specifications(str(row.get('Specifications', '')))
            
            if specs_dict:
                ram = ProductSpecParser.extract_numeric_value(specs_dict.get('RAM', '0'))
                storage = ProductSpecParser.extract_numeric_value(specs_dict.get('Dung lượng', '0'))
                rear_camera = ProductSpecParser.extract_numeric_value(specs_dict.get('Camera sau', '0'))
                front_camera = ProductSpecParser.extract_numeric_value(specs_dict.get('Camera trước', '0'))
            else:
                ram = row.get('ram', 0)
                storage = row.get('storage', 0)
                rear_camera = row.get('rear_camera', 0)
                front_camera = row.get('front_camera', 0)

            price = float(str(row['Price']).replace('₫','').replace('.','').strip()) if row.get('Price') else 0
            rating = float(row['User Rating']) if row.get('User Rating') else 0.0
            review_count = ProductSpecParser.extract_numeric_value(str(row.get('Review Count', 0)))
            
            return {
                'Product ID': product_id,
                'Price': price,
                'ram': ram,
                'storage': storage,
                'rear_camera': rear_camera,
                'front_camera': front_camera,
                'User Rating': rating,
                'Review Count': review_count,
                'sentiment': row.get('sentiment', 1),
                'phone_name': row.get('phone_name', '')
            }
        except Exception as e:
            print(f"Lỗi khi trích xuất đặc trưng cho sản phẩm {row.get('Product ID')}: {e}")
            traceback.print_exc()
            return None

class RecommendationSystem:
    def __init__(self, sentiment_analyzer):
        self.sentiment_analyzer = sentiment_analyzer
        self.feature_extractor = ProductFeatureExtractor(sentiment_analyzer)
        
    def create_recommendation_features(self, products_df):
        """Tạo ma trận đặc trưng cho hệ thống gợi ý"""
        try:
            numeric_features = ['Price', 'ram', 'storage', 'rear_camera', 'front_camera', 
                              'User Rating', 'Review Count', 'sentiment']
            
            # Kiểm tra các cột có tồn tại
            missing_features = [f for f in numeric_features if f not in products_df.columns]
            if missing_features:
                print(f"Warning: Missing columns: {missing_features}")
                print("Available columns:", products_df.columns.tolist())
                return np.zeros((len(products_df), len(numeric_features)))  # Trả về ma trận 0 thay vì None
            
            # Chuyển đổi dữ liệu sang numeric
            for feature in numeric_features:
                products_df[feature] = pd.to_numeric(products_df[feature], errors='coerce')
            
            # Điền giá trị NaN bằng 0
            products_df[numeric_features] = products_df[numeric_features].fillna(0)
            
            scaler = MinMaxScaler()
            scaled_features = scaler.fit_transform(products_df[numeric_features])
            
            weights = {
                'sentiment': 0.25,
                'User Rating': 0.15,
                'Price': 0.15,
                'ram': 0.1,
                'storage': 0.1,
                'rear_camera': 0.1,
                'front_camera': 0.05,
                'Review Count': 0.1
            }
            
            # Tạo DataFrame cho các đặc trưng đã scale
            scaled_df = pd.DataFrame(scaled_features, columns=numeric_features)
            
            # Áp dụng trọng số
            weighted_features = scaled_df.multiply(list(weights.values()))
            
            return weighted_features.values
            
        except Exception as e:
            print(f"Lỗi khi tạo ma trận đặc trưng: {e}")
            traceback.print_exc()
            return np.zeros((len(products_df), len(numeric_features)))  # Trả về ma trận 0 thay vì None

    def get_similar_products(self, product_id, features_matrix, products_df, n=5):
        """Tìm các sản phẩm tương tự"""
        try:
            product_id = int(product_id)
            print("Looking for product_id:", product_id)
            print("DataFrame columns:", products_df.columns.tolist())
            print("Available Product IDs:", products_df['Product ID'].unique().tolist())
            
            # Chuyển đổi Product ID sang kiểu int
            products_df['Product ID'] = products_df['Product ID'].astype(int)
            product_indices = products_df[products_df['Product ID'] == product_id].index
            
            if len(product_indices) == 0:
                print(f"Không tìm thấy sản phẩm với ID: {product_id}")
                print("Các ID có sẵn:", sorted(products_df['Product ID'].unique()))
                return None
            
            product_idx = product_indices[0]
            
            if features_matrix.shape[0] == 0:
                print("Ma trận đặc trưng trống")
                return None
            
            similarities = cosine_similarity([features_matrix[product_idx]], features_matrix)
            
            top_indices = similarities[0].argsort()[::-1]
            similar_indices = [idx for idx in top_indices if idx != product_idx][:n]
            
            if len(similar_indices) == 0:
                print("Không tìm thấy sản phẩm tương tự")
                return None
            
            result = products_df.iloc[similar_indices].copy()
            result['similarity_score'] = similarities[0][similar_indices]
            
            print(f"Tìm thấy {len(result)} sản phẩm tương tự")
            print("Original product:", products_df.iloc[product_idx][['Product ID', 'phone_name']])
            print("Similar products:")
            for _, row in result.iterrows():
                print(f"ID: {row['Product ID']}, Name: {row['phone_name']}, Score: {row['similarity_score']:.3f}")
            
            return result
            
        except Exception as e:
            print(f"Lỗi khi tìm sản phẩm tương tự: {e}")
            traceback.print_exc()
            return None

    def analyze_review_and_recommend(self, review_text, product_id, df, n=5):
        """Phân tích cảm xúc và gợi ý sản phẩm"""
        try:
            sentiment = self.sentiment_analyzer.analyze_sentiment(review_text)
            sentiment_text = {0: 'Tiêu cực', 1: 'Trung tính', 2: 'Tích cực'}.get(sentiment, 'Không xác định')
            print(f"Cảm xúc được phân tích: {sentiment_text}")
            
            # Nếu sentiment là tích cực (2), trả về None ngay lập tức
            if sentiment == 2:
                print("Sentiment tích cực, không tạo recommendations")
                return None, sentiment
            
            print("Input DataFrame columns:", df.columns.tolist())
            print("Product ID being searched:", product_id)
            
            products_features = []
            for _, row in df.iterrows():
                features = self.feature_extractor.extract_product_features(row)
                if features:
                    features['sentiment'] = sentiment if str(row['Product ID']) == str(product_id) else 1
                    products_features.append(features)
            
            if not products_features:
                print("Không thể trích xuất đặc trưng từ sản phẩm")
                return None, sentiment
            
            products_df = pd.DataFrame(products_features)
            features_matrix = self.create_recommendation_features(products_df)
            if features_matrix is not None and features_matrix.shape[0] > 0:
                recommendations = self.get_similar_products(product_id, features_matrix, products_df, n)
                return recommendations, sentiment
            else:
                return None, sentiment
            
        except Exception as e:
            print(f"Lỗi trong quá trình phân tích và gợi ý: {e}")
            traceback.print_exc()
            return None, None

def analyze_review_and_recommend(recommendation_system, review_text, product_id, df, n=5):
    return recommendation_system.analyze_review_and_recommend(review_text, product_id, df, n)