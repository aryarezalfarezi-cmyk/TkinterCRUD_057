
import tkinter as tk
from tkinter import ttk, messagebox
import sqlite3

# =========================
# 1. DATABASE SQLITE
# =========================
koneksi = sqlite3.connect("nilai_siswa.db")
cursor = koneksi.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS nilai_siswa (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    nama_siswa TEXT NOT NULL,
    biologi REAL NOT NULL,
    fisika REAL NOT NULL,
    inggris REAL NOT NULL,
    prediksi_fakultas TEXT NOT NULL
)
""")

koneksi.commit()
koneksi.close()


# =========================
# 2. FUNGSI PREDIKSI
# =========================
def prediksi_fakultas(biologi, fisika, inggris):
    nilai_tertinggi = max(biologi, fisika, inggris)

    # Jika ada nilai tertinggi yang sama
    jumlah_tertinggi = [
        nilai for nilai in (biologi, fisika, inggris)
        if nilai == nilai_tertinggi
    ]

    if len(jumlah_tertinggi) > 1:
        return "Seri - Perlu Peninjauan"

    if biologi == nilai_tertinggi:
        return "Kedokteran"
    elif fisika == nilai_tertinggi:
        return "Teknik"
    else:
        return "Bahasa"


# =========================
# 3. MENAMPILKAN DATA
# =========================
def tampilkan_data():
    for item in tabel.get_children():
        tabel.delete(item)

    koneksi = sqlite3.connect("nilai_siswa.db")
    cursor = koneksi.cursor()

    cursor.execute("""
        SELECT nama_siswa, biologi, fisika, inggris,
               prediksi_fakultas
        FROM nilai_siswa
        ORDER BY id DESC
    """)

    data = cursor.fetchall()
    koneksi.close()

    for baris in data:
        tabel.insert("", tk.END, values=baris)


# =========================
# 4. FUNGSI SUBMIT
# =========================
def submit_nilai():
    nama = entry_nama.get().strip()

    if not nama:
        messagebox.showwarning(
            "Peringatan", "Nama siswa wajib diisi!"
        )
        entry_nama.focus_set()
        return

    try:
        biologi = float(entry_biologi.get())
        fisika = float(entry_fisika.get())
        inggris = float(entry_inggris.get())
    except ValueError:
        messagebox.showerror(
            "Input Tidak Valid",
            "Semua nilai harus diisi dengan angka."
        )
        return

    if any(
        nilai < 0 or nilai > 100
        for nilai in (biologi, fisika, inggris)
    ):
        messagebox.showerror(
            "Nilai Tidak Valid",
            "Nilai harus berada di antara 0 sampai 100."
        )
        return

    hasil = prediksi_fakultas(
        biologi, fisika, inggris
    )

    # Simpan ke SQLite
    koneksi = sqlite3.connect("nilai_siswa.db")
    cursor = koneksi.cursor()

    cursor.execute("""
        INSERT INTO nilai_siswa
        (nama_siswa, biologi, fisika, inggris,
         prediksi_fakultas)
        VALUES (?, ?, ?, ?, ?)
    """, (nama, biologi, fisika, inggris, hasil))

    koneksi.commit()
    koneksi.close()

    # Tampilkan hasil
    label_hasil.config(
        text=f"Hasil Prediksi: {hasil}"
    )

    messagebox.showinfo(
        "Berhasil",
        f"Data {nama} berhasil disimpan!\n"
        f"Prediksi fakultas: {hasil}"
    )

    # Perbarui tabel dan kosongkan input
    tampilkan_data()

    entry_nama.delete(0, tk.END)
    entry_biologi.delete(0, tk.END)
    entry_fisika.delete(0, tk.END)
    entry_inggris.delete(0, tk.END)
    entry_nama.focus_set()


# =========================
# 5. GUI TKINTER
# =========================
root = tk.Tk()
root.title("Aplikasi Prediksi Fakultas")
root.geometry("850x700")
root.configure(bg="#244fbd")

judul = tk.Label(
    root,
    text="APLIKASI PREDIKSI FAKULTAS",
    font=("Arial", 18, "bold"),
    bg="#244fbd",
    fg="white"
)
judul.pack(pady=15)

frame_input = tk.Frame(
    root, bg="#244fbd"
)
frame_input.pack(padx=20, pady=5)

# Input nama siswa
tk.Label(
    frame_input, text="Nama Siswa:",
    font=("Arial", 11),
    bg="#244fbd", fg="white"
).grid(row=0, column=0, sticky="w", padx=10, pady=7)

entry_nama = tk.Entry(
    frame_input, font=("Arial", 11), width=30
)
entry_nama.grid(row=0, column=1, padx=10, pady=7)

# Input nilai Biologi
tk.Label(
    frame_input, text="Nilai Biologi:",
    font=("Arial", 11),
    bg="#244fbd", fg="white"
).grid(row=1, column=0, sticky="w", padx=10, pady=7)

entry_biologi = tk.Entry(
    frame_input, font=("Arial", 11), width=30
)
entry_biologi.grid(row=1, column=1, padx=10, pady=7)

# Input nilai Fisika
tk.Label(
    frame_input, text="Nilai Fisika:",
    font=("Arial", 11),
    bg="#244fbd", fg="white"
).grid(row=2, column=0, sticky="w", padx=10, pady=7)

entry_fisika = tk.Entry(
    frame_input, font=("Arial", 11), width=30
)
entry_fisika.grid(row=2, column=1, padx=10, pady=7)

# Input nilai Inggris
tk.Label(
    frame_input, text="Nilai Inggris:",
    font=("Arial", 11),
    bg="#244fbd", fg="white"
).grid(row=3, column=0, sticky="w", padx=10, pady=7)

entry_inggris = tk.Entry(
    frame_input, font=("Arial", 11), width=30
)
entry_inggris.grid(row=3, column=1, padx=10, pady=7)

# Tombol submit
tombol_submit = tk.Button(
    root,
    text="SUBMIT NILAI",
    font=("Arial", 11, "bold"),
    bg="white",
    fg="#244fbd",
    padx=20,
    pady=7,
    command=submit_nilai,
    cursor="hand2"
)
tombol_submit.pack(pady=10)

# Label hasil prediksi
label_hasil = tk.Label(
    root,
    text="Hasil Prediksi: -",
    font=("Arial", 13, "bold"),
    bg="#244fbd",
    fg="white"
)
label_hasil.pack(pady=8)

# Tabel riwayat data
tk.Label(
    root,
    text="Riwayat Nilai Siswa",
    font=("Arial", 12, "bold"),
    bg="#244fbd",
    fg="white"
).pack(pady=(8, 5))

frame_tabel = tk.Frame(root)
frame_tabel.pack(
    fill="both", expand=True,
    padx=15, pady=(0, 15)
)

kolom = (
    "nama_siswa", "biologi", "fisika",
    "inggris", "prediksi_fakultas"
)

tabel = ttk.Treeview(
    frame_tabel,
    columns=kolom,
    show="headings",
    height=8
)

tabel.heading("nama_siswa", text="Nama Siswa")
tabel.heading("biologi", text="Biologi")
tabel.heading("fisika", text="Fisika")
tabel.heading("inggris", text="Inggris")
tabel.heading(
    "prediksi_fakultas", text="Prediksi Fakultas"
)

tabel.column("nama_siswa", width=150)
tabel.column("biologi", width=80, anchor="center")
tabel.column("fisika", width=80, anchor="center")
tabel.column("inggris", width=80, anchor="center")
tabel.column("prediksi_fakultas", width=200)

scrollbar = ttk.Scrollbar(
    frame_tabel,
    orient="vertical",
    command=tabel.yview
)
tabel.configure(yscrollcommand=scrollbar.set)

tabel.pack(side="left", fill="both", expand=True)
scrollbar.pack(side="right", fill="y")

# Tampilkan data lama saat aplikasi dibuka
tampilkan_data()

# Jalankan aplikasi
root.mainloop()
