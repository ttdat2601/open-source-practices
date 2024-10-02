from selenium import webdriver
from selenium.webdriver.common.by import By
import pandas as pd
import time

# Khởi tạo trình duyệt Chrome
driver = webdriver.Chrome()

# Mở trang web chứa danh sách các nhạc sĩ
url = 'https://en.wikipedia.org/wiki/Lists_of_musicians'
driver.get(url)

# Tìm tất cả các liên kết có văn bản bắt đầu bằng "A"
links = driver.find_elements(By.TAG_NAME, 'A')

# Lọc các liên kết bắt đầu bằng "List of" và lưu vào danh sách
list_of_links = []
for link in links:
    text = link.text.strip()
    href = link.get_attribute('href')
    if text.startswith("List of") and href is not None:
        list_of_links.append({'Title': text, 'Link': href})
        print(f"Link: {href}")

# Chuyển đổi danh sách các liên kết "List of" thành DataFrame
df_links = pd.DataFrame(list_of_links)

# Kiểm tra nếu có liên kết "List of" và truy cập vào liên kết đầu tiên trong danh sách
musician_data = []
if not df_links.empty:
    first_list_link = df_links.iloc[0]['Link']
    print(f"Điều hướng đến trang danh sách: {first_list_link}")
    driver.get(first_list_link)
    time.sleep(2)  # Đợi trang tải

    # Tìm các liên kết đến các nghệ sĩ bắt đầu bằng chữ "A"
    artist_links_in_A = []
    links_on_list_page = driver.find_elements(By.TAG_NAME, 'a')
    for link in links_on_list_page:
        text = link.text.strip()
        href = link.get_attribute('href')
        # Chỉ lấy liên kết của nghệ sĩ, không phải anchor trên cùng một trang
        if text.startswith("A") and href is not None and 'redlink' not in href and not href.startswith('#'):
            artist_links_in_A.append(href)

    # Truy cập vào trang chi tiết của nghệ sĩ đầu tiên trong phần "A"
    if artist_links_in_A:
        first_artist_link = artist_links_in_A[0]
        print(f"Dẫn đến trang nghệ sĩ: {first_artist_link}")
        driver.get(first_artist_link)
        time.sleep(2)  # Đợi trang tải

        # Kiểm tra nếu trang có 'infobox'
        try:
            infobox = driver.find_elements(By.CLASS_NAME, 'infobox')

            if infobox:
                # Tìm các hàng trong bảng infobox
                rows = infobox[0].find_elements(By.TAG_NAME, 'tr')

                # Khởi tạo biến để lưu dữ liệu
                band_name = None
                years_active = None

                # Duyệt qua các hàng để tìm thông tin
                for row in rows:
                    header = row.find_elements(By.TAG_NAME, 'th')
                    data = row.find_elements(By.TAG_NAME, 'td')

                    if header and data:
                        header_text = header[0].text
                        data_text = data[0].text

                        if 'Associated acts' in header_text or 'Band' in header_text:
                            band_name = data_text

                        if 'Years active' in header_text:
                            years_active = data_text

                # In thông tin kiểm tra và thêm vào danh sách nếu tìm thấy
                print(f"Band Name: {band_name}")
                print(f"Years Active: {years_active}")

                if band_name or years_active:
                    musician_data.append({'Band Name': band_name, 'Years Active': years_active})
            else:
                print("No infobox found on the artist page.")

        except Exception as e:
            print(f"Error extracting information: {e}")
    else:
        print("No valid artist link found starting with 'A'.")
else:
    print("No valid list link found.")

# Đóng trình duyệt sau khi thực hiện
driver.quit()

# Lưu danh sách các liên kết "List of" ra file Excel
with pd.ExcelWriter("musicians.xlsx") as writer:
    # Lưu các liên kết "List of" vào sheet đầu tiên
    df_links.to_excel(writer, sheet_name='List of Links', index=False)

    # Kiểm tra và xuất dữ liệu nghệ sĩ ra sheet thứ hai nếu có
    if musician_data:
        df_musicians = pd.DataFrame(musician_data)
        df_musicians.to_excel(writer, sheet_name='Musician Data', index=False)
        print("Musician data has been written to musicians.xlsx")
    else:
        print("No musician data was collected.")
