import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.by import By
import time

# Khởi tạo webdriver
driver = webdriver.Chrome()

url = 'https://en.wikipedia.org/wiki/Lists_of_musicians#A'
driver.get(url)
time.sleep(2)

# Lấy ra tất cả các thẻ ul
ul_tag = driver.find_elements(By.TAG_NAME, 'ul')
# Chọn thẻ ul thứ 21
ul_musicians = ul_tag[21]

li_tags = ul_musicians.find_elements(By.TAG_NAME, 'li')

link1 = []
link2 = []

# Lấy các đường dẫn từ các thẻ li
for tag in li_tags:
    try:
        link1.append(tag.find_element(By.TAG_NAME, 'a').get_attribute('href'))
    except:
        pass

# In ra các đường dẫn
for l in link1:
    print(l)

# Lấy danh sách ban nhạc từ trang đầu tiên
driver.get(link1[0])
time.sleep(2)

# Lấy list ban nhạc
ul_tag2 = driver.find_elements(By.TAG_NAME, 'ul')
ul_bannhac = ul_tag2[24]
li_tags2 = ul_bannhac.find_elements(By.TAG_NAME, 'li')

# Lấy các đường dẫn của các ban nhạc
for tag2 in li_tags2:
    try:
        link2.append(tag2.find_element(By.TAG_NAME, 'a').get_attribute('href'))
    except:
        pass

# Danh sách để lưu dữ liệu các ban nhạc
musicians_data = []

# Lấy thông tin từng ban nhạc
for l2 in link2:
    try:
        driver.get(l2)
        time.sleep(2)

        # Trích xuất tên ban nhạc
        try:
            name = driver.find_element(By.TAG_NAME, 'h1').text
        except:
            name = ""

        # Lấy năm hoạt động 
        try:
            year_element = driver.find_element(By.XPATH, "//th[.//span[text()='Years active']]/following-sibling::td")
            year = year_element.text
        except:
            year = ""

        # Thêm thông tin vào danh sách
        musicians_data.append({'name of the band': name, 'years active': year})

    except Exception as e:
        print(f"Error processing {l2}: {e}")

# Tạo DataFrame từ danh sách dữ liệu
musicians_df = pd.DataFrame(musicians_data)

# Lưu vào file Excel
file_name = "musicians.xlsx"
musicians_df.to_excel(file_name, index=False)  # index=False để không lưu chỉ số
print('Đã lưu thành công')

# Đóng trình duyệt
driver.quit()