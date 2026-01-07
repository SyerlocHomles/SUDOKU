import streamlit as st
import random

# --- LOGIKA SUDOKU ---
def apakah_sah(papan, baris, kolom, angka):
    for i in range(9):
        if papan[baris][i] == angka or papan[i][kolom] == angka:
            return False
    awal_b, awal_k = (baris // 3) * 3, (kolom // 3) * 3
    for i in range(3):
        for j in range(3):
            if papan[awal_b + i][awal_k + j] == angka:
                return False
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

def render_tabel(papan, is_jawaban=False):
    tabel_html = "<table style='border: 2px solid black; border-collapse: collapse; margin: 0 auto; background: white;'>"
    for r in range(9):
        tabel_html += "<tr>"
        for c in range(9):
            val = papan[r][c] if papan[r][c] != 0 else ""
            style = "border: 1px solid black; width: 30px; height: 30px; text-align: center; font-size: 18px; color: black;"
            if val != "" and not is_jawaban: style += "background-color: #f0f0f0; font-weight: bold;"
            if (c + 1) % 3 == 0 and c != 8: style += "border-right: 2.5px solid black;"
            if (r + 1) % 3 == 0 and r != 8: style += "border-bottom: 2.5px solid black;"
            tabel_html += f"<td style='{style}'>{val}</td>"
        tabel_html += "</tr>"
    tabel_html += "</table>"
    return tabel_html

# --- UI STREAMLIT ---
st.set_page_config(page_title="Pabrik Sudoku", page_icon="🧩")

st.markdown("""
    <style>
    @media print {
        header, .stSidebar, button { display: none !important; }
        .main { background: white !important; }
        .page-break { page-break-before: always; }
    }
    </style>
    """, unsafe_allow_whitespace=True)

st.title("🧩 Pabrik Sudoku Pribadi")

with st.sidebar:
    st.header("⚙️ Pengaturan")
    level = st.selectbox("Pilih Level:", ["Mudah", "Normal", "Sulit", "Sangat Sulit"])
    jumlah = st.slider("Jumlah Puzzle:", 2, 10, 6, 2)
    if st.button("🔄 Generate Puzzle Baru"):
        st.session_state.data = []
        for _ in range(jumlah):
            p_dasar = [[0 for _ in range(9)] for _ in range(9)]
            selesaikan(p_dasar)
            jawaban = [b[:] for b in p_dasar]
            soal = buat_soal(jawaban, level)
            st.session_state.data.append({'soal': soal, 'jawaban': jawaban})

if 'data' in st.session_state:
    st.button("🖨️ Cetak ke PDF / Printer", on_click=lambda: st.write('<script>window.print()</script>', unsafe_allow_html=True))
    
    # Grid Soal
    st.subheader(f"Halaman Soal - Level {level}")
    cols = st.columns(2)
    for i, d in enumerate(st.session_state.data):
        with cols[i % 2]:
            st.markdown(f"<div style='text-align:center;'><h4>Puzzle #{i+1}</h4>{render_tabel(d['soal'])}</div>", unsafe_allow_html=True)
            st.write("")

    st.markdown("<div class='page-break'></div>", unsafe_allow_html=True)
    
    # Grid Jawaban
    st.subheader("Kunci Jawaban")
    cols_j = st.columns(2)
    for i, d in enumerate(st.session_state.data):
        with cols_j[i % 2]:
            st.markdown(f"<div style='text-align:center;'><h4>Jawaban #{i+1}</h4>{render_tabel(d['jawaban'], True)}</div>", unsafe_allow_html=True)
            st.write("")
