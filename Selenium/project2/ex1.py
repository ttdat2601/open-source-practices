from selenium import webdriver
from selenium.webdriver.chrome.service import Service
import time

# Đường dẫn đến file thực thi chromedriver
chrome_path = r"/Users/ttdat/Downloads/chromedriver-mac-arm64/chromedriver"  # Thay thế đường dẫn bằng vị trí của chromedriver

# Khởi tởi đối tượng dịch vụ với đường dẫn đến chromedriver
ser = Service(chrome_path)

# Tạo tùy chọn cho Chrome
options = webdriver.ChromeOptions()
# Thiết lập chrome để hiện thị giao diện (headless = False)
options.headless = False  # Nếu bạn muốn chạy không hiện giao diện, đổi thành True

# Khởi tạo driver
driver = webdriver.Chrome(service=ser, options=options)

# Tạo url
url = 'http://pythonscraping.com/pages/javascript/ajaxDemo.html'

# Truy cập trang web
driver.get(url)

# In ra nội dung của trang web trước khi đợi AJAX tải
print("Before: ================================\n")
print(driver.page_source)

# Tạm dừng khoảng 3 giây để chờ AJAX tải dữ liệu
time.sleep(3)

# In lại nội dung của trang sau khi AJAX đã tải
print("\n\n\n\nAfter: ================================\n")
print(driver.page_source)

# Đóng trình duyệt
driver.quit()
