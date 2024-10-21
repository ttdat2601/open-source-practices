from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
import re
import time
import sqlite3

######################################################
# 0. Tạo cơ sở dữ liệu
conn = sqlite3.connect('stock.db')
c = conn.cursor()
try:
    c.execute('''
        CREATE TABLE stock (
            id integer primary key autoincrement,
            _date text,
            open_price REAL,
            highest_price REAL,
            lowest_price REAL,
            closing_price REAL,
            changed_price REAL,
            price_change_percentage REAL,
            changed_volume integer
        )
    ''')
except Exception as e:
    print(e)

def insert_data(_date, open_price, highest_price, lowest_price, closing_price, changed_price, price_change_percentage, changed_volume):
    conn = sqlite3.connect('stock.db')
    c = conn.cursor()
    # Thêm vào cơ sở dữ liệu
    c.execute('''
        INSERT INTO stock(_date, open_price, highest_price, lowest_price, closing_price, changed_price, price_change_percentage, changed_volume)
        VALUES (:_date, :open_price, :highest_price, :lowest_price, :closing_price, :changed_price, :price_change_percentage, :changed_volume)
    ''',
      {
          '_date': _date,
          'open_price': open_price,
          'highest_price': highest_price,
          'lowest_price': lowest_price,
          'closing_price': closing_price,
          'changed_price': changed_price,
          'price_change_percentage': price_change_percentage,
          'changed_volume': changed_volume,
      })
    conn.commit()
    conn.close()

######################################################
# 1. Thu thập dữ liệu từ trang web
# Khởi tạo Webdriver

# Đường dẫn đến file thực thi ChromeDriver (hoặc geckodriver nếu bạn sử dụng Firefox)
chrome_path = r"/Users/ttdat/Downloads/chromedriver-mac-arm64/chromedriver"

# Khởi tởi đối tượng dịch vụ với đường dẫn đến ChromeDriver
ser = Service(chrome_path)

# Tạo tùy chọn cho trình duyệt Chrome
options = webdriver.ChromeOptions()
options.headless = False  # Nếu bạn muốn chạy ẩn, có thể đặt thành True

# Khởi tạo driver
driver = webdriver.Chrome(options=options, service=ser)

# Truy cập trang web cần lấy dữ liệu
driver.get("https://simplize.vn/co-phieu/SAB/lich-su-gia")
time.sleep(5)

# Lấy toàn bộ hàng trong bảng
rows = driver.find_elements(By.CSS_SELECTOR, ".simplize-table-row.simplize-table-row-level-0")
print(f"Tìm thấy {len(rows)} hàng dữ liệu.")
for row in rows:
    columns = row.find_elements(By.TAG_NAME, "td")
    
    # Lấy dữ liệu từng cột
    _date = columns[0].text
    
    # Xóa dấu phẩy và chuyển đổi sang số thực
    open_price = float(columns[1].text.replace(",", ""))
    highest_price = float(columns[2].text.replace(",", ""))
    lowest_price = float(columns[3].text.replace(",", ""))
    closing_price = float(columns[4].text.replace(",", ""))
    
    # Kiểm tra nếu có dấu "-" thì thay bằng 0, nếu không chuyển đổi thành số thực
    changed_price = float(columns[5].text.replace(",", "")) if columns[5].text != '-' else 0

    # Xử lý phần trăm thay đổi, loại bỏ dấu "%" và chuyển đổi thành số thực
    price_change_percentage = columns[6].text.replace(",", "").replace("%", "")
    price_change_percentage = float(price_change_percentage) if price_change_percentage != '-' else 0
    
    # Khối lượng thay đổi
    changed_volume = int(columns[7].text.replace(",", ""))
    
    # Chèn dữ liệu vào cơ sở dữ liệu
    insert_data(_date, open_price, highest_price, lowest_price, closing_price, changed_price, price_change_percentage, changed_volume)

# Đóng trình duyệt
driver.quit()
