import streamlit as st
import random
import base64

# --- LOGIKA SUDOKU ---
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
    tabel_html = "<table style='border: 2px solid black; border-collapse: collapse; margin: 5px auto; background: white;'>"
    for r in range(9):
        tabel_html += "<tr>"
        for c in range(9):
            val = papan[r][c] if papan[r][c] != 0 else ""
            style = "border: 1px solid black; width: 26px; height: 26px; text-align: center; font-size: 15px; font-family: Arial; color: black; padding: 0;"
            if val != "" and not is_jawaban: style += "background-color: #f2f2f2; font-weight: bold;"
            if (c + 1) % 3 == 0 and c != 8: style += "border-right: 2.5px solid black;"
            if (r + 1) % 3 == 0 and r != 8: style += "border-bottom: 2.5px solid black;"
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
        # Membuat ID Unik untuk setiap papan
        puzzle_id = f"SS-{random.randint(1000, 9999)}"
        st.session_state.data.append({'soal': soal, 'jawaban': jawaban, 'id': puzzle_id})

# --- PROSES HALAMAN CETAK ---
html_cetak = f"""
<html>
<head>
    <style>
        @page {{ size: A4; margin: 0.5cm; }}
        body {{ font-family: Arial; text-align: center; margin: 0; padding: 0; }}
        .grid {{ display: grid; grid-template-columns: repeat(2, 1fr); gap: 10px; }}
        .page-break {{ page-break-before: always; }}
        h2 {{ margin: 10px 0; font-size: 18px; color: #2c3e50; }}
        .id-label {{ font-size: 10px; color: #7f8c8d; margin-bottom: 2px; }}
        @media print {{ .no-print {{ display: none; }} }}
    </style>
</head>
<body onload="window.print()">
    <button class="no-print" onclick="window.print()" style="padding:10px; margin:20px; background:#27ae60; color:white; border:none; border-radius:5px; cursor:pointer;">CETAK SEKARANG</button>
    <h2>HALAMAN SOAL - {level.upper()}</h2>
    <div class="grid">
"""
for d in st.session_state.data:
    html_cetak += f"<div><div class='id-label'>ID: {d['id']}</div>{render_tabel_html(d['soal'])}</div>"

html_cetak += "</div><div class='page-break'></div><h2>KUNCI JAWABAN</h2><div class='grid'>"
for d in st.session_state.data:
    html_cetak += f"<div><div class='id-label'>Jawaban ID: {d['id']}</div>{render_tabel_html(d['jawaban'], True)}</div>"
html_cetak += "</div></body></html>"

b64 = base64.b64encode(html_cetak.encode()).decode()
href = f'<a href="data:text/html;base64,{b64}" target="_blank" style="text-decoration: none;"><button style="width:100%; padding:15px; background-color:#e67e22; color:white; border:none; border-radius:10px; font-weight:bold; cursor:pointer;">🚀 BUKA HALAMAN SIAP CETAK</button></a>'

st.markdown(href, unsafe_allow_html=True)

# Preview di Web
st.write("---")
cols = st.columns(2)
for i, d in enumerate(st.session_state.data):
    with cols[i % 2]:
        st.caption(f"ID: {d['id']}")
        st.markdown(render_tabel_html(d['soal']), unsafe_allow_html=True)
