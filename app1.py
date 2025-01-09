from flask import Flask, render_template, request, redirect, url_for, session, flash
from transformers import RobertaConfig, AutoTokenizer
from function.Data_preprocessing import DataPreprocessing
from function.User_file import User
from function.Phone_file import Phone
from function.UserDao_file import UserDao
from function.Comment_file import Comment
from function.CommentDao_file import CommentDao
from function.PhoneDao_file import PhoneDao
from function.Recommendation import SentimentAnalyzer, RecommendationSystem

import csv
import traceback
import pandas as pd
import torch
from PhoBert.model import RobertaForAIViVN

APP_CONFIG = {
    'TEMPLATE_FOLDER': 'templates',
    'STATIC_FOLDER': 'static',
    'SECRET_KEY': 'sentiment',
    'DATA_PATH': "F:\\Khoa-Luan\\data\\data_process\\train_processed.csv",
    'MODEL_CONFIG_PATH': "PhoBert/PhoBERT_base_transformers/config.json",
    'MODEL_WEIGHTS_PATH': "F:\Khoa-Luan\PhoBert\Weights\model_weights_Bert.pth",
    'ITEMS_PER_PAGE': 8
}

app = Flask(__name__,
    template_folder=APP_CONFIG['TEMPLATE_FOLDER'],
    static_folder=APP_CONFIG['STATIC_FOLDER']
)
app.secret_key = APP_CONFIG['SECRET_KEY']

# 2. Logic xử lý model thành class riêng
class SentimentPredictor:
    def __init__(self):
        self.dp = DataPreprocessing(APP_CONFIG['DATA_PATH'])
        self.config = RobertaConfig.from_pretrained(
            APP_CONFIG['MODEL_CONFIG_PATH'], 
            from_tf=False,
            num_labels=3,
            output_hidden_states=True
        )
        self.model = self._initialize_model()

    def _initialize_model(self):
        model = RobertaForAIViVN(self.config)
        model.load_state_dict(
            torch.load(APP_CONFIG['MODEL_WEIGHTS_PATH'], 
            map_location=torch.device('cpu'))
        )
        return model

    def predict(self, inputs):
        try:
            self.model.eval()
            with torch.no_grad():
                outputs = self.model(**inputs)
                logits = outputs if isinstance(outputs, torch.Tensor) else outputs.logits
                return torch.argmax(logits, dim=1).item()
        except Exception as e:
            print(f"Lỗi khi dự đoán sentiment: {e}")
            return None

# 3. Logic xử lý phone thành helper function
def process_phone_data(phone_data):
    try:
        return Phone(
            id=phone_data[0] or 0,
            phone_name=phone_data[1] or '',
            brand_id=phone_data[2] or '',
            product_id=phone_data[3] or 0,
            price=float(phone_data[4] or 0.0),
            ram=int(phone_data[5] or 0),
            storage=int(phone_data[6] or 0),
            front_camera=int(phone_data[7] or 0),
            rear_camera=int(phone_data[8] or 0),
            battery=int(phone_data[9] or 0),
            rating=float(phone_data[10] or 0.0),
            review_count=int(phone_data[11] or 0),
            photo_url=phone_data[12] or ''
        )
    except (TypeError, ValueError) as e:
        print(f"Error processing phone data: {e}")
        return None

# 4. Logic phân trang
def paginate_results(items, page, per_page):
    start = (page - 1) * per_page
    end = start + per_page
    total_pages = len(items) // per_page + (1 if len(items) % per_page > 0 else 0)
    return items[start:end], total_pages

@app.route('/recommendation_sentiment_analysis', methods=['GET', 'POST'])
def recommendation_sentiment_analysis():
    if 'user_id' not in session:
        return redirect(url_for('login'))
    
    userDao = UserDao()
    commentDao = CommentDao()
    phoneDao = PhoneDao()
    user = User(user_id=session['user_id'], username=session['username'])
    
    if request.method == 'POST':
        comment_input = request.form.get('comment_input')
        if comment_input:
            try:
                # Lấy thông tin phone từ session
                phone_id = session.get('phone_id')
                if not phone_id:
                    flash('Không tìm thấy thông tin điện thoại', 'error')
                    return redirect(url_for('phone'))

                # Lấy thông tin phone từ database
                phone_data = phoneDao.get_phone(phone_id)
                phone = process_phone_data(phone_data)

                # Xử lý comment và recommendations như cũ
                comment = Comment(comment=comment_input)
                commentDao.insert_comment(user, comment, phone.getId)
                comment_id = commentDao.get_comment_id_by_user()
                comment_idp = Comment(comment_id=comment_id)
                phoneDao.insert_comment_phone(phone, comment_idp)

                # Xử lý sentiment và recommend
                sentiment_predictor = SentimentPredictor()
                processed_comment = sentiment_predictor.dp.fit_transform(comment_input)
                prediction = sentiment_predictor.predict(processed_comment)
                prediction_s = sentiment_predictor.dp.Standardization(prediction)
                comment_result = Comment(comment_id=comment.getId, predict=prediction)
                commentDao.update_comment(comment_result)

                
                product_id = session.get('product_id')
                print("Retrieved from session - product_id:", product_id)
                
                if product_id:
                    phone_features = []
                    all_phones = phoneDao.get_list_phone()
                    print("Total phones fetched:", len(all_phones))
                    print("Database Product IDs:", [p[0] for p in all_phones])
                    
                    for p in all_phones:
                        try:
                            features = {
                                'Product ID': int(p[0]) if p[0] is not None else 0,
                                'phone_name': str(p[1]) if p[1] is not None else '',
                                'brand': str(p[2]) if p[2] is not None else '',
                                'Price': float(p[3]) if p[3] is not None else 0,
                                'User Rating': float(p[4]) if p[4] is not None else 0,
                                'Review Count': int(p[5]) if p[5] is not None else 0,
                                'ram': int(p[6]) if p[6] is not None else 0,
                                'storage': int(p[7]) if p[7] is not None else 0,
                                'rear_camera': int(p[8]) if p[8] is not None else 0,
                                'front_camera': int(p[9]) if p[9] is not None else 0,
                                'photo_url': str(p[10]) if p[10] is not None else url_for('static', filename='images/default-phone.jpg'),
                                'sentiment': prediction if int(p[0]) == int(product_id) else 1
                            }
                            
                            print(f"\nProcessing phone {p[1]}:")
                            print(f"Photo URL from database: {p[10]}")
                            print(f"Photo URL in features: {features['photo_url']}")
                            
                            phone_features.append(features)
                            
                        except Exception as e:
                            print(f"Error processing phone {p[0] if len(p) > 0 else 'unknown'}: {str(e)}")
                            continue
                    
                    print("Processed features for phones:", len(phone_features))
                    
                    if phone_features:
                        df = pd.DataFrame(phone_features)
                        print("DataFrame columns:", df.columns.tolist())  # Debug
                        
                        # Tạo cột Specifications
                        df['Specifications'] = df.apply(lambda row: str({
                            'RAM': f"{row['ram']}GB",
                            'Dung lượng': f"{row['storage']}GB",
                            'Camera sau': f"{row['rear_camera']}MP",
                            'Camera trước': f"{row['front_camera']}MP"
                        }), axis=1)
                        
                        try:
                            config = RobertaConfig.from_json_file("PhoBert/PhoBERT_base_transformers/config.json")
                            config.num_labels = 3
                            config.output_hidden_states = True
                            
                            model = RobertaForAIViVN(config)
                            model.load_state_dict(
                                torch.load("F:\Khoa-Luan\PhoBert\Weights\model_weights_Bert.pth", map_location=torch.device('cpu'), weights_only=True)
                            )
                            
                            # Khởi tạo tokenizer từ VINAI's PhoBERT
                            tokenizer = AutoTokenizer.from_pretrained(
                                "vinai/phobert-base",
                                use_fast=False,
                                local_files_only=False
                            )
                            
                            sentiment_analyzer = SentimentAnalyzer(model, tokenizer)
                            recommendation_system = RecommendationSystem(sentiment_analyzer)
                            
                            print("Analyzing comment:", comment.getComment)
                            recommendations, sentiment = recommendation_system.analyze_review_and_recommend(
                                review_text=comment.getComment,
                                product_id=str(product_id),
                                df=df,
                                n=5
                            )
                            
                            print("Sentiment:", sentiment)
                            if sentiment == 2:
                                print("Cảm xúc tích cực")
                            elif sentiment == 1:
                                print("Cảm xúc trung lập")
                            else:
                                print("Cảm xúc tiêu cực")
                            print("Recommendations:", recommendations)

                            statistics = commentDao.statistical()
                            with open('static/statistics.csv', 'w', newline='', encoding='utf-8') as csvfile:
                                fieldnames = ['Phone Name', 'Number of Positives', 'Number of Negatives', 'Number of Neutrals', 'Current Sentiment']
                                writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
                                writer.writeheader()
                                for row in statistics:
                                    writer.writerow({
                                        'Phone Name': row[0],
                                        'Number of Positives': row[1],
                                        'Number of Negatives': row[2],
                                        'Number of Neutrals': row[3],
                                        'Current Sentiment': "Tích cực" if sentiment == 2 else "Trung lập" if sentiment == 1 else "Tiêu cực"
                                    })
                            
                            if recommendations is not None:
                                if isinstance(recommendations, pd.DataFrame):
                                    # Kiểm tra sentiment trước khi xử lý recommendations
                                    if sentiment == 2:
                                        flash('Không có đề xuất sản phẩm do đánh giá tích cực', 'info')
                                        return render_template('recommendation_sentiment_analysis.html',
                                                            user_id=user.getUserId,
                                                            username=user.getUserName,
                                                            phone=phone,
                                                            recommendations=None,
                                                            sentiment=sentiment)
                                        
                                    # Nếu sentiment tiêu cực và trung lập, tiếp tục xử lý recommendations như bình thường
                                    for index, row in recommendations.iterrows():
                                        product_id = row['Product ID']
                                        original_phone = next(
                                            (p for p in phone_features if p['Product ID'] == product_id), 
                                            None
                                        )
                                        if original_phone and 'photo_url' in original_phone:
                                            recommendations.at[index, 'photo_url'] = original_phone['photo_url']
                                        else:
                                            phone_data = phoneDao.get_phone(product_id)
                                            if phone_data and phone_data[12]:
                                                recommendations.at[index, 'photo_url'] = phone_data[12]
                                            else:
                                                recommendations.at[index, 'photo_url'] = url_for('static', filename='images/default-phone.jpg')
                                    
                                    recommendations_dict = recommendations.to_dict('records')
                                    return render_template('recommendation_sentiment_analysis.html',
                                                        user_id=user.getUserId,
                                                        username=user.getUserName,
                                                        phone=phone,
                                                        recommendations=recommendations_dict,
                                                        sentiment=sentiment)
                                else:
                                    flash('Không tìm thấy sản phẩm phù hợp để gợi ý', 'info')
                            
                        except Exception as e:
                            print("Error in recommendation process:", str(e))
                            traceback.print_exc()
                            flash('Có lỗi xảy ra khi tạo gợi ý sản phẩm', 'error')
                    else:
                        print("No phone features were processed successfully")
                        flash('Không thể tải dữ liệu sản phẩm', 'error')
                
            except Exception as e:
                print("Error in main processing:", str(e))
                traceback.print_exc()
                flash('Có lỗi xảy ra trong quá trình xử lý', 'error')
                return render_template('recommendation_sentiment_analysis.html',
                                    user_id=user.getUserId,
                                    username=user.getUserName,
                                    phone=phone,
                                    recommendations=None,
                                    sentiment=None)
            
            return render_template('recommendation_sentiment_analysis.html',
                                user_id=user.getUserId,
                                username=user.getUserName,
                                phone=phone,
                                recommendations=None,
                                sentiment=None)
        else:
            flash('Bình luận không được để trống!', 'error')
            return render_template('recommendation_sentiment_analysis.html',
                                user_id=user.getUserId,
                                username=user.getUserName,
                                phone=phone,
                                recommendations=None,
                                sentiment=None)
    
    return render_template('recommendation_sentiment_analysis.html',
                         user_id=user.getUserId,
                         username=user.getUserName)



@app.route('/phone', methods=['GET', 'POST'])
def phone():
    # Lấy số trang từ tham số URL, mặc định là trang 1
    page = request.args.get('page', 1, type=int)
    phoneDao = PhoneDao()
    phone_list = phoneDao.get_list_phone()
    
    results = [
        process_phone_data(phone) 
        for phone in phone_list[:30] 
        if phone[0] is not None
    ]
    results = [r for r in results if r is not None]
    
    paginated_results, total_pages = paginate_results(
        results, page, APP_CONFIG['ITEMS_PER_PAGE']
    )
    
    return render_template('phone.html',
                         results=paginated_results,
                         current_page=page,
                         total_pages=total_pages)

@app.route('/phone/<int:phone_id>', methods=['GET', 'POST'])
def phone_detail(phone_id):
    try:
        phoneDao = PhoneDao()
        phone_of_db = phoneDao.get_phone(phone_id)
        
        print(f"Retrieved phone data: {phone_of_db}")  # Debug log
        
        if phone_of_db is None:
            print(f"No phone found with ID: {phone_id}")
            flash('Không tìm thấy thông tin điện thoại', 'error')
            return redirect(url_for('phone'))
            
        phone = process_phone_data(phone_of_db)
        
        # Lưu vào session
        session['phone_id'] = phone_id
        session['product_id'] = phone_id
        
        print("Saved to session - phone_id:", phone_id)
        print("Saved to session - product_id:", phone_id)
        
        if 'username' not in session or 'user_id' not in session:
            flash('Vui lòng đăng nhập để tiếp tục', 'error')
            return redirect(url_for('login'))
            
        user = User(username=session['username'], user_id=session['user_id'])
        
        return render_template('recommendation_sentiment_analysis.html',
                             user_id=user.getUserId,
                             username=user.getUserName,
                             phone=phone,
                             recommendations=None)
                             
    except Exception as e:
        print(f"Error in phone_detail: {str(e)}")
        traceback.print_exc()
        flash('Có lỗi xảy ra khi tải thông tin điện thoại', 'error')
        return redirect(url_for('phone'))

@app.route('/', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        user = User(username, password)
        userDao = UserDao()

        if userDao.check_login(user):
            user_id = userDao.get_user_id(user)
            session['username'] = username
            session['user_id'] = user_id
            if session['user_id'] == 1:
                return redirect(url_for('recommendation_sentiment_analysis.html'))
            else:
                return redirect(url_for('phone'))
        else:
            flash('Invalid username or password.', 'error')

    return render_template('login.html')


if __name__ == '__main__':
    app.run(debug=True)