
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


