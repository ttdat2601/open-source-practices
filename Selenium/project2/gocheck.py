from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
import time
import pandas as pd

# Đường dẫn đến ChromeDriver
chrome_path = r"/Users/ttdat/Downloads/chromedriver-mac-arm64/chromedriver"  # Thay thế đường dẫn bằng vị trí của ChromeDriver

# Khởi tạo đối tượng dịch vụ với đường dẫn đến ChromeDriver
ser = Service(chrome_path)

# Tạo tùy chọn cho Chrome
options = webdriver.ChromeOptions()
options.headless = False  # Để chạy với giao diện

# Khởi tạo driver
driver = webdriver.Chrome(service=ser, options=options)

# Truy cập trang web GoChek
url = 'https://gochek.vn/collections/all'
driver.get(url)

# Tạm dừng để đảm bảo trang tải xong
time.sleep(3)

# Tạo danh sách để lưu thông tin sản phẩm
ten_san_pham = []
gia_san_pham = []
hinh_anh_san_pham = []

# Nhấn "Xem thêm" để tải thêm sản phẩm (nếu có nút này)
while True:
    try:
        # Tìm và nhấn nút "Xem thêm" để tải thêm sản phẩm
        xem_them = driver.find_element(By.XPATH, "//button[text()='Xem thêm']")
        xem_them.click()
        time.sleep(3)  # Đợi trang tải thêm sản phẩm
    except:
        print("Không tìm thấy hoặc đã tải hết sản phẩm.")
        break

# Tìm các sản phẩm trên trang
san_pham_elements = driver.find_elements(By.CLASS_NAME, 'product-grid-item')

# Lấy thông tin từng sản phẩm
for sp in san_pham_elements:
    try:
        # Lấy tên sản phẩm
        ten = sp.find_element(By.CLASS_NAME, 'product-title').text
        ten_san_pham.append(ten)

        # Lấy giá sản phẩm
        gia = sp.find_element(By.CLASS_NAME, 'price').text
        gia_san_pham.append(gia)

        # Lấy hình ảnh sản phẩm
        hinh_anh = sp.find_element(By.TAG_NAME, 'img').get_attribute('src')
        hinh_anh_san_pham.append(hinh_anh)
    except Exception as e:
        print(f"Lỗi khi thu thập thông tin sản phẩm: {e}")

# Đóng trình duyệt
driver.quit()

# Tạo DataFrame từ dữ liệu đã thu thập
df = pd.DataFrame({
    'Tên sản phẩm': ten_san_pham,
    'Giá sản phẩm': gia_san_pham,
    'Hình ảnh sản phẩm': hinh_anh_san_pham
})

# Lưu vào file Excel
df.to_excel('san_pham_gochek.xlsx', index=False)

print("Thu thập dữ liệu hoàn tất và lưu vào file Excel.")
