import time
import csv
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup

def scrape_product_details(product_link):
    driver.get(product_link)  
    driver.refresh()
    
    soup = BeautifulSoup(driver.page_source, 'html.parser')

    try:
        image_container = soup.select_one("div.owl-stage-outer div.owl-lazy div.item-img")
        
        if image_container and image_container.has_attr("src"):
            image_url = image_container["src"]
        elif image_container and image_container.has_attr("data-thumb"):
            image_url = image_container["data-thumb"]
        else:
            image_url = "N/A"
        
        print(f'Image URL: {image_url}')
    except Exception as e:
        print(f"Error finding the Image URL: {e}")
        image_url = "N/A"



    try:
        # Tìm tên sản phẩm trong thẻ h1 trong div.product-name
        product_name = soup.select_one("div.product-name h1").get_text(strip=True)
        print(f'Product Name: {product_name}')
    except Exception as e:
        print("Could not find the product name.")
        product_name = "N/A"

    try:
        price = soup.select_one("div.bs_price strong").get_text(strip=True)
        print(f'Product Price: {price}')
    except Exception as e:
        try:
            price = soup.select_one("div.box-price p.box-price-present").get_text(strip=True)
            print(f'Product Price: {price}')
        except Exception as e:
            print("Could not find the product price in either location.")
            price = "N/A"
    
    try:
        average_score = soup.select_one("div.point .point-average-score").get_text(strip=True)
        print(f'Average Score: {average_score}')
    except Exception as e:
        print("Could not find the point average score.")
        average_score = "N/A"

    try:
        review_count = soup.select_one("div.point .point-alltimerate").get_text(strip=True)
        print(f'Review Count: {review_count}')
    except Exception as e:
        print("Could not find the point average score.")
        review_count = "N/A"

    # Click the 'All Reviews' section
    def try_click_reviews_button(driver):
        review_button_xpaths = [
            "/html/body/section/div[2]/div[1]/div[10]/div[2]/div/div/div[6]/div/a",
            "/html/body/section/div[2]/div[1]/div[9]/div[2]/div/div/div[6]/div/a",
            "/html/body/section/div[2]/div[1]/div[12]/div[2]/div/div/div[6]/div/a",
            "/html/body/section/div[2]/div[1]/div[8]/div[2]/div/div/div[6]/div/a",
            "/html/body/section/div[2]/div[1]/div[12]/div[2]/div/div/div[6]/div/a",
            "/html/body/section/div[2]/div[1]/div[14]/div[2]/div/div/div[6]/div/a",
            "/html/body/section/div[2]/div[1]/div[11]/div[2]/div/div/div[6]/div/a",
        ]
        
        for xpath in review_button_xpaths:
            try:
                button = WebDriverWait(driver, 5).until(
                    EC.element_to_be_clickable((By.XPATH, xpath))
                )
                button.click()
                print(f"Đã click thành công nút Reviews với XPath: {xpath}")
                return True
            except Exception as e:
                continue
        
        print("Không tìm thấy nút Reviews nào có thể click")
        return False

    if not try_click_reviews_button(driver):
        print("Không thể tìm thấy phần đánh giá cho sản phẩm này")
        return []

    time.sleep(5)

    review_data = []

    page_count = 0
    max_pages = 100

    while page_count < max_pages:
        time.sleep(5)

        soup = BeautifulSoup(driver.page_source, 'html.parser')
        review_items = soup.select("li[id^='r-']")

        if not review_items:
            print("Không tìm thấy đánh giá nào. Đang thoát...")
            break

        for review_item in review_items:
            try:
                user_id = review_item.get('id', 'Unknown ID')
                
                # Lấy số sao đánh giá
                star_elements = review_item.select(".cmt-top-star i.iconcmt-starbuy")
                rating = len(star_elements)
                
                # Lấy nội dung đánh giá
                review_element = review_item.select_one(".cmt-txt")
                review = review_element.text.strip() if review_element else "Không có nội dung đánh giá"


                print(f'User ID: {user_id}, Rating: {rating}, Review: {review}')
                review_data.append([image_url, product_link, product_name, price, user_id, average_score ,rating, review, review_count])

            except Exception as e:
                print(f"Lỗi khi xử lý đánh giá: {e}")
                continue

        try:
            pagination = soup.select_one("div.pagcomment")
            if not pagination:
                print("Không tìm thấy phân trang")
                break

            active_page = pagination.select_one("span.active")
            if not active_page:
                print("Không tìm thấy trang hiện tại.")
                break

            current_page = int(active_page.text)
            print(f"Đang ở trang {current_page}")

            next_page = current_page + 1
            next_page_link = pagination.find('a', title=f'trang {next_page}')

            if not next_page_link:
                print("Đã đến trang cuối cùng")
                break

            driver.execute_script(f"ratingCmtList({next_page})")
            print(f"Đang chuyển đến trang {next_page}")

            time.sleep(3)

            new_soup = BeautifulSoup(driver.page_source, 'html.parser')
            new_active_page = new_soup.select_one("div.pagcomment span.active")
            if not new_active_page or int(new_active_page.text) != next_page:
                print("Chuyển trang không thành công")
                break

            page_count += 1
            print(f"Đã chuyển sang trang {next_page} thành công")

        except Exception as e:
            print(f"Lỗi khi chuyển trang: {str(e)}")
            try:
                driver.refresh()
                time.sleep(5)
            except:
                break

    return review_data


driver = webdriver.Chrome()

input_csv_file_path = "data/data_orginal/Cleaned_Phone_Links.csv"
product_links = []

with open(input_csv_file_path, mode='r', encoding='utf-8') as file:
    reader = csv.DictReader(file)
    for row in reader:
        product_links.append(row['Product Link'])

output_csv_file_path = "data/data_orginal/Mobile_Phone_Data.csv"
with open(output_csv_file_path, mode='w', newline='', encoding='utf-8') as file:
    writer = csv.writer(file)
    writer.writerow(["Product Image URL", "Product Link", "Product Name", "product Price", "User ID","Average Score", "User Rating", "Review", "Review Count"])

total_links = len(product_links)
for index, link in enumerate(product_links, start=1):
    print(f"Processing link {index} of {total_links}: {link}")
    review_data = scrape_product_details(link)
    if review_data:
        with open(output_csv_file_path, mode='a', newline='', encoding='utf-8') as file:
            writer = csv.writer(file)
            writer.writerows(review_data)
    
    driver.get("about:blank")

driver.quit()
