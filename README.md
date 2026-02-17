# LinkedIn Queen Solver

## Author

**Nama:** Matthew Sebastian Kurniawan  
**NIM:** 18223096  
**Mata Kuliah:** IF2211 Strategi Algoritma

## Penjelasan Singkat Program

LinkedIn Queen Solver adalah program untuk menyelesaikan puzzle LinkedIn Queen Game. Program ini menggunakan dua algoritma:
1. **Brute Force** - Mencoba semua kombinasi penempatan queen C(n², n)
2. **Optimized Brute Force** - Menghasilkan konfigurasi secara bertahap (generate) dan langsung memvalidasi constraint pada setiap langkah

Program memiliki GUI interaktif berbasis Tkinter yang menampilkan:
- Board visual dengan warna-warna region
- Solusi dengan posisi queen
- Live Update untuk melihat proses iterasi algoritma
- Fitur save solution ke file gambar atau txt

## Struktur Folder

```
├── src/                          
│   ├── LinkedinQueenGUI.py       
│   └── LinkedinQueenSolver.py    
├── bin/                          
│   ├── LinkedinQueenGUI.exe      
│   └── LinkedinQueenSolver.exe   
├── test/                         
│   ├── test1.txt                
│   ├── test2.txt                
│   ├── test3.txt                 
│   ├── test4.txt                
│   ├── test5.txt                 
│   ├── test6.txt              
│   ├── test7.txt                 
│   ├── image1.png               
│   ├── image2.png               
│   └── image3.png               
├── doc/                          
│   └── Tucil_K01_18223096_Matthew Sebastian Kurniawan.pdf
├── .gitignore                    
└── README.md                     
```

## Requirements

- **Python 3.x** (direkomendasikan Python 3.8+)
- **Library yang dibutuhkan:**
  - `tkinter` 
  - `Pillow` 

### Instalasi Dependencies

```bash
pip install Pillow
```

## Cara Kompilasi

Program ini ditulis dalam Python dan tidak perlu dikompilasi

## Cara Menjalankan Program

### GUI 

**Melalui Python:**
```bash
cd src
python LinkedinQueenGUI.py
```

**Melalui Executable:**
```bash
cd bin
.\LinkedinQueenGUI.exe
```
Atau double-click file `bin/LinkedinQueenGUI.exe`

### CLI 

**Melalui Python:**
```bash
cd src
python LinkedinQueenSolver.py
```

## Cara Menggunakan Program

### GUI 

1. **Load Board via File:**
   - Klik tombol "Input File" untuk memilih file input (.txt)

2. **Load Board via Image:**
   - Klik tombol "Load Image" untuk memilih gambar board
   - Masukkan ukuran board pada field "Board Size"
   - Klik tombol "Apply" untuk mengekstrak grid dari gambar

3. **Solve Puzzle:**
   - Klik "Brute Force" untuk solve dengan algoritma brute force
   - Klik "Optimized Brute Force" untuk solve dengan algoritma brute force yang dioptimasi

4. **Live Update:**
   - Setelah solve selesai, klik "Live Update" untuk melihat snapshot iterasi
   - Gunakan tombol Prev/Next untuk navigasi antar snapshot

5. **Save Solution:**
   - Klik "Save as Image" untuk menyimpan solusi dalam format gambar (.png)
   - Klik "Save as Txt" untuk menyimpan solusi dalam format file teks (.txt)

### CLI 

1. **Run the Program:**
   - Buka Terminal atau Command Prompt
   - Masuk ke folder src 
   - Jalankan program

2. **Input Board File (txt):**
   - Masukkan nama file input (.txt)

3. **Choose Solving Method:**
   - Masukkan angka 1 untuk solve dengan algoritma brute force
   - Masukkan angka 2 untuk solve dengan algoritma brute force yang dioptimasi


### Format Input File TXT

```
AABB
AABB
CCDD
CCDD
```