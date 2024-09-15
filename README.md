**Implementasi Algoritma A\* untuk Menentukan Waktu Pit Stop Ideal pada
Balapan Formula 1**

Cara Mengakses Program: Anda dapat mengakses aplikasi simulasi secara
langsung dengan mengunjungi tautan berikut:
https://pitstopf1.streamlit.app/

Cara Menjalankan Aplikasi Secara Lokal: Jika Anda ingin menjalankan
aplikasi secara lokal di mesin Anda, ikuti langkah-langkah berikut:

1\. Persyaratan - Pastikan Anda telah menginstal Python versi 3.7 atau
yang lebih baru. Anda juga perlu menginstal beberapa paket Python yang
diperlukan.

2\. Unduh Source Code - Unduh file ZIP yang berisi source code aplikasi
dari repository atau tautan yang diberikan. - Ekstrak file ZIP ke dalam
folder di mesin Anda.

3\. Instalasi Paket Buka terminal atau command prompt, navigasikan ke
folder tempat Anda mengekstrak file ZIP, dan jalankan perintah berikut
untuk menginstal paket yang diperlukan:

pip install -r requirements.txt

File requirements.txt berisi daftar semua paket Python yang diperlukan
untuk menjalankan aplikasi.

4\. Menjalankan Aplikasi Setelah semua paket diinstal, jalankan aplikasi
dengan perintah berikut:

streamlit run app.py

Gantilah app.py dengan nama file Python utama Anda jika berbeda.
Aplikasi akan dibuka di browser default Anda pada alamat
http://localhost:8501.

5\. Menggunakan Aplikasi

- Pilih Sirkuit: Dari menu dropdown di sidebar, pilih sirkuit balapan
yang ingin Anda simulasikan.
- Masukkan Parameter Simulasi: Tentukan jumlah lap, kecepatan rata-rata mobil, dan tingkat keausan ban per lap.
- Jalankan Simulasi: Klik tombol \"Jalankan Simulasi\" untuk melihat hasil simulasi dengan algoritma A\*.
- Pit Stop Manual: Jika ingin menentukan pit stop manual, masukkan lap-lap di mana pit stop akan
dilakukan dan klik \"Konfirmasi Pit Stop\" untuk melihat hasilnya.

6\. Mengatasi Masalah Jika Anda mengalami masalah saat menjalankan
aplikasi, pastikan bahwa semua paket diinstal dengan benar dan versi
Python yang digunakan sesuai dengan yang direkomendasikan.
