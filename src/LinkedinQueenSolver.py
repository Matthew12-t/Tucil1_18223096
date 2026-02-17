import time
import os

class LinkedinQueenSolver:    
    def __init__(self):
        self.board = None
        self.n = 0
        self.solution = None
        self.total_possibilities = 0  
        self.total_checked = 0
        self.time_ms = 0
        self.error_message = None  
    
    def read_board(self, filename):
        self.error_message = None 
        board = []

        with open(filename, "r") as file:
            for row in file:
                row = row.strip()
                if row:
                    board.append(list(row))

        n = len(board)
        for row in board:
            if len(row) != n:
                self.error_message = "input tidak valid, ukuran board bukan n x n"
                return None

        colors = set()
        for row in board:
            for col in row:
                colors.add(col)
        
        if len(colors) != n:
            self.error_message = "input tidak valid, warna melebihi jumlah n"
            return None

        self.board = board
        self.n = n
        return board

    def is_valid(self, q_positions):
        n = len(q_positions)

        # Cek baris unik
        rows = [pos[0] for pos in q_positions]
        if len(set(rows)) != n:
            return False

        # Cek kolom unik
        cols = [pos[1] for pos in q_positions]
        if len(set(cols)) != n:
            return False

        # Cek warna unik
        used_colors = set()
        for row, col in q_positions:
            color = self.board[row][col]
            if color in used_colors:
                return False
            used_colors.add(color)
        
        # Cek tidak ada queen yang bersebelahan 
        for i in range(n):
            for j in range(i + 1, n):
                row_i, col_i = q_positions[i]
                row_j, col_j = q_positions[j]
                if abs(row_i - row_j) <= 1 and abs(col_i - col_j) <= 1:
                    return False

        return True

    # Generate semua kemungkinan 
    def generate_all(self, queen_idx, q_positions, all_positions, start_idx, all_possibility):
        if queen_idx == self.n:
            all_possibility.append(q_positions.copy())
            return
        
        for i in range(start_idx, len(all_positions)):
            pos = all_positions[i]
            q_positions.append(pos)
            self.generate_all(queen_idx + 1, q_positions, all_positions, i + 1, all_possibility)
            q_positions.pop()
            
    # Validasi
    def validate_all(self, all_configs):
        valid_solutions = []
        iteration = 0
        
        for config in all_configs:
            iteration += 1
            
            if iteration % 100 == 0:
                print(f"==== Iterasi ke-{iteration} ====")
                self.print_board_with_queens(config)
            
            if self.is_valid(config):
                valid_solutions.append(config)
        
        return valid_solutions
    
    # Generate dan Cek
    def generate_and_check(self, queen_idx, q_positions, all_positions, start_idx, result):
        if queen_idx == self.n:
            result['total'] += 1
            
            if result['total'] % 100 == 0:
                print(f"==== Iterasi ke-{result['total']} ===")
                self.print_board_with_queens(q_positions)
            
            if self.is_valid(q_positions):
                result['solution'] = q_positions.copy()
                return True  
            
            return False  
        
        for i in range(start_idx, len(all_positions)):
            pos = all_positions[i]
            q_positions.append(pos)
            
            if self.generate_and_check(queen_idx + 1, q_positions, all_positions, i + 1, result):
                return True  
            
            q_positions.pop()
        
        return False
    
    def print_board_with_queens(self, q_positions):
        queen_positions = set(q_positions)
        for row in range(self.n):
            line_output = ""
            for col in range(self.n):
                if (row, col) in queen_positions:
                    line_output += "# "
                else:
                    line_output += self.board[row][col] + " "
            print(line_output)

    # brute force
    def brute_force(self):
        all_positions = []
        for r in range(self.n):
            for c in range(self.n):
                all_positions.append((r, c))

        start_time = time.time()
        all_possibility = []
        self.generate_all(0, [], all_positions, 0, all_possibility)
        self.total_possibilities = len(all_possibility)  
        self.total_checked = len(all_possibility)
        valid_solutions = self.validate_all(all_possibility)
        self.solution = valid_solutions[0] if valid_solutions else None
        end_time = time.time()
        self.time_ms = (end_time - start_time) * 1000

        return self.solution, self.total_checked, self.time_ms

    # Optimized brute force
    def optimized_brute_force(self):     
        all_positions = []
        for r in range(self.n):
            for c in range(self.n):
                all_positions.append((r, c))

        all_possibility = []
        self.generate_all(0, [], all_positions, 0, all_possibility)
        self.total_possibilities = len(all_possibility)
        start_time = time.time() 
        result = {'solution': None, 'total': 0} 
        self.generate_and_check(0, [], all_positions, 0, result)
        self.solution = result['solution']
        self.total_checked = result['total']
        end_time = time.time()
        self.time_ms = (end_time - start_time) * 1000

        return self.solution, self.total_checked, self.time_ms

    def print_solution(self):
        if self.solution is None:
            print("Tidak ada solusi.")
            return
        
        queen_positions = set(self.solution)

        for row in range(self.n):
            line_output = ""
            for col in range(self.n):
                if (row, col) in queen_positions:
                    line_output += "#"
                else:
                    line_output += self.board[row][col]
            print(line_output)

if __name__ == "__main__":
    solver = LinkedinQueenSolver()
    
    filename = input("Masukkan nama file (.txt): ")
    
    if not os.path.exists(filename):
        test_path = os.path.join(os.path.dirname(__file__), "..", "test", filename)
        if os.path.exists(test_path):
            filename = test_path
    
    result = solver.read_board(filename)
    
    if result is None:
        print(solver.error_message)
        exit()
    
    print("\nPilih metode:")
    print("1. Brute Force (generate semua - validasi semua)")
    print("2. Optimized Brute Force (generate 1 - validasi - stop kalau ketemu)")
    pilihan = input("Masukkan pilihan (1/2): ")
    
    if pilihan == "2":
        print("\nMenggunakan Optimized Brute Force")
        solution, total_checked, time_ms = solver.optimized_brute_force()
    else:
        print("\nMenggunakan Brute Force")
        solution, total_checked, time_ms = solver.brute_force()
    
    if solution:
        print("\nSolusi ditemukan:\n")
        solver.print_solution()
    else:
        print("\nTidak ada solusi.")
    
    print(f"\nUkuran papan: {solver.n} x {solver.n}")
    print(f"Waktu pencarian: {round(time_ms, 2)} ms")
    print(f"Banyak kemungkinan: {solver.total_possibilities} kasus")
    print(f"Banyak kasus yang ditinjau: {solver.total_checked} kasus")