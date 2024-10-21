from tkinter import *
from tkinter import messagebox
from tkinter import ttk
import sqlite3

root = Tk()
root.title("Hệ thống quản lý địa chỉ")
root.geometry("600x600")

# Kết nối tới database và tạo bảng nếu chưa tồn tại
conn = sqlite3.connect('address_book.db')
c = conn.cursor()

# Tạo bảng addresses nếu chưa tồn tại
c.execute('''
     CREATE TABLE IF NOT EXISTS addresses(
         id INTEGER PRIMARY KEY AUTOINCREMENT,
         first_name TEXT,
         last_name TEXT,
         address TEXT,
         city TEXT,
         state TEXT,
         zipcode INTEGER
     )
''')
conn.commit()
conn.close()

# Chức năng thêm bản ghi
def them():
    conn = sqlite3.connect('address_book.db')
    c = conn.cursor()

    # Thêm dữ liệu
    c.execute('''
        INSERT INTO 
        addresses (first_name, last_name, address, city, state, zipcode)
        VALUES 
        (:first_name, :last_name, :address, :city, :state, :zipcode)
    ''', {
        'first_name': f_name.get(),
        'last_name': l_name.get(),
        'address': address.get(),
        'city': city.get(),
        'state': state.get(),
        'zipcode': zipcode.get(),
    })

    conn.commit()
    conn.close()

    # Xóa nội dung trong các ô nhập liệu
    f_name.delete(0, END)
    l_name.delete(0, END)
    address.delete(0, END)
    city.delete(0, END)
    state.delete(0, END)
    zipcode.delete(0, END)

    # Hiển thị lại dữ liệu sau khi thêm mới
    truy_van()

# Chức năng xóa bản ghi
def xoa():
    conn = sqlite3.connect('address_book.db')
    c = conn.cursor()
    c.execute("DELETE FROM addresses WHERE id=:id", {'id': delete_box.get()})
    delete_box.delete(0, END)
    conn.commit()
    conn.close()

    # Hiển thị lại dữ liệu sau khi xóa
    truy_van()

# Chức năng truy vấn và hiển thị dữ liệu trong Treeview
def truy_van():
    # Xóa các dữ liệu hiện tại trong TreeView
    for row in tree.get_children():
        tree.delete(row)

    # Lấy dữ liệu từ cơ sở dữ liệu
    conn = sqlite3.connect('address_book.db')
    c = conn.cursor()
    c.execute("SELECT * FROM addresses")
    records = c.fetchall()

    # Hiển thị dữ liệu trong TreeView
    for r in records:
        tree.insert("", END, values=(r[0], r[1], r[2]))

    conn.close()

# Chức năng chỉnh sửa bản ghi
def chinh_sua():
    # Mở cửa sổ chỉnh sửa
    global editor
    editor = Tk()
    editor.title('Cập nhật bản ghi')
    editor.geometry("400x300")

    conn = sqlite3.connect('address_book.db')
    c = conn.cursor()
    record_id = delete_box.get()

    # Lấy dữ liệu của bản ghi theo ID
    c.execute("SELECT * FROM addresses WHERE id=:id", {'id': record_id})
    records = c.fetchall()

    # Các Entry trong cửa sổ chỉnh sửa
    global f_name_editor, l_name_editor, address_editor, city_editor, state_editor, zipcode_editor

    f_name_editor = Entry(editor, width=30)
    f_name_editor.grid(row=0, column=1, padx=20, pady=(10, 0))
    l_name_editor = Entry(editor, width=30)
    l_name_editor.grid(row=1, column=1)
    address_editor = Entry(editor, width=30)
    address_editor.grid(row=2, column=1)
    city_editor = Entry(editor, width=30)
    city_editor.grid(row=3, column=1)
    state_editor = Entry(editor, width=30)
    state_editor.grid(row=4, column=1)
    zipcode_editor = Entry(editor, width=30)
    zipcode_editor.grid(row=5, column=1)

    # Nhãn cho các Entry
    f_name_label = Label(editor, text="Họ")
    f_name_label.grid(row=0, column=0, pady=(10, 0))
    l_name_label = Label(editor, text="Tên")
    l_name_label.grid(row=1, column=0)
    address_label = Label(editor, text="Địa chỉ")
    address_label.grid(row=2, column=0)
    city_label = Label(editor, text="Thành phố")
    city_label.grid(row=3, column=0)
    state_label = Label(editor, text="Tỉnh/Thành")
    state_label.grid(row=4, column=0)
    zipcode_label = Label(editor, text="Mã bưu chính")
    zipcode_label.grid(row=5, column=0)

    # Điền dữ liệu đã có vào các ô nhập liệu
    for record in records:
        f_name_editor.insert(0, record[1])
        l_name_editor.insert(0, record[2])
        address_editor.insert(0, record[3])
        city_editor.insert(0, record[4])
        state_editor.insert(0, record[5])
        zipcode_editor.insert(0, record[6])

    # Nút lưu bản ghi chỉnh sửa
    edit_btn = Button(editor, text="Lưu bản ghi", command=cap_nhat)
    edit_btn.grid(row=6, column=0, columnspan=2, pady=10, padx=10, ipadx=100)

# Chức năng cập nhật bản ghi sau khi chỉnh sửa
def cap_nhat():
    conn = sqlite3.connect('address_book.db')
    c = conn.cursor()
    record_id = delete_box.get()

    # Cập nhật dữ liệu trong cơ sở dữ liệu
    c.execute("""UPDATE addresses SET
           first_name = :first,
           last_name = :last,
           address = :address,
           city = :city,
           state = :state,
           zipcode = :zipcode
           WHERE id = :id""",
              {
                  'first': f_name_editor.get(),
                  'last': l_name_editor.get(),
                  'address': address_editor.get(),
                  'city': city_editor.get(),
                  'state': state_editor.get(),
                  'zipcode': zipcode_editor.get(),
                  'id': record_id
              })

    conn.commit()
    conn.close()
    editor.destroy()

    # Cập nhật lại danh sách bản ghi sau khi chỉnh sửa
    truy_van()

# Frame trên cùng (Chứa các ô nhập liệu)
top_frame = Frame(root)
top_frame.pack(fill="x", padx=10, pady=10)

# Các ô nhập liệu
f_name = Entry(top_frame, width=30)
f_name.grid(row=0, column=1, padx=20, pady=(10, 0))
l_name = Entry(top_frame, width=30)
l_name.grid(row=1, column=1)
address = Entry(top_frame, width=30)
address.grid(row=2, column=1)
city = Entry(top_frame, width=30)
city.grid(row=3, column=1)
state = Entry(top_frame, width=30)
state.grid(row=4, column=1)
zipcode = Entry(top_frame, width=30)
zipcode.grid(row=5, column=1)

# Nhãn cho các ô nhập liệu
f_name_label = Label(top_frame, text="Họ")
f_name_label.grid(row=0, column=0, pady=(10, 0))
l_name_label = Label(top_frame, text="Tên")
l_name_label.grid(row=1, column=0)
address_label = Label(top_frame, text="Địa chỉ")
address_label.grid(row=2, column=0)
city_label = Label(top_frame, text="Thành phố")
city_label.grid(row=3, column=0)
state_label = Label(top_frame, text="Tỉnh/Thành")
state_label.grid(row=4, column=0)
zipcode_label = Label(top_frame, text="Mã bưu chính")
zipcode_label.grid(row=5, column=0)

# Frame ở giữa (Chứa các nút chức năng)
middle_frame = Frame(root)
middle_frame.pack(fill="x", padx=10, pady=10)

# Nút thêm bản ghi
submit_btn = Button(middle_frame, text="Thêm bản ghi", command=them)
submit_btn.grid(row=0, column=0, pady=10, padx=10, ipadx=20)

# Nút hiển thị bản ghi
query_btn = Button(middle_frame, text="Hiển thị bản ghi", command=truy_van)
query_btn.grid(row=0, column=1, pady=10, padx=10, ipadx=20)

# Ô nhập ID để xóa hoặc chỉnh sửa
delete_box_label = Label(middle_frame, text="Chọn ID")
delete_box_label.grid(row=1, column=0, pady=5)
delete_box = Entry(middle_frame, width=30)
delete_box.grid(row=1, column=1, pady=5)

# Nút xóa bản ghi
delete_btn = Button(middle_frame, text="Xóa bản ghi", command=xoa)
delete_btn.grid(row=2, column=0, pady=10, padx=10, ipadx=20)

# Nút chỉnh sửa bản ghi
edit_btn = Button(middle_frame, text="Chỉnh sửa bản ghi", command=chinh_sua)
edit_btn.grid(row=2, column=1, pady=10, padx=10, ipadx=20)

# Frame dưới cùng (Chứa bảng Treeview để hiển thị dữ liệu)
bottom_frame = Frame(root)
bottom_frame.pack(fill="both", expand=True, padx=10, pady=10)

# Treeview để hiển thị bản ghi
columns = ("ID", "Họ", "Tên")
tree = ttk.Treeview(bottom_frame, columns=columns, show="headings", height=8)

# Định nghĩa các cột trong Treeview
for column in columns:
    tree.column(column, anchor=CENTER)
    tree.heading(column, text=column)

tree.pack(fill="both", expand=True)

# Gọi hàm truy vấn để hiển thị dữ liệu khi khởi động
truy_van()

root.mainloop()
