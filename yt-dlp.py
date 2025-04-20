import tkinter as tk
from tkinter import ttk, messagebox
import subprocess
import threading

class YTDLPGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Descargador de YouTube")
        self.root.geometry("600x450")
        
        # Configuración del estilo
        self.style = ttk.Style()
        self.style.theme_use('clam')
        
        # Frame principal
        self.main_frame = ttk.Frame(root, padding="15")
        self.main_frame.pack(fill=tk.BOTH, expand=True)
        
        # URL Entry
        ttk.Label(self.main_frame, text="URL del video:").pack(pady=(0, 5))
        self.url_entry = ttk.Entry(self.main_frame, width=60)
        self.url_entry.pack(pady=(0, 10))
        
        # Tipo de descarga
        ttk.Label(self.main_frame, text="Tipo de descarga:").pack(pady=(0, 5))
        self.download_type = tk.StringVar(value="video")
        ttk.Radiobutton(self.main_frame, text="Video", variable=self.download_type, value="video").pack()
        ttk.Radiobutton(self.main_frame, text="Audio", variable=self.download_type, value="audio").pack()
        
        # Frame para opciones de video
        self.video_options_frame = ttk.LabelFrame(self.main_frame, text="Opciones de Video", padding=(10, 5))
        
        # Calidad de video
        ttk.Label(self.video_options_frame, text="Calidad:").pack(pady=(0, 5))
        self.video_quality = ttk.Combobox(self.video_options_frame, 
                                        values=["Mejor calidad", "2160p (4K)", "1440p (2K)", "1080p", "720p", "480p", "360p", "Peor calidad"],
                                        state="readonly")
        self.video_quality.set("Mejor calidad")
        self.video_quality.pack(pady=(0, 10))
        
        # Formato de video
        ttk.Label(self.video_options_frame, text="Formato:").pack(pady=(0, 5))
        self.video_format = ttk.Combobox(self.video_options_frame, 
                                       values=["MP4", "MKV", "WebM"],
                                       state="readonly")
        self.video_format.set("MP4")
        self.video_format.pack()
        
        self.video_options_frame.pack(fill=tk.X, pady=10)
        
        # Frame para opciones de audio
        self.audio_options_frame = ttk.LabelFrame(self.main_frame, text="Opciones de Audio", padding=(10, 5))
        
        # Calidad de audio
        ttk.Label(self.audio_options_frame, text="Calidad:").pack(pady=(0, 5))
        self.audio_quality = ttk.Combobox(self.audio_options_frame, 
                                        values=["Mejor calidad", "320kbps", "256kbps", "192kbps", "160kbps", "128kbps", "96kbps", "Peor calidad"],
                                        state="readonly")
        self.audio_quality.set("Mejor calidad")
        self.audio_quality.pack(pady=(0, 10))
        
        # Formato de audio
        ttk.Label(self.audio_options_frame, text="Formato:").pack(pady=(0, 5))
        self.audio_format = ttk.Combobox(self.audio_options_frame, 
                                       values=["MP3", "AAC", "M4A", "OPUS", "WAV", "FLAC"],
                                       state="readonly")
        self.audio_format.set("MP3")
        self.audio_format.pack()
        
        self.audio_options_frame.pack(fill=tk.X, pady=10)
        
        # Botón de descarga
        self.download_btn = ttk.Button(self.main_frame, text="Descargar", command=self.start_download)
        self.download_btn.pack(pady=15)
        
        # Consola de salida
        output_frame = ttk.LabelFrame(self.main_frame, text="Salida", padding=(10, 5))
        self.output_text = tk.Text(output_frame, height=10, state=tk.DISABLED)
        scrollbar = ttk.Scrollbar(output_frame, command=self.output_text.yview)
        self.output_text.configure(yscrollcommand=scrollbar.set)
        
        self.output_text.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        output_frame.pack(fill=tk.BOTH, expand=True)
        
        # Actualizar opciones según tipo de descarga
        self.download_type.trace_add('write', self.update_options)
        self.update_options()
    
    def update_options(self, *args):
        if self.download_type.get() == "video":
            self.video_options_frame.pack(fill=tk.X, pady=10)
            self.audio_options_frame.pack_forget()
        else:
            self.audio_options_frame.pack(fill=tk.X, pady=10)
            self.video_options_frame.pack_forget()
    
    def start_download(self):
        url = self.url_entry.get()
        if not url:
            messagebox.showerror("Error", "Por favor ingresa una URL")
            return
        
        download_type = self.download_type.get()
        thread = threading.Thread(target=self.download, args=(url, download_type), daemon=True)
        thread.start()
    
    def download(self, url, download_type):
        self.append_output(f"Iniciando descarga de {url}...\n")
        self.download_btn.config(state=tk.DISABLED)
        
        try:
            cmd = ["yt-dlp", "--newline"]
            
            if download_type == "audio":
                # Configuración para audio
                format_map = {
                    "MP3": "mp3",
                    "AAC": "aac",
                    "M4A": "m4a",
                    "OPUS": "opus",
                    "WAV": "wav",
                    "FLAC": "flac"
                }
                audio_format = format_map[self.audio_format.get()]
                
                cmd.extend(["-x", "--audio-format", audio_format])
                
                quality = self.audio_quality.get()
                if quality == "320kbps":
                    cmd.extend(["--audio-quality", "320K"])
                elif quality == "256kbps":
                    cmd.extend(["--audio-quality", "256K"])
                elif quality == "192kbps":
                    cmd.extend(["--audio-quality", "192K"])
                elif quality == "160kbps":
                    cmd.extend(["--audio-quality", "160K"])
                elif quality == "128kbps":
                    cmd.extend(["--audio-quality", "128K"])
                elif quality == "96kbps":
                    cmd.extend(["--audio-quality", "96K"])
                elif quality == "Peor calidad":
                    cmd.extend(["--audio-quality", "0"])
            
            else:  # video
                # Configuración para video
                format_map = {
                    "MP4": "mp4",
                    "MKV": "mkv",
                    "WebM": "webm"
                }
                video_format = format_map[self.video_format.get()]
                
                cmd.extend(["--merge-output-format", video_format])
                
                quality = self.video_quality.get()
                if quality == "2160p (4K)":
                    cmd.extend(["-f", "bestvideo[height<=2160]+bestaudio/best[height<=2160]"])
                elif quality == "1440p (2K)":
                    cmd.extend(["-f", "bestvideo[height<=1440]+bestaudio/best[height<=1440]"])
                elif quality == "1080p":
                    cmd.extend(["-f", "bestvideo[height<=1080]+bestaudio/best[height<=1080]"])
                elif quality == "720p":
                    cmd.extend(["-f", "bestvideo[height<=720]+bestaudio/best[height<=720]"])
                elif quality == "480p":
                    cmd.extend(["-f", "bestvideo[height<=480]+bestaudio/best[height<=480]"])
                elif quality == "360p":
                    cmd.extend(["-f", "bestvideo[height<=360]+bestaudio/best[height<=360]"])
                elif quality == "Peor calidad":
                    cmd.extend(["-f", "worstvideo+worstaudio/worst"])
            
            cmd.extend(["--progress", "--no-simulate"])
            cmd.append(url)
            
            self.append_output("Comando ejecutado: " + " ".join(cmd) + "\n")
            
            process = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, 
                                     universal_newlines=True, bufsize=1)
            
            for line in process.stdout:
                self.append_output(line)
            
            process.wait()
            
            if process.returncode == 0:
                self.append_output("\n✅ Descarga completada con éxito!\n")
            else:
                self.append_output("\n❌ Error en la descarga\n")
        
        except Exception as e:
            self.append_output(f"\n❌ Error: {str(e)}\n")
        finally:
            self.download_btn.config(state=tk.NORMAL)
    
    def append_output(self, text):
        self.output_text.config(state=tk.NORMAL)
        self.output_text.insert(tk.END, text)
        self.output_text.see(tk.END)
        self.output_text.config(state=tk.DISABLED)
        self.root.update()

if __name__ == "__main__":
    root = tk.Tk()
    app = YTDLPGUI(root)
    root.mainloop()