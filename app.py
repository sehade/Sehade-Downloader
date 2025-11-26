import streamlit as st
import yt_dlp
import os
import shutil

# --- Konfigurasi Halaman ---
st.set_page_config(page_title="Sehade Downloader", page_icon="⬇️")

st.title("⬇️ Sehade Downloader")
st.markdown("Download video TikTok, IG, FB, & YouTube dengan pilihan kualitas HD.")

# --- Fungsi Download ---
def download_video(url, format_choice):
    # Bersihkan folder download lama agar tidak penuh
    if os.path.exists("downloads"):
        shutil.rmtree("downloads")
    os.makedirs("downloads")
    
    # Mapping pilihan user ke format yt-dlp
    format_string = 'best' # Default
    
    if format_choice == "Kualitas Terbaik (Max/4K)":
        # Download Video terbaik + Audio terbaik, lalu gabung
        format_string = 'bestvideo+bestaudio/best'
    elif format_choice == "Full HD (1080p)":
        format_string = 'bestvideo[height<=1080]+bestaudio/best[height<=1080]'
    elif format_choice == "HD (720p)":
        format_string = 'bestvideo[height<=720]+bestaudio/best[height<=720]'
    elif format_choice == "Hemat Data (480p/360p)":
        format_string = 'worstvideo+bestaudio/worst'
    elif format_choice == "Audio Saja (MP3)":
        format_string = 'bestaudio/best'

    # Konfigurasi yt-dlp
    ydl_opts = {
        'format': format_string,
        'outtmpl': 'downloads/%(title)s.%(ext)s',
        'noplaylist': True,
        'updatetime': False,
        # Fake User Agent agar tidak dideteksi bot
        'user_agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
    }
    
    # Khusus jika user memilih Audio Saja, kita convert ke MP3
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
            
            # Ambil nama file yang sudah didownload
            # Kita cari file di folder downloads karena prepare_filename kadang beda ekstensi setelah merge
            files = os.listdir("downloads")
            if files:
                file_path = os.path.join("downloads", files[0])
                return file_path, info.get('title', 'video')
            return None, "File tidak ditemukan setelah download."
            
    except Exception as e:
        return None, str(e)

# --- UI Input & Pilihan ---
col1, col2 = st.columns([3, 1])

with col1:
    url = st.text_input("Link Video:", placeholder="Tempel link TikTok/IG/YT di sini...")

with col2:
    # Dropdown Pilihan Kualitas
    quality = st.selectbox(
        "Pilih Kualitas:",
        (
            "Kualitas Terbaik (Max/4K)", 
            "Full HD (1080p)", 
            "HD (720p)", 
            "Hemat Data (480p/360p)",
            "Audio Saja (MP3)"
        )
    )

# Tombol Download
if st.button("🚀 Download Sekarang"):
    if url:
        status_text = st.empty()
        status_text.info("🔄 Sedang memproses... (Menggabungkan Video & Audio butuh waktu sedikit lama)")
        
        file_path, result = download_video(url, quality)

        if file_path and os.path.exists(file_path):
            status_text.success(f"✅ Selesai! Judul: {result}")
            
            # Tentukan MIME type
            mime_type = "audio/mpeg" if quality == "Audio Saja (MP3)" else "video/mp4"
            
            with open(file_path, "rb") as file:
                st.download_button(
                    label="⬇️ Simpan ke Galeri/PC",
                    data=file,
                    file_name=os.path.basename(file_path),
                    mime=mime_type
                )
        else:
            status_text.error(f"❌ Gagal: {result}")
    else:
        st.warning("⚠️ Masukkan link dulu bosku.")

# --- Footer ---
st.markdown("---")
st.caption("Tips: Untuk YouTube Shorts/TikTok, pilih 'Kualitas Terbaik'. Untuk Video Musik, bisa pilih 'Audio Saja'.")
