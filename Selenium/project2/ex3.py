from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

# Đường dẫn đến file thực thi chromedriver
chrome_path = r"/Users/ttdat/Downloads/chromedriver-mac-arm64/chromedriver"  # Thay thế bằng đường dẫn đến ChromeDriver của bạn

# Khởi tạo đối tượng dịch vụ với đường dẫn đến ChromeDriver
ser = Service(chrome_path)

# Tạo tùy chọn cho Chrome
options = webdriver.ChromeOptions()
options.headless = False  # Để hiển thị giao diện

# Khởi tạo driver
driver = webdriver.Chrome(service=ser, options=options)

# Tạo url
url = 'http://pythonscraping.com/pages/files/form.html'

# Truy cập trang web
driver.get(url)

# Đợi trường firstname xuất hiện và điền thông tin vào form
try:
    firstname_input = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.XPATH, "//input[@name='firstname']"))
    )
    firstname_input.send_keys('Tuan Dat')

    # Điền thông tin vào trường lastname
    lastname_input = driver.find_element(By.XPATH, "//input[@name='lastname']")
    lastname_input.send_keys("Tran")

    # Tìm nút submit và click để gửi form
    submit_button = driver.find_element(By.XPATH, "//input[@type='submit']")
    submit_button.click()

    # Đợi vài giây để quan sát kết quả sau khi gửi form
    time.sleep(5)

finally:
    # Đóng trình duyệt
    driver.quit()
