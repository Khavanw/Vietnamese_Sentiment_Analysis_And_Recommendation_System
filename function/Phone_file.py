class Phone:
    def __init__(self, id=None, phone_name=None, brand_id=None, product_id=None, price=None, ram=None, storage=None, front_camera=None, rear_camera=None, battery=None, rating=None, review_count=None, photo_url=None):
        self._id = id
        self._phone_name = phone_name
        self._brand_id = brand_id
        self._product_id = product_id
        self._price = price
        self._ram = ram
        self._storage = storage
        self._front_camera = front_camera
        self._rear_camera = rear_camera
        self._battery = battery
        self._rating = rating
        self._review_count = review_count
        self._photo_url = photo_url

    @property
    def getId(self):
        return self._id

    @property
    def getPhoneName(self):
        return self._phone_name

    @property
    def getBrandId(self):
        return self._brand_id
    
    @property
    def getProductId(self):
        return self._product_id
    
    @property
    def getPrice(self):
        return self._price  
    
    @property
    def getRam(self):
        return self._ram
    
    @property
    def getStorage(self):
        return self._storage
    
    @property
    def getFrontCamera(self):
        return self._front_camera
    
    @property
    def getRearCamera(self):
        return self._rear_camera    
    
    @property
    def getBattery(self):
        return self._battery
    
    @property
    def getRating(self):
        return self._rating
    
    @property
    def getReviewCount(self):
        return self._review_count
    
    @property
    def getPhotoUrl(self):
        return self._photo_url
    
    @property
    def getSpecifications(self):
        """Trả về dictionary chứa thông số kỹ thuật của điện thoại"""
        def format_price(price):
            if price:
                # Chuyển số thành chuỗi và loại bỏ phần thập phân
                price_str = str(int(price))
                # Format số với dấu chấm phân cách hàng nghìn
                formatted_price = '{:,}'.format(int(price_str)).replace(',', '.')
                return f"{formatted_price} VNĐ"
            return "N/A"

        return {
            "Giá": format_price(self._price),
            "RAM": f"{self._ram}GB" if self._ram else "N/A",
            "Bộ nhớ trong": f"{self._storage}GB" if self._storage else "N/A",
            "Camera trước": f"{self._front_camera}MP" if self._front_camera else "N/A",
            "Camera sau": f"{self._rear_camera}MP" if self._rear_camera else "N/A",
            "Pin": f"{self._battery}mAh" if self._battery else "N/A",
            "Đánh giá": f"{self._rating} ({self._review_count} đánh giá)" if self._rating else "Chưa có đánh giá"
        }
        
