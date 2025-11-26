import streamlit as st
import yt_dlp
import os
import shutil
import time

# --- Konfigurasi Halaman ---
st.set_page_config(page_title="Sehade Downloader - No Watermark", page_icon="⬇️")

st.title("⬇️ Sehade Downloader")
st.markdown("""
### ✨ Download Video HD & **Tanpa Watermark**
Support: TikTok, Instagram, Facebook, YouTube Shorts
""")

# --- Fungsi Download ---
def download_video(url, format_choice):
    # Bersihkan folder download
    if os.path.exists("downloads"):
        shutil.rmtree("downloads")
    os.makedirs("downloads")
    
    # Mapping pilihan kualitas
    format_string = 'best' 
    
    if format_choice == "Kualitas Terbaik (Max/4K)":
        format_string = 'bestvideo+bestaudio/best'
    elif format_choice == "Full HD (1080p)":
        format_string = 'bestvideo[height<=1080]+bestaudio/best[height<=1080]'
    elif format_choice == "HD (720p)":
        format_string = 'bestvideo[height<=720]+bestaudio/best[height<=720]'
    elif format_choice == "Hemat Data (480p/360p)":
        format_string = 'worstvideo+bestaudio/worst'
    elif format_choice == "Audio Saja (MP3)":
        format_string = 'bestaudio/best'

    # --- KONFIGURASI PENTING (UPDATE) ---
    ydl_opts = {
        'format': format_string,
        'outtmpl': 'downloads/%(title)s.%(ext)s',
        'noplaylist': True,
        'quiet': True,
        'no_warnings': True,
        # TRICK 1: Gunakan User Agent samaran
        'user_agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
        # TRICK 2: Memaksa menggunakan Client Android (Lolos blokir Shorts)
        'extractor_args': {
            'youtube': {
                'player_client': ['android', 'web'],
                'skip': ['dash', 'hls']
            }
        }
    }
    
    if format_choice == "Audio Saja (MP3)":
        ydl_opts['postprocessors'] = [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
            'preferredquality': '192',
        }]
        ydl_opts['outtmpl'] = 'downloads/%(title)s.%(ext)s'

    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=True)
            
            files = os.listdir("downloads")
            if files:
                file_path = os.path.join("downloads", files[0])
                return file_path, info.get('title', 'video')
            return None, "File tidak ditemukan."
            
    except Exception as e:
        # Menampilkan pesan error spesifik jika gagal
        return None, str(e)

# --- UI ---
st.markdown("---")
col1, col2 = st.columns([3, 1])

with col1:
    url = st.text_input("🔗 Tempel Link Video:", placeholder="https://youtube.com/shorts/...")

with col2:
    quality = st.selectbox(
        "⚙️ Pilihan:",
        ("Kualitas Terbaik (Max/4K)", "Full HD (1080p)", "HD (720p)", "Hemat Data", "Audio Saja (MP3)")
    )

if st.button("🚀 Download Tanpa Watermark"):
    if url:
        status_text = st.empty()
        status_text.info("🔄 Sedang memproses... (YouTube Shorts butuh waktu ekstra)")
        
        file_path, result = download_video(url, quality)

        if file_path and os.path.exists(file_path):
            status_text.success("✅ Berhasil!")
            st.caption(f"Judul: {result}")
            
            mime_type = "audio/mpeg" if quality == "Audio Saja (MP3)" else "video/mp4"
            with open(file_path, "rb") as file:
                st.download_button(
                    label="⬇️ Simpan ke Perangkat",
                    data=file,
                    file_name=os.path.basename(file_path),
                    mime=mime_type,
                    type="primary"
                )
        else:
            # Tampilkan error agar tahu kenapa gagal
            status_text.error(f"❌ Gagal: {result}")
            if "Sign in" in str(result) or "403" in str(result):
                st.warning("⚠️ YouTube memblokir IP server ini. Coba lagi nanti atau gunakan link TikTok/IG.")
    else:
        st.warning("⚠️ Masukkan link dulu.")
