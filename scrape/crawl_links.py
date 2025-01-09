from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import pandas as pd
import time

class PhoneCrawler:
    def __init__(self):
        self.driver = webdriver.Chrome()
        self.wait = WebDriverWait(self.driver, 10)
        
    def crawl_phone_data(self, url, brand_xpaths):
        """Crawl dữ liệu điện thoại từ trang web"""
        self.driver.get(url)
        all_phones_data = []
        
        for brand, xpath in brand_xpaths.items():
            try:
                # Click vào nút "Lọc"
                filter_button = self.wait.until(
                    EC.element_to_be_clickable((By.CSS_SELECTOR, "div.filter-item__title.jsTitle"))
                )
                filter_button.click()
                print(f"Đang crawl thương hiệu {brand}...")
                time.sleep(2)

                # Click vào thương hiệu
                brand_element = self.wait.until(
                    EC.element_to_be_clickable((By.XPATH, xpath))
                )
                brand_element.click()
                time.sleep(2)

                # Click nút "Xem kết quả"
                view_results_button = self.wait.until(
                    EC.element_to_be_clickable((By.XPATH, "/html/body/div[7]/section[4]/div[2]/div/div[1]/section/div/div[1]/div[1]/div[2]/div[2]/div[16]/a[2]"))
                )
                view_results_button.click()
                print("Đã click nút Xem kết quả")
                time.sleep(3)

                # Click nút "Xem thêm" cho đến khi không còn
                while True:
                    try:
                        self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
                        time.sleep(1)
                        see_more_button = self.wait.until(
                            EC.element_to_be_clickable((By.CSS_SELECTOR, "a strong.see-more-btn"))
                        )
                        self.driver.execute_script("arguments[0].click();", see_more_button)
                        print("Đã click nút Xem thêm")
                        time.sleep(2)
                    except Exception:
                        print("Đã load hết sản phẩm")
                        break

                # Crawl dữ liệu sản phẩm
                products = self.driver.find_elements(By.CSS_SELECTOR, "ul.listproduct > li.item")
                
                for product in products:
                    try:
                        phone_data = {
                            'Product Link': product.find_element(By.CSS_SELECTOR, "a.main-contain").get_attribute('href'),
                            'Product Name': product.find_element(By.CSS_SELECTOR, "h3").text,
                            'Price': product.find_element(By.CSS_SELECTOR, "strong.price").text
                        }
                        all_phones_data.append(phone_data)
                        print(f"Đã lấy dữ liệu: {phone_data['Product Name']}")
                        
                    except Exception as e:
                        print(f"Lỗi khi lấy thông tin sản phẩm: {e}")
                        continue

                # Sau khi crawl xong một thương hiệu, quay về trang chủ
                print(f"Đã crawl xong thương hiệu {brand}")
                self.driver.get(url)
                time.sleep(2)

            except Exception as e:
                print(f"Lỗi khi xử lý thương hiệu {brand}: {e}")
                self.driver.get(url)
                time.sleep(2)
                continue

        return all_phones_data

    def save_to_csv(self, data, filename):
        """Lưu dữ liệu vào file CSV"""
        df = pd.DataFrame(data)
        df.to_csv(filename, index=False, encoding='utf-8')
        print(f"Đã lưu dữ liệu vào {filename}")
        
    def close(self):
        """Đóng trình duyệt"""
        self.driver.quit()

def main():
    brand_xpaths = {
        "Samsung": '/html/body/div[7]/section[4]/div[2]/div/div[1]/section/div/div[1]/div[1]/div[2]/div[2]/div[2]/div/a[1]',
        "iPhone": '/html/body/div[7]/section[4]/div[2]/div/div[1]/section/div/div[1]/div[1]/div[2]/div[2]/div[2]/div/a[2]',
        "Oppo": '/html/body/div[7]/section[4]/div[2]/div/div[1]/section/div/div[1]/div[1]/div[2]/div[2]/div[2]/div/a[3]',
        "Xiaomi": '/html/body/div[7]/section[4]/div[2]/div/div[1]/section/div/div[1]/div[1]/div[2]/div[2]/div[2]/div/a[4]',
        "Vivo": '/html/body/div[7]/section[4]/div[2]/div/div[1]/section/div/div/div[1]/div[2]/div[2]/div[2]/div/a[5]',
        "Realme": '/html/body/div[7]/section[4]/div[2]/div/div[1]/section/div/div/div[1]/div[2]/div[2]/div[2]/div/a[6]',
        "Honor": '/html/body/div[7]/section[4]/div[2]/div/div[1]/section/div/div/div[1]/div[2]/div[2]/div[2]/div/a[7]',
        "TCL": '/html/body/div[7]/section[4]/div[2]/div/div[1]/section/div/div/div[1]/div[2]/div[2]/div[2]/div/a[8]',
        "Tecno": '/html/body/div[7]/section[4]/div[2]/div/div[1]/section/div/div/div[1]/div[2]/div[2]/div[2]/div/a[9]',
        "Nokia": '/html/body/div[7]/section[4]/div[2]/div/div[1]/section/div/div/div[1]/div[2]/div[2]/div[2]/div/a[10]',
        "Masstel": '/html/body/div[7]/section[4]/div[2]/div/div[1]/section/div/div/div[1]/div[2]/div[2]/div[2]/div/a[11]',
        "Mobell": '/html/body/div[7]/section[4]/div[2]/div/div[1]/section/div/div/div[1]/div[2]/div[2]/div[2]/div/a[12]',
        "Itel": '/html/body/div[7]/section[4]/div[2]/div/div[1]/section/div/div/div[1]/div[2]/div[2]/div[2]/div/a[13]',
        "Viettel": '/html/body/div[7]/section[4]/div[2]/div/div[1]/section/div/div/div[1]/div[2]/div[2]/div[2]/div/a[14]',
        "Benco": '/html/body/div[7]/section[4]/div[2]/div/div[1]/section/div/div/div[1]/div[2]/div[2]/div[2]/div/a[15]'
    }

    crawler = PhoneCrawler()
    try:
        url = "https://www.thegioididong.com/dtdd"
        phone_data = crawler.crawl_phone_data(url, brand_xpaths)
        crawler.save_to_csv(phone_data, 'phone_data.csv')
    finally:
        crawler.close()

if __name__ == "__main__":
    main()