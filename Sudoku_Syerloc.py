import streamlit as st
import random
import base64

# --- LOGIKA SUDOKU (Tetap Sama) ---
def apakah_sah(papan, baris, kolom, angka):
    for i in range(9):
        if papan[baris][i] == angka or papan[i][kolom] == angka: return False
    awal_b, awal_k = (baris // 3) * 3, (kolom // 3) * 3
    for i in range(3):
        for j in range(3):
            if papan[awal_b + i][awal_k + j] == angka: return False
    return True

def selesaikan(papan):
    for b in range(9):
        for k in range(9):
            if papan[b][k] == 0:
                angka_acak = list(range(1, 10))
                random.shuffle(angka_acak)
                for angka in angka_acak:
                    if apakah_sah(papan, b, k, angka):
                        papan[b][k] = angka
                        if selesaikan(papan): return True
                        papan[b][k] = 0
                return False
    return True

def buat_soal(papan_penuh, level):
    diff = {"Mudah": 35, "Normal": 45, "Sulit": 54, "Sangat Sulit": 60}
    soal = [baris[:] for baris in papan_penuh]
    count = 0
    while count < diff[level]:
        b, k = random.randint(0, 8), random.randint(0, 8)
        if soal[b][k] != 0:
            soal[b][k] = 0
            count += 1
    return soal

def render_tabel_html(papan, is_jawaban=False):
    tabel_html = "<table style='border: 2px solid black; border-collapse: collapse; margin: 10px auto; background: white;'>"
    for r in range(9):
        tabel_html += "<tr>"
        for c in range(9):
            val = papan[r][c] if papan[r][c] != 0 else ""
            style = "border: 1px solid black; width: 30px; height: 30px; text-align: center; font-size: 18px; font-family: Arial; color: black;"
            if val != "" and not is_jawaban: style += "background-color: #f2f2f2; font-weight: bold;"
            if (c + 1) % 3 == 0 and c != 8: style += "border-right: 3px solid black;"
            if (r + 1) % 3 == 0 and r != 8: style += "border-bottom: 3px solid black;"
            tabel_html += f"<td style='{style}'>{val}</td>"
        tabel_html += "</tr>"
    tabel_html += "</table>"
    return tabel_html

# --- UI STREAMLIT ---
st.set_page_config(page_title="Sudoku Sherlock", layout="centered")
st.title("🧩 Sudoku Sherlock")

with st.sidebar:
    st.header("⚙️ Pengaturan")
    level = st.selectbox("Pilih Level:", ["Mudah", "Normal", "Sulit", "Sangat Sulit"])
    jumlah = st.slider("Jumlah Puzzle:", 2, 6, 6)
    generate = st.button("🔄 Buat Puzzle Baru")

if 'data' not in st.session_state or generate:
    st.session_state.data = []
    for _ in range(jumlah):
        p_dasar = [[0 for _ in range(9)] for _ in range(9)]
        selesaikan(p_dasar)
        jawaban = [b[:] for b in p_dasar]
        soal = buat_soal(jawaban, level)
        st.session_state.data.append({'soal': soal, 'jawaban': jawaban})

# --- PROSES MEMBUAT HALAMAN CETAK KHUSUS ---
html_cetak = f"""
<html>
<head>
    <title>Cetak Sudoku</title>
    <style>
        body {{ font-family: Arial; text-align: center; }}
        .grid {{ display: grid; grid-template-columns: repeat(2, 1fr); gap: 10px; }}
        .page-break {{ page-break-before: always; }}
        @media print {{ .no-print {{ display: none; }} }}
    </style>
</head>
<body onload="window.print()">
    <button class="no-print" onclick="window.print()" style="padding:15px; margin:20px; background:#27ae60; color:white; border:none; border-radius:5px;">KLIK CETAK / SIMPAN PDF</button>
    <h2>HALAMAN SOAL - {level.upper()}</h2>
    <div class="grid">
"""
for i, d in enumerate(st.session_state.data):
    html_cetak += f"<div><h4>Puzzle #{i+1}</h4>{render_tabel_html(d['soal'])}</div>"

html_cetak += "</div><div class='page-break'></div><h2>KUNCI JAWABAN</h2><div class='grid'>"
for i, d in enumerate(st.session_state.data):
    html_cetak += f"<div><h4>Jawaban #{i+1}</h4>{render_tabel_html(d['jawaban'], True)}</div>"
html_cetak += "</div></body></html>"

# Tombol untuk membuka halaman cetak di TAB BARU
b64 = base64.b64encode(html_cetak.encode()).decode()
href = f'<a href="data:text/html;base64,{b64}" target="_blank" style="text-decoration: none;"><button style="width:100%; padding:15px; background-color:#e67e22; color:white; border:none; border-radius:10px; font-weight:bold; cursor:pointer;">🚀 BUKA HALAMAN SIAP CETAK (TAB BARU)</button></a>'

st.markdown(href, unsafe_allow_html=True)
st.info("Setelah klik tombol oranye di atas, tab baru akan terbuka. Tekan Ctrl+P (Laptop) atau gunakan menu Share > Print (HP) di tab baru tersebut.")

# Tampilan Preview di Website
st.write("---")
st.subheader("Preview Papan:")
cols = st.columns(2)
for i, d in enumerate(st.session_state.data):
    with cols[i % 2]:
        st.markdown(f"<div style='text-align:center;'>{render_tabel_html(d['soal'])}</div>", unsafe_allow_html=True)
