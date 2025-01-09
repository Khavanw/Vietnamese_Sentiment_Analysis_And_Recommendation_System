import re
import string
import pandas as pd
from vncorenlp import VnCoreNLP
from transformers import PhobertTokenizer
from sklearn.preprocessing import LabelEncoder
from tensorflow.keras.preprocessing.text import Tokenizer # type: ignore
from keras.preprocessing.sequence import pad_sequences # type: ignore

class DataPreprocessing:
    def __init__(self, path):
        self.x_train, self.y_train = self.ReadData(path)
        self.x_train = self.WordSeparation(self.x_train)
        self.x_train = self.CreateCorpus(self.x_train)
        self.labelEn = LabelEncoder()
        self.labelEn.fit(self.y_train)
        
        # Khởi tạo VnCoreNLP và tokenizer
        self.rdrsegmenter = VnCoreNLP("PhoBert/vncorenlp/VnCoreNLP-1.1.1.jar", annotators="wseg", max_heap_size='-Xmx500m')
        self.tokenizer = PhobertTokenizer.from_pretrained("vinai/phobert-base")

    def fit_transform(self, comment):
        # Phân đoạn văn bản
        word_segmented_text = self.rdrsegmenter.tokenize(comment)
        segmented_text = " ".join([" ".join(sentence) for sentence in word_segmented_text])
        
        # Mã hóa văn bản
        inputs = self.tokenizer(segmented_text, return_tensors="pt", padding=True, truncation=True, max_length=250)
        
        return inputs

    def remove_repeated_words(self, comment):
        words = comment.split()
        new_words = [words[i] for i in range(len(words)) if i == 0 or words[i] != words[i-1]]
        return ' '.join(new_words)

    def ReadData(self, path):
        df = pd.read_csv(path, encoding='utf-8')
        return df['comment'], df['label']
    
    def WordSeparation(self, comments):
        """
        Tách từ trong các bình luận
        
        Args:
            comments: Series hoặc list các bình luận
            
        Returns:
            List các bình luận đã được tách từ
        """
        processed_comments = []
        for review in comments:
            if isinstance(review, float):
                processed_comments.append([])
            else:
                review_str = str(review)
                processed_comments.append(review_str.split())
        
        return processed_comments

    def Padding(self, comments, sequence_length):
        tokenizer = Tokenizer(oov_token='<oov>')
        tokenizer.fit_on_texts(comments)
        sequences = tokenizer.texts_to_sequences(comments)
        padded_sequences = pad_sequences(sequences, maxlen=sequence_length, padding='pre')
        return padded_sequences

    def CreateCorpus(self, comments):
        tokenizer = Tokenizer(oov_token='<oov>')
        tokenizer.fit_on_texts(comments)
        return tokenizer

    def Standardization(self, prediction):
        """
        Chuyển đổi nhãn dự đoán thành mô tả cảm xúc.
        
        Args:
            prediction (int): Nhãn dự đoán của mô hình (0, 1, hoặc 2).

        Returns:
            str: Mô tả cảm xúc tương ứng với nhãn dự đoán.
        """
        if prediction == 0:
            return "Đây là một bình luận mang ý nghĩa tiêu cực"
        elif prediction == 1:
            return "Đây là một bình luận mang ý nghĩa trung lập"
        else:
            return "Đây là một bình luận mang ý nghĩa tích cực"


    def remove_punctuation(self, comment):
        # Tạo bảng chuyển đổi
        translator = str.maketrans('', '', string.punctuation)
        # Loại bỏ dấu câu
        new_string = comment.translate(translator)
        # Loại bỏ khoảng trắng dư thừa và ký hiệu ngắt dòng
        new_string = re.sub('[\n ]+', ' ', new_string)
        # Loại bỏ emoji
        emoji_pattern = re.compile("["
                u"\U0001F600-\U0001F64F"  # emoticons
                u"\U0001F300-\U0001F5FF"  # symbols & pictographs
                u"\U0001F680-\U0001F6FF"  # transport & map symbols
                u"\U0001F1E0-\U0001F1FF"  # flags (iOS)
                u"\U00002500-\U00002BEF"  # chinese char
                u"\U00002702-\U000027B0"
                u"\U000024C2-\U0001F251"
                u"\U0001f926-\U0001f937"
                u"\U00010000-\U0010ffff"
                u"\u2640-\u2642"
                u"\u2600-\u2B55"
                u"\u200d"
                u"\u23cf"
                u"\u23e9"
                u"\u231a"
                u"\ufe0f"  # dingbats
                u"\u3030"
                "]+", flags=re.UNICODE)
        new_string = re.sub(emoji_pattern, '', new_string)
        return new_string

    def read_filestopwords(self):
        with open('data/data_stopwords/vietnamese_stopwords.txt', 'r', encoding='utf-8') as file:
            stop_words = file.read().splitlines()
        return stop_words

    def remove_stopword(self, comment):
        stop_words = self.read_filestopwords()
        filtered_words = [word for word in comment.split() if word not in stop_words]
        return ' '.join(filtered_words)
