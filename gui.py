import customtkinter as ctk
from tkinter import ttk, messagebox
import pandas as pd
from connect import connect_to_sql_server
from main import run_quality_engine

class DataQualityApp(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("Data Quality")
        self.geometry("1200x750")

        # --- LAYOUT CONFIG ---
        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(0, weight=1)

        # --- 1. SIDEBAR: Cấu hình kết nối ---
        self.sidebar = ctk.CTkFrame(self, width=300, corner_radius=0)
        self.sidebar.grid(row=0, column=0, sticky="nsew")
        
        ctk.CTkLabel(self.sidebar, text="KẾT NỐI HỆ THỐNG", font=("Arial", 18, "bold")).pack(pady=20)

        # Các ô nhập liệu 
        self.entry_server = self.create_input("Server Name:", r'DESKTOP-EMDJA3J\CSDLTTCS')
        self.entry_db = self.create_input("Database:", 'DataQualityDB')
        self.entry_driver = self.create_input("ODBC Driver:", '{ODBC Driver 17 for SQL Server}')

        self.btn_connect = ctk.CTkButton(self.sidebar, text="1. Kết nối & Xem trước", 
                                          command=self.handle_connect, fg_color="#1f538d")
        self.btn_connect.pack(pady=20, padx=20)

        self.btn_run = ctk.CTkButton(self.sidebar, text="2. Chạy chấm điểm", 
                                      command=self.handle_run, state="disabled", fg_color="#27ae60")
        self.btn_run.pack(pady=10, padx=20)

        # --- 2. MAIN VIEW: Hiển thị ---
        self.main_view = ctk.CTkFrame(self)
        self.main_view.grid(row=0, column=1, padx=20, pady=20, sticky="nsew")
        
        self.status_label = ctk.CTkLabel(self.main_view, text="Trạng thái: Chờ kết nối SQL Server", font=("Arial", 14))
        self.status_label.pack(pady=10)

        self.setup_table()

    def create_input(self, label, default):
        """Tạo label và ô nhập liệu nhanh"""
        ctk.CTkLabel(self.sidebar, text=label, anchor="w").pack(fill="x", padx=25)
        entry = ctk.CTkEntry(self.sidebar)
        entry.insert(0, default)
        entry.pack(fill="x", padx=25, pady=(0, 15))
        return entry

    def setup_table(self):
        """Khởi tạo bảng hiển thị dữ liệu gốc"""
        cols = ("Customer_ID", "Full_Name", "Age", "Email", "Phone", "Total_Spent", "Join_Date")
        self.tree = ttk.Treeview(self.main_view, columns=cols, show='headings')
        
        for col in cols:
            self.tree.heading(col, text=col.replace("_", " "))
            self.tree.column(col, width=120, anchor="center")

        scroll = ttk.Scrollbar(self.main_view, orient="vertical", command=self.tree.yview)
        self.tree.configure(yscrollcommand=scroll.set)
        
        self.tree.pack(expand=True, fill='both', padx=10, pady=10)
        scroll.pack(side="right", fill="y")

   

    def handle_connect(self):
       
        server = self.entry_server.get()
        db = self.entry_db.get()
        driver = self.entry_driver.get()

        self.status_label.configure(text="Đang truy vấn SQL Server...", text_color="yellow")
        self.update()

        
        df = connect_to_sql_server(server, db, driver)
 
        if df is not None:
            # Xóa bảng cũ và nạp 100 dòng đầu để preview
            self.tree.delete(*self.tree.get_children())
            for _, row in df.head(100).iterrows():
                self.tree.insert("", "end", values=list(row)[:7]) # Chỉ lấy 7 cột đầu
            
            self.status_label.configure(text=f"Nạp thành công {len(df)} dòng dữ liệu!", text_color="#2ecc71")
            self.btn_run.configure(state="normal")
        else:
            self.status_label.configure(text="Lỗi kết nối", text_color="#e74c3c")

    def handle_run(self):
        # Lấy thông số
        server = self.entry_server.get()
        db = self.entry_db.get()
        driver = self.entry_driver.get()
        rules_path = "rules/dq_rules.json" 

        self.status_label.configure(text="Hệ thống đang chấm điểm chất lượng...", text_color="cyan")
        self.update()

        try:
            report_df, final_score, dirty_df = run_quality_engine(rules_path, server, db, driver)

            messagebox.showinfo("Kết quả", 
                f"Điểm chất lượng tổng quát: {round(final_score, 2)}/100\n"
                f"Số dòng phát hiện lỗi: {len(dirty_df)}")
            
            self.status_label.configure(text=f"Điểm: {round(final_score, 2)}/100", text_color="#2ecc71")
            if not report_df.empty:
                self.show_report_window(report_df)
            if not dirty_df.empty:
                self.show_error_window(dirty_df)

        except Exception as e:
            messagebox.showerror("Lỗi", f"Quá trình xử lý thất bại: {e}")

    def show_error_window(self, df):
        """Cửa sổ phụ hiện danh sách lỗi vi phạm (dirty_df)"""
        # Kiểm tra nếu cửa sổ đã tồn tại và chưa bị đóng thì không tạo mới
        if hasattr(self, "error_win") and self.error_win.winfo_exists():
            self.error_win.focus() 
            return

        self.error_win = ctk.CTkToplevel(self)
        self.error_win.title("Danh sách dòng dữ liệu vi phạm")
        self.error_win.geometry("800x400")
        
        # Mẹo: Ép cửa sổ phụ luôn nổi lên trên cửa sổ chính
        self.error_win.attributes("-topmost", True)

        cols = list(df.columns)
        tree_err = ttk.Treeview(self.error_win, columns=cols, show='headings')
        for col in cols:
            tree_err.heading(col, text=col)
            tree_err.column(col, width=150)
        
        for _, row in df.head(200).iterrows():
            tree_err.insert("", "end", values=list(row))
        
        tree_err.pack(expand=True, fill='both', padx=10, pady=10)

    def show_report_window(self, df):
        """Cửa sổ phụ hiện Báo cáo (report_df)"""
        if hasattr(self, "report_win") and self.report_win.winfo_exists():
            self.report_win.focus()
            return

        self.report_win = ctk.CTkToplevel(self)
        self.report_win.title("Báo cáo chi tiết")
        self.report_win.geometry("800x400")
        
        self.report_win.attributes("-topmost", True)

        cols = list(df.columns)
        tree_rep = ttk.Treeview(self.report_win, columns=cols, show='headings')
        for col in cols:
            tree_rep.heading(col, text=col)
            tree_rep.column(col, width=150)
        
        for _, row in df.iterrows():
            tree_rep.insert("", "end", values=list(row))
        
        tree_rep.pack(expand=True, fill='both', padx=10, pady=10)

if __name__ == "__main__":
    app = DataQualityApp()
    app.mainloop()