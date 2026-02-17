import tkinter as tk
from tkinter import filedialog, messagebox, Toplevel, scrolledtext
from PIL import Image, ImageTk
from LinkedinQueenSolver import LinkedinQueenSolver
import time


class LiveUpdateWindow:
    def __init__(self, parent, method, iteration_live_update, found_solution):
        self.parent = parent
        self.live_update = iteration_live_update  
        self.current_index = 0
        self.board = parent.solver.board
        self.n = parent.solver.n
        self.color_map = parent.color_map
        self.window = Toplevel(parent.root)
        self.window.title(f"Live Update - {method}")
        self.window.configure(bg='#1a1a2e')
        self.window.geometry("550x650")
        
        self.setup_ui(method, found_solution)
        
    def setup_ui(self, method, found_solution):
        bg_color = '#1a1a2e'
        frame_color = '#16213e'
        accent_color = '#e94560'
        text_color = '#eaeaea'
        button_color = '#0f3460'
        
        lbl_title = tk.Label(self.window, text=f"Live Update - {method}",
                              font=("Arial", 16, "bold"), bg=bg_color, fg=accent_color)
        lbl_title.pack(pady=10)

        self.lbl_iteration = tk.Label(self.window, text="",
                                       font=("Arial", 12), bg=bg_color, fg=text_color)
        self.lbl_iteration.pack(pady=5)
        
        self.canvas_size = 400
        self.canvas = tk.Canvas(self.window, width=self.canvas_size, 
                                 height=self.canvas_size, bg=frame_color,
                                 highlightthickness=3, highlightbackground=accent_color)
        self.canvas.pack(padx=10, pady=10)
        
        nav_frame = tk.Frame(self.window, bg=bg_color)
        nav_frame.pack(pady=10)
        
        self.btn_prev = tk.Button(nav_frame, text=" Prev", command=self.prev_snapshot,
                                   font=("Arial", 10, "bold"), bg=button_color, fg=text_color,
                                   width=10, height=2)
        self.btn_prev.pack(side=tk.LEFT, padx=10)
        
        self.lbl_page = tk.Label(nav_frame, text="", font=("Arial", 11), 
                                  bg=bg_color, fg=text_color, width=15)
        self.lbl_page.pack(side=tk.LEFT, padx=10)
        
        self.btn_next = tk.Button(nav_frame, text="Next ", command=self.next_snapshot,
                                   font=("Arial", 10, "bold"), bg=button_color, fg=text_color,
                                   width=10, height=2)
        self.btn_next.pack(side=tk.LEFT, padx=10)
        
        if found_solution:
            status_text = "Solusi ditemukan"
            status_color = '#4ECDC4'
        else:
            status_text = "Solusi tidak ditemukan."
            status_color = '#e94560'
        
        lbl_status = tk.Label(self.window, text=status_text,
                               font=("Arial", 11), bg=bg_color, fg=status_color)
        lbl_status.pack(pady=5)
        
        btn_close = tk.Button(self.window, text="Close", command=self.window.destroy,
                               font=("Arial", 10, "bold"), bg='#e94560', fg='white',
                               width=10, height=2)
        btn_close.pack(pady=10)
        
        if self.live_update:
            self.draw_snapshot()
            self.update_navigation()
    
    # gambar snapshot board untuk live update window
    def draw_snapshot(self):
        self.canvas.delete("all")
        
        if not self.live_update or self.board is None:
            return
        
        iteration, config = self.live_update[self.current_index]
        q_positions = set(config)
        
        cell_size = self.canvas_size // self.n
        offset = (self.canvas_size - cell_size * self.n) // 2
        
        for r in range(self.n):
            for c in range(self.n):
                x1 = offset + c * cell_size
                y1 = offset + r * cell_size
                x2 = x1 + cell_size
                y2 = y1 + cell_size
                
                char = self.board[r][c]
                color = self.color_map.get(char, 'lightgray')
                
                self.canvas.create_rectangle(x1, y1, x2, y2, 
                                              fill=color, outline='#1a1a2e', width=2)
                
                if (r, c) in q_positions:
                    padding = cell_size // 6
                    self.canvas.create_oval(x1 + padding, y1 + padding,
                                            x2 - padding, y2 - padding,
                                            fill='white', outline='#1a1a2e', width=2)
                    font_size = max(12, cell_size // 2)
                    self.canvas.create_text((x1 + x2) // 2, (y1 + y2) // 2,
                                            text="Q", font=("Arial", font_size),
                                            fill='#1a1a2e')
        
        self.lbl_iteration.config(text=f"Iterasi ke-{iteration}")
    
    def update_navigation(self):
        total = len(self.live_update)
        self.lbl_page.config(text=f"{self.current_index + 1} / {total}")
        
        self.btn_prev.config(state=tk.NORMAL if self.current_index > 0 else tk.DISABLED)
        self.btn_next.config(state=tk.NORMAL if self.current_index < total - 1 else tk.DISABLED)
    
    def prev_snapshot(self):
        if self.current_index > 0:
            self.current_index -= 1
            self.draw_snapshot()
            self.update_navigation()
    
    def next_snapshot(self):
        if self.current_index < len(self.live_update) - 1:
            self.current_index += 1
            self.draw_snapshot()
            self.update_navigation()


class LinkedinQueenGUI: 
    def __init__(self, root):
        self.root = root
        self.root.title("LinkedIn Queen Solver")
        self.root.configure(bg='#1a1a2e')
        self.root.resizable(False, False)
        self.solver = LinkedinQueenSolver()
        
        self.color_map = {}
        self.color_palette = [
            '#FF6B6B', '#4ECDC4', '#45B7D1', '#96CEB4', '#FFEAA7',
            '#DDA0DD', '#98D8C8', '#F7DC6F', '#BB8FCE', '#85C1E9',
            '#F8B500', '#00CED1', '#FF69B4', '#32CD32', '#FFD700',
            '#FF7F50', '#6495ED', '#DC143C', '#00FA9A', '#FF1493',
            '#8B4513', '#20B2AA', '#BA55D3', '#CD853F', '#4682B4', 
            '#9ACD32'
        ]
        
        self.extracted_colors = {}
        self.original_image = None
        self.image_tk = None
        self.grid_mode = False
        self.board_size = 0
        self.iteration_live_update = []
        self.last_method = None    
        self.button_color = '#0f3460'
        self.setup_ui()
    
    def setup_ui(self):
        bg_color = '#1a1a2e'
        frame_color = '#16213e'
        accent_color = '#e94560'
        text_color = '#eaeaea'
        button_color = '#0f3460'
        
        self.main_frame = tk.Frame(self.root, bg=bg_color, padx=20, pady=20)
        self.main_frame.pack()
        
        self.lbl_title = tk.Label(self.main_frame, text="LinkedIn Queen Solver", 
                                   font=("Arial", 24, "bold"), bg=bg_color, fg=accent_color)
        self.lbl_title.grid(row=0, column=0, columnspan=2, pady=(0, 20))
        
        self.top_frame = tk.Frame(self.main_frame, bg=bg_color)
        self.top_frame.grid(row=1, column=0, columnspan=2, pady=(0, 15), sticky='w')
        
        self.btn_input_file = tk.Button(self.top_frame, text="Input\nFile", 
                                         command=self.load_file, width=10, height=2,
                                         font=("Arial", 10, "bold"), bg=button_color, fg=text_color,
                                         relief='ridge', bd=3)
        self.btn_input_file.pack(side=tk.LEFT, padx=5)
        
        self.btn_input_image = tk.Button(self.top_frame, text="Input\nImage", 
                                          command=self.load_image, width=10, height=2,
                                          font=("Arial", 10, "bold"), bg=button_color, fg=text_color,
                                          relief='ridge', bd=3)
        self.btn_input_image.pack(side=tk.LEFT, padx=5)
        
        self.lbl_board_size = tk.Label(self.top_frame, text="Board Size:", 
                                        font=("Arial", 11), bg=bg_color, fg=text_color)
        self.lbl_board_size.pack(side=tk.LEFT, padx=(20, 5))
        
        self.entry_board_size = tk.Entry(self.top_frame, width=8, font=("Arial", 12),
                                          bg=frame_color, fg=text_color, insertbackground=text_color)
        self.entry_board_size.pack(side=tk.LEFT, padx=5)
        self.entry_board_size.insert(0, "4")
        
        self.btn_apply_size = tk.Button(self.top_frame, text="Apply", 
                                         command=self.apply_board_size, width=6,
                                         font=("Arial", 9), bg=accent_color, fg=text_color)
        self.btn_apply_size.pack(side=tk.LEFT, padx=5)
        
        self.middle_frame = tk.Frame(self.main_frame, bg=bg_color)
        self.middle_frame.grid(row=2, column=0, columnspan=2, pady=10)
        
        self.canvas_size = 450
        self.canvas = tk.Canvas(self.middle_frame, width=self.canvas_size, 
                                 height=self.canvas_size, bg=frame_color,
                                 highlightthickness=3, highlightbackground=accent_color)
        self.canvas.pack(side=tk.LEFT, padx=(0, 20))
        self.canvas.bind("<Button-1>", self.on_canvas_click)
        
        self.info_frame = tk.Frame(self.middle_frame, bg=frame_color, padx=15, pady=15,
                                    highlightthickness=2, highlightbackground=accent_color)
        self.info_frame.pack(side=tk.LEFT, fill=tk.Y)
        
        info_font = ("Arial", 11)
        
        self.lbl_info_title = tk.Label(self.info_frame, text="Statistics", 
                                        font=("Arial", 14, "bold"), bg=frame_color, fg=accent_color)
        self.lbl_info_title.pack(pady=(0, 15))
        
        self.lbl_board_size_info = tk.Label(self.info_frame, text="Board Size: -", 
                                             font=info_font, bg=frame_color, fg=text_color, anchor='w')
        self.lbl_board_size_info.pack(fill=tk.X, pady=5)
        
        self.lbl_time = tk.Label(self.info_frame, text="Time: -", 
                                  font=info_font, bg=frame_color, fg=text_color, anchor='w')
        self.lbl_time.pack(fill=tk.X, pady=5)
        
        self.lbl_total_possible = tk.Label(self.info_frame, text="Total Possible\nConfigurations: -", 
                                            font=info_font, bg=frame_color, fg=text_color, anchor='w',
                                            justify=tk.LEFT)
        self.lbl_total_possible.pack(fill=tk.X, pady=5)
        
        self.lbl_total_checked = tk.Label(self.info_frame, text="Total Configurations\nChecked: -", 
                                           font=info_font, bg=frame_color, fg=text_color, anchor='w',
                                           justify=tk.LEFT)
        self.lbl_total_checked.pack(fill=tk.X, pady=5)
        
        tk.Label(self.info_frame, text="", bg=frame_color).pack(pady=10)
        
        self.btn_live_update = tk.Button(self.info_frame, text="Live Update", 
                                          command=self.open_live_update_window, width=12, height=2,
                                          font=("Arial", 10, "bold"), bg=button_color, fg=text_color,
                                          relief='ridge', bd=3, state=tk.DISABLED)
        self.btn_live_update.pack(pady=10)
        
        self.btn_save = tk.Button(self.info_frame, text="Save as\nImage", 
                                   command=self.save_solution_image, width=12, height=2,
                                   font=("Arial", 10, "bold"), bg=button_color, fg=text_color,
                                   relief='ridge', bd=3, state=tk.DISABLED)
        self.btn_save.pack(pady=10)
        
        self.btn_save_txt = tk.Button(self.info_frame, text="Save as\nTxt", 
                                       command=self.save_solution_txt, width=12, height=2,
                                       font=("Arial", 10, "bold"), bg=button_color, fg=text_color,
                                       relief='ridge', bd=3, state=tk.DISABLED)
        self.btn_save_txt.pack(pady=10)
        
        self.lbl_status = tk.Label(self.info_frame, text="", 
                                    font=("Arial", 10), bg=frame_color, fg=text_color,
                                    wraplength=120, justify=tk.CENTER)
        self.lbl_status.pack(pady=(5, 0))
        
        self.bottom_frame = tk.Frame(self.main_frame, bg=bg_color)
        self.bottom_frame.grid(row=3, column=0, columnspan=2, pady=(20, 0))
        
        self.lbl_solve = tk.Label(self.bottom_frame, text="Solve with:", 
                                   font=("Arial", 12, "bold"), bg=bg_color, fg=text_color)
        self.lbl_solve.pack(side=tk.LEFT, padx=(0, 20))
        
        self.btn_brute = tk.Button(self.bottom_frame, text="Brute Force", 
                                    command=self.solve_brute_force, width=15, height=2,
                                    font=("Arial", 11, "bold"), bg=button_color, fg=text_color,
                                    relief='ridge', bd=3, state=tk.DISABLED)
        self.btn_brute.pack(side=tk.LEFT, padx=10)
        
        self.btn_optimized = tk.Button(self.bottom_frame, text="Optimized\nBrute Force", 
                                        command=self.solve_optimized, width=15, height=2,
                                        font=("Arial", 11, "bold"), bg=button_color, fg=text_color,
                                        relief='ridge', bd=3, state=tk.DISABLED)
        self.btn_optimized.pack(side=tk.LEFT, padx=10)
    
    # load board dari file .txt 
    def load_file(self):
        filename = filedialog.askopenfilename(
            title="Pilih file input",
            filetypes=[("Text files", "*.txt"), ("All files", "*.*")]
        )
        
        if filename:
            try:
                result = self.solver.read_board(filename)
                
                if result is None:
                    self.lbl_status.config(text="input tidak valid", fg='#e94560')
                    self.disable_solve_buttons()
                    return
                
                self.solver.solution = None
                self.solver.total_possibilities = 0
                self.solver.total_checked = 0
                self.solver.time_ms = 0
                self.iteration_live_update = []
                self.btn_save.config(state=tk.DISABLED)
                self.btn_save_txt.config(state=tk.DISABLED)
                self.btn_live_update.config(state=tk.DISABLED)
                
                self.board_size = self.solver.n
                self.entry_board_size.delete(0, tk.END)
                self.entry_board_size.insert(0, str(self.board_size))
                
                self.assign_colors()
                self.draw_board()
                self.update_info()
                
                self.lbl_status.config(text="Board loaded from file. Ready to solve", fg='#4ECDC4')
                self.enable_solve_buttons()
                
            except Exception as e:
                messagebox.showerror("Error", f"Gagal membaca file:\n{str(e)}")
    
    # load image 
    def load_image(self):
        filename = filedialog.askopenfilename(
            title="Pilih image",
            filetypes=[("Image files", "*.png *.jpg *.jpeg *.bmp *.gif"), ("All files", "*.*")]
        )
        
        if filename:
            try:
                self.solver.solution = None
                self.solver.total_possibilities = 0
                self.solver.total_checked = 0
                self.solver.time_ms = 0
                self.iteration_live_update = []
                self.btn_save.config(state=tk.DISABLED)
                self.btn_save_txt.config(state=tk.DISABLED)
                self.btn_live_update.config(state=tk.DISABLED)
                
                self.original_image = Image.open(filename).convert('RGB')
                self.display_image_on_canvas()
                self.grid_mode = True
                
                self.lbl_status.config(text="Image loaded. Set board size, click Apply, then click image.", 
                                        fg='#FFEAA7')
                
            except Exception as e:
                messagebox.showerror("Error", f"Gagal membaca image:\n{str(e)}")
    
    def display_image_on_canvas(self):
        if self.original_image is None:
            return
        
        img_ratio = self.original_image.width / self.original_image.height
        
        if img_ratio > 1:
            new_width = self.canvas_size
            new_height = int(self.canvas_size / img_ratio)
        else:
            new_height = self.canvas_size
            new_width = int(self.canvas_size * img_ratio)
        
        resized = self.original_image.resize((new_width, new_height), Image.Resampling.LANCZOS)
        self.image_tk = ImageTk.PhotoImage(resized)
        
        self.canvas.delete("all")
        
        x_offset = (self.canvas_size - new_width) // 2
        y_offset = (self.canvas_size - new_height) // 2
        
        self.canvas.create_image(x_offset, y_offset, anchor=tk.NW, image=self.image_tk, tags="image")
        self.image_bounds = (x_offset, y_offset, x_offset + new_width, y_offset + new_height)
    
    def apply_board_size(self):
        try:
            size = int(self.entry_board_size.get())
            if size < 1 or size > 20:
                raise ValueError("Size harus antara 1-20")
            
            self.board_size = size
            
            if self.original_image is not None and self.grid_mode:
                self.extract_colors_from_image()
            
        except ValueError as e:
            messagebox.showerror("Error", f"Invalid board size: {str(e)}")
    
    def draw_grid_overlay(self):
        if not hasattr(self, 'image_bounds') or self.board_size == 0:
            return
        
        self.canvas.delete("grid")
        
        x1, y1, x2, y2 = self.image_bounds
        width = x2 - x1
        height = y2 - y1
        
        cell_w = width / self.board_size
        cell_h = height / self.board_size
        
        for i in range(self.board_size + 1):
            self.canvas.create_line(x1, y1 + i * cell_h, x2, y1 + i * cell_h, 
                                     fill='#e94560', width=2, tags="grid")
            self.canvas.create_line(x1 + i * cell_w, y1, x1 + i * cell_w, y2, 
                                     fill='#e94560', width=2, tags="grid")
    
    def on_canvas_click(self, event):
        if self.grid_mode and self.original_image is not None and self.board_size > 0:
            self.extract_colors_from_image()
    
    # Mengambil warna dominan dari area cell pada image
    def get_dominant_color(self, img, x1, y1, x2, y2):
        padding = 2
        x1 = max(0, int(x1) + padding)
        y1 = max(0, int(y1) + padding)
        x2 = min(img.width, int(x2) - padding)
        y2 = min(img.height, int(y2) - padding)
        
        if x2 <= x1 or y2 <= y1:
            x1, y1 = max(0, int(x1)), max(0, int(y1))
            x2, y2 = min(img.width, int(x2) + padding * 2), min(img.height, int(y2) + padding * 2)
        
        total_r, total_g, total_b = 0, 0, 0
        count = 0
        
        center_x1 = x1 + (x2 - x1) * 0.2
        center_y1 = y1 + (y2 - y1) * 0.2
        center_x2 = x1 + (x2 - x1) * 0.8
        center_y2 = y1 + (y2 - y1) * 0.8
        
        step = max(1, int((center_x2 - center_x1) / 5))
        
        for px in range(int(center_x1), int(center_x2), step):
            for py in range(int(center_y1), int(center_y2), step):
                if 0 <= px < img.width and 0 <= py < img.height:
                    try:
                        pixel = img.getpixel((px, py))
                        if isinstance(pixel, tuple):
                            r, g, b = pixel[:3]
                        else:
                            r = g = b = pixel
                        total_r += r
                        total_g += g
                        total_b += b
                        count += 1
                    except:
                        pass
        
        if count == 0:
            cx, cy = (x1 + x2) // 2, (y1 + y2) // 2
            pixel = img.getpixel((int(cx), int(cy)))
            if isinstance(pixel, tuple):
                return pixel[:3]
            return (pixel, pixel, pixel)
        
        return (total_r // count, total_g // count, total_b // count)
    
    # Mengecek kesamaan dua warna RGB 
    def color_similarity(self, c1, c2, threshold=40):
        return (abs(c1[0] - c2[0]) < threshold and 
                abs(c1[1] - c2[1]) < threshold and 
                abs(c1[2] - c2[2]) < threshold)
    
    # Mengekstrak warna 
    def extract_colors_from_image(self):
        if not hasattr(self, 'image_bounds') or self.original_image is None:
            return
        
        try:
            img = self.original_image
            img_cell_w = img.width / self.board_size
            img_cell_h = img.height / self.board_size
            
            board = []
            detected_colors = []  
            char_counter = 0
            
            for r in range(self.board_size):
                row = []
                for c in range(self.board_size):
                    cell_x1 = c * img_cell_w
                    cell_y1 = r * img_cell_h
                    cell_x2 = (c + 1) * img_cell_w
                    cell_y2 = (r + 1) * img_cell_h
                    
                    avg_color = self.get_dominant_color(img, cell_x1, cell_y1, cell_x2, cell_y2)
                    
                    found_char = None
                    for existing_color, existing_char in detected_colors:
                        if self.color_similarity(avg_color, existing_color):
                            found_char = existing_char
                            break
                    
                    if found_char is None:
                        found_char = chr(ord('A') + char_counter)
                        detected_colors.append((avg_color, found_char))
                        char_counter += 1
                    
                    row.append(found_char)
                board.append(row)
            
            self.extracted_colors = {char: color for color, char in detected_colors}
            
            print(f"\nExtracted {len(detected_colors)} colors from image:")
            for color, char in detected_colors:
                print(f"  {char}: RGB{color}")
            print(f"\nBoard:")
            for row in board:
                print("  " + " ".join(row))
            
            self.solver.board = board
            self.solver.n = self.board_size
            self.solver.solution = None
            self.solver.total_possibilities = 0
            self.solver.total_checked = 0
            self.solver.time_ms = 0
            
            self.grid_mode = False
            self.assign_colors_from_extracted()
            self.draw_board()
            self.update_info()
            
            self.lbl_status.config(text=f"Extracted {len(detected_colors)} colors.", fg='#4ECDC4')
            self.enable_solve_buttons()
            
        except Exception as e:
            import traceback
            traceback.print_exc()
            messagebox.showerror("Error", f"Failed to extract colors:\n{str(e)}")
    
    def assign_colors_from_extracted(self):
        self.color_map = {}
        
        for char, rgb in self.extracted_colors.items():
            hex_color = '#{:02x}{:02x}{:02x}'.format(rgb[0], rgb[1], rgb[2])
            self.color_map[char] = hex_color
    
    def open_live_update_window(self):
        if not self.iteration_live_update:
            messagebox.showwarning("Warning", "Belum ada data iterasi. Solve terlebih dahulu")
            return
        
        LiveUpdateWindow(self, self.last_method, self.iteration_live_update, self.solver.solution is not None)
    
    def enable_solve_buttons(self):
        self.btn_brute.config(state=tk.NORMAL)
        self.btn_optimized.config(state=tk.NORMAL)
    
    def disable_solve_buttons(self):
        self.btn_brute.config(state=tk.DISABLED)
        self.btn_optimized.config(state=tk.DISABLED)
        self.btn_live_update.config(state=tk.DISABLED)
    
    def add_snapshot(self, iteration, config):
        self.iteration_live_update.append((iteration, list(config)))
    
    def solve_brute_force(self):
        if self.solver.board is None:
            messagebox.showwarning("Warning", "Load board terlebih dahulu")
            return
        
        self.disable_solve_buttons()
        self.lbl_status.config(text="Solving with Brute Force", fg='#FFEAA7')
        self.root.update()
        
        self.iteration_live_update = []
        self.last_method = "Brute Force"
        self.run_brute_force_with_logging()
    
    def solve_optimized(self):
        if self.solver.board is None:
            messagebox.showwarning("Warning", "Load board terlebih dahulu")
            return
        
        self.disable_solve_buttons()
        self.lbl_status.config(text="Solving with Optimized Brute Force", fg='#FFEAA7')
        self.root.update()
        
        self.iteration_live_update = []
        self.last_method = "Optimized Brute Force"
        self.run_optimized_with_logging()
    
    def run_brute_force_with_logging(self):
        all_positions = []
        for r in range(self.solver.n):
            for c in range(self.solver.n):
                all_positions.append((r, c))
        
        start_time = time.time()
        
        all_possibility = []
        self.solver.generate_all(0, [], all_positions, 0, all_possibility)
        self.solver.total_possibilities = len(all_possibility)
        self.solver.total_checked = len(all_possibility)
        
        valid_solutions = []
        iteration = 0
        
        for config in all_possibility:
            iteration += 1
            
            if iteration % 100 == 0:
                self.add_snapshot(iteration, config)
            
            if self.solver.is_valid(config):
                valid_solutions.append(config)
        
        self.solver.solution = valid_solutions[0] if valid_solutions else None
        end_time = time.time()
        self.solver.time_ms = (end_time - start_time) * 1000
        
        self.on_solve_complete("Brute Force")
    
    def run_optimized_with_logging(self):
        all_positions = []
        for r in range(self.solver.n):
            for c in range(self.solver.n):
                all_positions.append((r, c))
        
        all_possibility = []
        self.solver.generate_all(0, [], all_positions, 0, all_possibility)
        self.solver.total_possibilities = len(all_possibility)
        
        start_time = time.time()
        
        result = {'solution': None, 'total': 0}
        self.generate_and_check_with_logging(0, [], all_positions, 0, result)
        
        self.solver.solution = result['solution']
        self.solver.total_checked = result['total']
        
        end_time = time.time()
        self.solver.time_ms = (end_time - start_time) * 1000
        
        self.on_solve_complete("Optimized Brute Force")
    
    def generate_and_check_with_logging(self, queen_idx, q_positions, all_positions, start_idx, result):
        if queen_idx == self.solver.n:
            result['total'] += 1
            
            if result['total'] % 100 == 0:
                self.add_snapshot(result['total'], q_positions)
            
            if self.solver.is_valid(q_positions):
                result['solution'] = q_positions.copy()
                return True
            
            return False
        
        for i in range(start_idx, len(all_positions)):
            pos = all_positions[i]
            q_positions.append(pos)
            
            if self.generate_and_check_with_logging(queen_idx + 1, q_positions, all_positions, i + 1, result):
                return True
            
            q_positions.pop()
        
        return False
    
    def on_solve_complete(self, method):
        self.draw_board()
        self.update_info()
        self.enable_solve_buttons()
        
        self.btn_live_update.config(state=tk.NORMAL)
        
        if self.solver.solution:
            self.lbl_status.config(text=f"Solution found ({method})", fg='#4ECDC4')
            self.btn_save.config(state=tk.NORMAL)
            self.btn_save_txt.config(state=tk.NORMAL)
        else:
            self.lbl_status.config(text="No solution found.", fg='#e94560')
            self.btn_save.config(state=tk.DISABLED)
            self.btn_save_txt.config(state=tk.DISABLED)
    
    def assign_colors(self):
        if self.extracted_colors:
            self.assign_colors_from_extracted()
            return
        
        self.color_map = {}
        color_idx = 0
        
        for row in self.solver.board:
            for char in row:
                if char not in self.color_map:
                    self.color_map[char] = self.color_palette[color_idx % len(self.color_palette)]
                    color_idx += 1
    
    # Menggambar board dan queen ke canvas utama
    def draw_board(self):
        self.canvas.delete("all")
        
        if self.solver.board is None:
            return
        
        cell_size = self.canvas_size // self.solver.n
        offset = (self.canvas_size - cell_size * self.solver.n) // 2
        
        q_positions = set(self.solver.solution) if self.solver.solution else set()
        
        for r in range(self.solver.n):
            for c in range(self.solver.n):
                x1 = offset + c * cell_size
                y1 = offset + r * cell_size
                x2 = x1 + cell_size
                y2 = y1 + cell_size
                
                char = self.solver.board[r][c]
                color = self.color_map.get(char, 'lightgray')
                
                self.canvas.create_rectangle(x1, y1, x2, y2, 
                                              fill=color, outline='#1a1a2e', width=2)
                
                if (r, c) in q_positions:
                    padding = cell_size // 6
                    self.canvas.create_oval(x1 + padding, y1 + padding,
                                            x2 - padding, y2 - padding,
                                            fill='white', outline='#1a1a2e', width=2)
                    font_size = max(12, cell_size // 2)
                    self.canvas.create_text((x1 + x2) // 2, (y1 + y2) // 2,
                                            text="Q", font=("Arial", font_size),
                                            fill='#1a1a2e')
    
    def draw_board_with_config(self, config):
        self.canvas.delete("all")
        
        if self.solver.board is None:
            return
        
        cell_size = self.canvas_size // self.solver.n
        offset = (self.canvas_size - cell_size * self.solver.n) // 2
        
        q_positions = set(config)
        
        for r in range(self.solver.n):
            for c in range(self.solver.n):
                x1 = offset + c * cell_size
                y1 = offset + r * cell_size
                x2 = x1 + cell_size
                y2 = y1 + cell_size
                
                char = self.solver.board[r][c]
                color = self.color_map.get(char, 'lightgray')
                
                self.canvas.create_rectangle(x1, y1, x2, y2, 
                                              fill=color, outline='#1a1a2e', width=2)
                
                if (r, c) in q_positions:
                    padding = cell_size // 6
                    self.canvas.create_oval(x1 + padding, y1 + padding,
                                            x2 - padding, y2 - padding,
                                            fill='white', outline='#1a1a2e', width=2)
                    font_size = max(12, cell_size // 2)
                    self.canvas.create_text((x1 + x2) // 2, (y1 + y2) // 2,
                                            text="Q", font=("Arial", font_size),
                                            fill='#1a1a2e')
    
    def update_info(self):
        if self.solver.board:
            self.lbl_board_size_info.config(text=f"Board Size: {self.solver.n} x {self.solver.n}")
        else:
            self.lbl_board_size_info.config(text="Board Size: -")
        
        if self.solver.time_ms > 0:
            self.lbl_time.config(text=f"Time: {self.solver.time_ms:.2f} ms")
        else:
            self.lbl_time.config(text="Time: -")
        
        if self.solver.total_possibilities > 0:
            self.lbl_total_possible.config(text=f"Total Possible\nConfigurations: {self.solver.total_possibilities}")
        else:
            self.lbl_total_possible.config(text="Total Possible\nConfigurations: -")
        
        if self.solver.total_checked > 0:
            self.lbl_total_checked.config(text=f"Total Configurations\nChecked: {self.solver.total_checked}")
        else:
            self.lbl_total_checked.config(text="Total Configurations\nChecked: -")
    
    # Menyimpan solusi 
    def save_solution_image(self):
        if self.solver.solution is None:
            messagebox.showwarning("Warning", "Tidak ada solusi untuk disimpan")
            return
        
        filename = filedialog.asksaveasfilename(
            title="Save Solution as Image",
            initialfile="linkedin_queen_solution.png",
            defaultextension=".png",
            filetypes=[("PNG files", "*.png"), ("JPEG files", "*.jpg"), ("All files", "*.*")]
        )
        
        if filename:
            try:
                cell_size = 60
                padding = 20
                n = self.solver.n
                img_size = n * cell_size + 2 * padding
                
                from PIL import Image, ImageDraw, ImageFont
                img = Image.new('RGB', (img_size, img_size), color='#1a1a2e')
                draw = ImageDraw.Draw(img)
                
                q_positions = set(self.solver.solution)
                
                for r in range(n):
                    for c in range(n):
                        x1 = padding + c * cell_size
                        y1 = padding + r * cell_size
                        x2 = x1 + cell_size
                        y2 = y1 + cell_size
                        
                        char = self.solver.board[r][c]
                        color = self.color_map.get(char, '#808080')
                    
                        draw.rectangle([x1, y1, x2, y2], fill=color, outline='#1a1a2e', width=2)
                        
                        if (r, c) in q_positions:
                            circle_padding = cell_size // 6
                            draw.ellipse([x1 + circle_padding, y1 + circle_padding,
                                          x2 - circle_padding, y2 - circle_padding],
                                         fill='white', outline='#1a1a2e', width=2)
                            
                            try:
                                font = ImageFont.truetype("arial.ttf", cell_size // 2)
                            except:
                                font = ImageFont.load_default()
                            
                            text = "Q"
                            bbox = draw.textbbox((0, 0), text, font=font)
                            text_w = bbox[2] - bbox[0]
                            text_h = bbox[3] - bbox[1]
                            text_x = x1 + (cell_size - text_w) // 2
                            text_y = y1 + (cell_size - text_h) // 2 - 5
                            draw.text((text_x, text_y), text, fill='#1a1a2e', font=font)
                
                img.save(filename)
                messagebox.showinfo("Success", f"Solution saved to:\n{filename}")
                
            except Exception as e:
                import traceback
                traceback.print_exc()
                messagebox.showerror("Error", f"Failed to save image:\n{str(e)}")
    
    def save_solution_txt(self):
        if self.solver.solution is None:
            messagebox.showwarning("Warning", "Tidak ada solusi untuk disimpan")
            return
        
        filename = filedialog.asksaveasfilename(
            title="Save Solution as Text",
            initialfile="linkedin_queen_solution.txt",
            defaultextension=".txt",
            filetypes=[("Text files", "*.txt"), ("All files", "*.*")]
        )
        
        if filename:
            try:
                q_positions = set(self.solver.solution)
                n = self.solver.n
                
                with open(filename, 'w') as f:
                    for r in range(n):
                        line = ""
                        for c in range(n):
                            if (r, c) in q_positions:
                                line += "#"
                            else:
                                line += self.solver.board[r][c]
                        f.write(line + "\n")
                
                messagebox.showinfo("Success", f"Solution saved to:\n{filename}")
                
            except Exception as e:
                messagebox.showerror("Error", f"Failed to save text:\n{str(e)}")

if __name__ == "__main__":
    root = tk.Tk()
    app = LinkedinQueenGUI(root)
    root.mainloop()
