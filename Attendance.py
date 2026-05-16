import tkinter as tk
from tkinter import ttk, messagebox
from datetime import datetime
import database

class AttendanceApp:
    def __init__(self, root):
        self.root = root
        self.root.title("School Attendance Ledger")
        self.root.geometry("1100x750")
        self.root.configure(bg="#FAFAFA")
        
        database.init_db()
        self.selected_date = datetime.now().strftime("%Y-%m-%d")
        
        self.setup_styles()
        self.create_widgets()
        self.load_students_table()

    def setup_styles(self):
        self.style = ttk.Style()
        self.style.theme_use("clam")
        
        # Main Treeview Design
        self.style.configure("Treeview", 
                             background="#FFFFFF", 
                             fieldbackground="#FFFFFF", 
                             foreground="#1A1A1A",
                             rowheight=38,
                             font=("Segoe UI", 10))
        self.style.configure("Treeview.Heading", 
                             background="#FAFAFA", 
                             foreground="#1A1A1A",
                             font=("Segoe UI Semibold", 11),
                             borderwidth=0)
        self.style.map("Treeview", background=[("selected", "#007AFF")], foreground=[("selected", "#FFFFFF")])
        
        # Side Groups Design
        self.style.configure("Summary.Treeview", 
                             background="#FFFFFF", 
                             fieldbackground="#FFFFFF", 
                             foreground="#1A1A1A",
                             rowheight=30,
                             font=("Segoe UI", 9))
        self.style.configure("Summary.Treeview.Heading", 
                             background="#FAFAFA", 
                             foreground="#1A1A1A",
                             font=("Segoe UI Semibold", 9),
                             borderwidth=0)

    def create_widgets(self):
        # Header Area
        header = tk.Frame(self.root, bg="#FAFAFA")
        header.pack(fill="x", padx=40, pady=(30, 15))
        
        title_label = tk.Label(header, text="Attendance Management", font=("Segoe UI Display", 24, "bold"), fg="#1A1A1A", bg="#FAFAFA")
        title_label.pack(side="left")
        
        self.date_label = tk.Label(header, text=f"Session Date: {self.selected_date}", font=("Segoe UI Semibold", 12), fg="#8E8E93", bg="#FAFAFA")
        self.date_label.pack(side="right", pady=(10, 0))

        # Main Split Container
        main_container = tk.Frame(self.root, bg="#FAFAFA")
        main_container.pack(fill="both", expand=True, padx=40, pady=(0, 20))

        # ================= LEFT PANEL: Enrollment & Actions =================
        left_panel = tk.Frame(main_container, bg="#FAFAFA")
        left_panel.pack(side="left", fill="y", padx=(0, 20))

        reg_title = tk.Label(left_panel, text="STUDENT ROSTER", font=("Segoe UI Semibold", 10), fg="#8E8E93", bg="#FAFAFA")
        reg_title.pack(anchor="w", pady=(0, 10))

        tk.Label(left_panel, text="Student ID", font=("Segoe UI", 10), fg="#1A1A1A", bg="#FAFAFA").pack(anchor="w")
        self.entry_id = tk.Entry(left_panel, font=("Segoe UI", 11), bg="#FFFFFF", fg="#1A1A1A", bd=1, relief="solid", width=22)
        self.entry_id.pack(anchor="w", pady=(5, 10))

        tk.Label(left_panel, text="Full Name", font=("Segoe UI", 10), fg="#1A1A1A", bg="#FAFAFA").pack(anchor="w")
        self.entry_name = tk.Entry(left_panel, font=("Segoe UI", 11), bg="#FFFFFF", fg="#1A1A1A", bd=1, relief="solid", width=22)
        self.entry_name.pack(anchor="w", pady=(5, 15))

        btn_add = tk.Button(left_panel, text="Add Student", bg="#1A1A1A", fg="#FFFFFF", font=("Segoe UI Semibold", 10), bd=0, width=22, height=2, activebackground="#333333", activeforeground="#FFFFFF", cursor="hand2")
        btn_add.config(command=self.add_student)
        btn_add.pack(anchor="w", pady=(0, 10))

        btn_delete = tk.Button(left_panel, text="Remove Selection", bg="#FFFFFF", fg="#1A1A1A", font=("Segoe UI Semibold", 10), bd=1, relief="solid", highlightthickness=0, width=22, height=2, activebackground="#FAFAFA", cursor="hand2")
        btn_delete.config(command=self.delete_student)
        btn_delete.pack(anchor="w", pady=(0, 35))

        att_title = tk.Label(left_panel, text="ACTIONS", font=("Segoe UI Semibold", 10), fg="#8E8E93", bg="#FAFAFA")
        att_title.pack(anchor="w", pady=(0, 10))

        btn_present = tk.Button(left_panel, text="Mark Present", bg="#007AFF", fg="#FFFFFF", font=("Segoe UI Semibold", 10), bd=0, width=22, height=2, activebackground="#0063CC", activeforeground="#FFFFFF", cursor="hand2")
        btn_present.config(command=lambda: self.set_attendance("Present"))
        btn_present.pack(anchor="w", pady=(0, 10))

        btn_absent = tk.Button(left_panel, text="Mark Absent", bg="#FFFFFF", fg="#1A1A1A", font=("Segoe UI Semibold", 10), bd=1, relief="solid", highlightthickness=0, width=22, height=2, activebackground="#FAFAFA", cursor="hand2")
        btn_absent.config(command=lambda: self.set_attendance("Absent"))
        btn_absent.pack(anchor="w")

        # ================= CENTER PANEL: Core Ledger Grid =================
        center_panel = tk.Frame(main_container, bg="#FFFFFF")
        center_panel.pack(side="left", fill="both", expand=True, padx=10)

        columns = ("id", "name", "status")
        self.tree = ttk.Treeview(center_panel, columns=columns, show="headings", selectmode="browse")
        
        self.tree.heading("id", text="Student ID", anchor="w")
        self.tree.heading("name", text="Full Name", anchor="w")
        self.tree.heading("status", text="Attendance Status", anchor="w")
        
        self.tree.column("id", width=120, anchor="w")
        self.tree.column("name", width=250, anchor="w")
        self.tree.column("status", width=120, anchor="w")
        self.tree.pack(fill="both", expand=True)
        
        # Color Tags Mapping
        self.tree.tag_configure("Present", background="#E1F5FE", foreground="#0288D1") 
        self.tree.tag_configure("Absent", background="#FFEBEE", foreground="#C62828")   
        self.tree.tag_configure("Unmarked", background="#FFFFFF", foreground="#1A1A1A")

        # ================= RIGHT PANEL: Real-time Group Splits =================
        right_panel = tk.Frame(main_container, bg="#FAFAFA", width=280)
        right_panel.pack(side="right", fill="both", padx=(20, 0))
        right_panel.pack_propagate(False)

        # Present Bucket
        lbl_pres_group = tk.Label(right_panel, text="PRESENT GROUP", font=("Segoe UI Semibold", 9), fg="#0288D1", bg="#FAFAFA")
        lbl_pres_group.pack(anchor="w", pady=(0, 5))
        
        self.tree_present = ttk.Treeview(right_panel, columns=("name",), show="headings", style="Summary.Treeview", height=10)
        self.tree_present.heading("name", text="Student Name", anchor="w")
        self.tree_present.column("name", width=260)
        self.tree_present.pack(fill="x", pady=(0, 20))

        # Absent Bucket
        lbl_abs_group = tk.Label(right_panel, text="ABSENT GROUP", font=("Segoe UI Semibold", 9), fg="#C62828", bg="#FAFAFA")
        lbl_abs_group.pack(anchor="w", pady=(0, 5))

        self.tree_absent = ttk.Treeview(right_panel, columns=("name",), show="headings", style="Summary.Treeview", height=10)
        self.tree_absent.heading("name", text="Student Name", anchor="w")
        self.tree_absent.column("name", width=260)
        self.tree_absent.pack(fill="x")

    def load_students_table(self):
        # Linisin ang mga lumang data sa view boxes bago mag-refresh
        for item in self.tree.get_children(): self.tree.delete(item)
        for item in self.tree_present.get_children(): self.tree_present.delete(item)
        for item in self.tree_absent.get_children(): self.tree_absent.delete(item)
            
        conn = database.get_connection()
        cursor = conn.cursor()
        
        # Pull data directly and format matching tags dynamically
        query = """
            SELECT s.id, s.name, COALESCE(a.status, 'Unmarked') 
            FROM students s
            LEFT JOIN attendance a ON CAST(s.id AS TEXT) = CAST(a.student_id AS TEXT) AND a.date = ?
            ORDER BY s.name ASC
        """
        cursor.execute(query, (self.selected_date,))
        rows = cursor.fetchall()
        
        for row in rows:
            status = row[2]
            self.tree.insert("", "end", values=row, tags=(status,))
            
            # Piliting pumasok sa mga kahon sa kanan base sa nakuha niyang status
            if status == "Present":
                self.tree_present.insert("", "end", values=(row[1],))
            elif status == "Absent":
                self.tree_absent.insert("", "end", values=(row[1],))
                
        conn.close()

    def add_student(self):
        s_id = str(self.entry_id.get()).strip()
        s_name = self.entry_name.get().strip()
        
        if not s_id or not s_name:
            messagebox.showwarning("Required Input", "Please populate both Student ID and Full Name fields.")
            return
            
        conn = database.get_connection()
        cursor = conn.cursor()
        try:
            cursor.execute("INSERT INTO students (id, name) VALUES (?, ?)", (s_id, s_name))
            conn.commit()
            self.entry_id.delete(0, tk.END)
            self.entry_name.delete(0, tk.END)
            self.load_students_table()
        except sqlite3.IntegrityError:
            messagebox.showerror("Error", f"Student ID '{s_id}' already exists.")
        finally:
            conn.close()

    def delete_student(self):
        selected_item = self.tree.selection()
        if not selected_item:
            messagebox.showwarning("Selection Required", "Please choose a record from the ledger list to remove.")
            return
            
        student_id = str(self.tree.item(selected_item)["values"][0]).strip()
        student_name = self.tree.item(selected_item)["values"][1]
        
        confirm = messagebox.askyesno("Confirm Deletion", f"Permanently remove {student_name}?")
        if confirm:
            conn = database.get_connection()
            cursor = conn.cursor()
            cursor.execute("DELETE FROM attendance WHERE CAST(student_id AS TEXT) = CAST(? AS TEXT)", (student_id,))
            cursor.execute("DELETE FROM students WHERE CAST(id AS TEXT) = CAST(? AS TEXT)", (student_id,))
            conn.commit()
            conn.close()
            self.load_students_table()

    def set_attendance(self, status):
        selected_item = self.tree.selection()
        
        if not selected_item:
            messagebox.showwarning("Selection Required", "Please select a student from the middle table first.")
            return
        else:
            item_data = self.tree.item(selected_item)
            student_values = item_data.get("values", [])
            
            if len(student_values) == 0:
                return
            else:
                # Dito natin pinupwersa na maging malinis na Text String ang ID para walang kawala ang SQL query natin
                student_id = str(student_values[0]).strip()
                
                conn = database.get_connection()
                cursor = conn.cursor()
                
                # Check kung umiiral na ang raw text match record
                cursor.execute("SELECT * FROM attendance WHERE CAST(student_id AS TEXT) = CAST(? AS TEXT) AND date = ?", (student_id, self.selected_date))
                existing_record = cursor.fetchone()
                
                if existing_record is None:
                    cursor.execute(
                        "INSERT INTO attendance (student_id, date, status) VALUES (?, ?, ?)",
                        (student_id, self.selected_date, status)
                    )
                else:
                    cursor.execute(
                        "UPDATE attendance SET status = ? WHERE CAST(student_id AS TEXT) = CAST(? AS TEXT) AND date = ?",
                        (status, student_id, self.selected_date)
                    )
                
                conn.commit()
                conn.close()
                
                # I-refresh at linisin ang blue highlight para lumabas agad ang kulay at tumalon sa mga side groups
                self.load_students_table()
                try:
                    self.tree.selection_remove(selected_item)
                except:
                    pass

if __name__ == "__main__":
    root = tk.Tk()
    app = AttendanceApp(root)
    root.mainloop()