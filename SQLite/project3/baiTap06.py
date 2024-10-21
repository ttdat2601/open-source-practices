from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
import re
import time
import sqlite3

# 0. Tạo cơ sở dữ liệu
conn = sqlite3.connect('painters.db')
c = conn.cursor()
try:
    c.execute('''
        CREATE TABLE IF NOT EXISTS painter (
            id integer primary key autoincrement,
            name text,
            birth text,
            death text,
            nationality text
        )
    ''')
except Exception as e:
    print(e)

def them(name, birth, death, nationality):
    conn = sqlite3.connect('painters.db')
    c = conn.cursor()
    # Thêm vào cơ sở dữ liệu
    c.execute('''
        INSERT INTO painter(name, birth, death, nationality)
        VALUES (:name, :birth, :death, :nationality)
    ''', {
        'name': name,
        'birth': birth,
        'death': death,
        'nationality': nationality,
    })
    conn.commit()
    conn.close()

# I. Tải nơi chứa các liên kết và tạo danh sách rỗng để lưu trữ các liên kết
all_links = []

# II. Lấy tất cả các đường dẫn đến trang của painters
# Đường dẫn đến file thực thi ChromeDriver
chrome_path = r"/Users/ttdat/Downloads/chromedriver-mac-arm64/chromedriver"
ser = Service(chrome_path)

# Tạo tùy chọn
options = webdriver.ChromeOptions()
options.headless = False  # Chạy với giao diện, có thể bật headless=True để chạy ẩn

# Khởi tạo driver Chrome (chỉ mở một lần)
driver = webdriver.Chrome(service=ser, options=options)

for i in range(70, 71):  # Thay đổi số lượng ký tự bắt đầu nếu cần
    url = "https://en.wikipedia.org/wiki/List_of_painters_by_name_beginning_with_%22"+chr(i)+"%22"
    try:
        driver.get(url)
        time.sleep(3)

        # Lấy ra tất cả các thẻ ul
        ul_tags = driver.find_elements(By.TAG_NAME, "ul")
        print(len(ul_tags))

        # Chọn thẻ ul thứ 21 (nơi chứa các liên kết painters)
        ul_painters = ul_tags[20]  # List bắt đầu với chỉ mục 0

        # Lấy tất cả các thẻ li thuộc ul_painters
        li_tags = ul_painters.find_elements(By.TAG_NAME, "li")

        # Tạo danh sách các URL
        links = [tag.find_element(By.TAG_NAME, "a").get_attribute("href") for tag in li_tags]
        all_links.extend(links)  # Thêm tất cả các liên kết vào danh sách all_links

    except Exception as e:
        print(f"Error while processing list of painters starting with {chr(i)}: {e}")

######################################################
# III. Lấy thông tin từ từng trang painters
count = 0
for link in all_links:
    if count > 3:
        break
    count += 1

    print(f"Processing link: {link}")
    try:
        # Truy cập vào từng trang painters
        driver.get(link)
        time.sleep(2)

        # Lấy tên painter
        name = driver.find_element(By.TAG_NAME, "h1").text

        # Lấy ngày sinh
        try:
            birth_element = driver.find_element(By.XPATH, "//th[text()='Born']/following-sibling::td")
            birth = birth_element.text
            birth = re.findall(r'[0-9]{1,2}+\s+[A-Za-z]+\s+[0-9]{4}', birth)[0]  # regex
        except Exception:
            birth = ""

        # Lấy ngày mất
        try:
            death_element = driver.find_element(By.XPATH, "//th[text()='Died']/following-sibling::td")
            death = death_element.text
            death = re.findall(r'[0-9]{1,2}+\s+[A-Za-z]+\s+[0-9]{4}', death)[0]
        except Exception:
            death = ""

        # Lấy quốc tịch
        try:
            nationality_element = driver.find_element(By.XPATH, "//th[text()='Nationality']/following-sibling::td")
            nationality = nationality_element.text
        except Exception:
            nationality = ""

        # Lưu thông tin vào cơ sở dữ liệu
        them(name, birth, death, nationality)

    except Exception as e:
        print(f"Error processing {link}: {e}")

# Đóng driver khi hoàn thành công việc
driver.quit()
