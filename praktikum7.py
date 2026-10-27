
import tkinter as tk
from tkinter import ttk, messagebox
import sqlite3

# =========================
# 1. DATABASE SQLITE
# =========================
koneksi = sqlite3.connect("nilai_siswa.db")
cursor = koneksi.cursor()

