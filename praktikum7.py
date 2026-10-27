
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

    