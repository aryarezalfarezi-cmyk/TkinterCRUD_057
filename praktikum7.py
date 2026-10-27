
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


