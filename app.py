import streamlit as st
import yt_dlp
import os
import time

# --- Konfigurasi Halaman ---
st.set_page_config(page_title="Sehade Downloader", page_icon="⬇️")

st.title("⬇️ Sehade Downloader")
st.markdown("Download video dari TikTok, Instagram, YouTube Shorts, dan Facebook secara gratis.")

# --- Fungsi Download ---
def download_video(url):
    # Membuat folder temp jika belum ada
    if not os.path.exists("downloads"):
        os.makedirs("downloads")
    
    # Konfigurasi yt-dlp
    ydl_opts = {
        'format': 'best',  # Kualitas terbaik
        'outtmpl': 'downloads/%(title)s.%(ext)s', # Template nama file
        'noplaylist': True,
        # Opsi khusus untuk mengatasi beberapa proteksi sederhana
        'user_agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
    }

    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=True)
            file_path = ydl.prepare_filename(info)
            return file_path, info.get('title', 'video')
    except Exception as e:
        return None, str(e)

# --- UI Bagian Input ---
url = st.text_input("Masukkan Link Video:", placeholder="https://www.tiktok.com/@user/video/...")

if st.button("Download Video"):
    if url:
        with st.spinner("Sedang memproses video... Mohon tunggu..."):
            file_path, result = download_video(url)

            if file_path and os.path.exists(file_path):
                st.success(f"Berhasil diproses: {result}")
                
                # Membuka file untuk dibaca user
                with open(file_path, "rb") as file:
                    btn = st.download_button(
                        label="⬇️ Simpan ke Perangkat",
                        data=file,
                        file_name=os.path.basename(file_path),
                        mime="video/mp4"
                    )
                
                # (Opsional) Membersihkan file setelah beberapa saat agar server tidak penuh
                # Di Streamlit cloud, file temp akan hilang saat restart, tapi baiknya dihapus manual jika perlu
            else:
                st.error(f"Gagal mendownload. Error: {result}")
                st.info("Catatan: Pastikan link benar dan video bersifat Publik (bukan Private/Friends Only).")
    else:
        st.warning("Silakan masukkan link terlebih dahulu.")

# --- Footer ---
st.markdown("---")
st.caption("Dibuat untuk project Sehade Downloader via Streamlit & yt-dlp.")