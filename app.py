import streamlit as st
import pandas as pd
import heapq
from PIL import Image

# Fungsi untuk menghitung waktu per lap berdasarkan keausan ban
def lap_time(tire_wear, lap_length_km, average_speed_kmh):
    base_lap_time = (lap_length_km / average_speed_kmh) * 3600  # dalam detik
    if tire_wear > 60:
        wear_penalty = (tire_wear - 60) * 0.01 * base_lap_time
    else:
        wear_penalty = 0
    return base_lap_time + wear_penalty

# Fungsi untuk menentukan kapan pit stop sebaiknya dilakukan
def a_star_pit_strategy(total_laps, lap_length_km, average_speed_kmh, wear_increase_per_lap, pit_stop_time, max_wear_limit):
    initial_tire_wear = 0  # Tingkat keausan ban awal (%)
    start = (0, 0, initial_tire_wear, 0, [], [])  # Start state
    pq = [(0, start)]  # Priority queue: (f_cost, state)
    visited = set()
    lap_data = []

    while pq:
        f_cost, (time_so_far, lap, tire_wear, pit_stops, pit_laps, lap_data) = heapq.heappop(pq)
        
        if lap <= total_laps:
            current_lap_data = (lap_time(tire_wear, lap_length_km, average_speed_kmh), pit_stops, tire_wear)
            lap_data.append(current_lap_data)
        
        if lap == total_laps:
            return time_so_far, pit_laps, lap_data
        
        if (lap, tire_wear, pit_stops) in visited:
            continue
        visited.add((lap, tire_wear, pit_stops))
        
        next_tire_wear = tire_wear + wear_increase_per_lap
        if next_tire_wear <= max_wear_limit:
            next_time = time_so_far + lap_time(tire_wear, lap_length_km, average_speed_kmh)
            next_state = (next_time, lap + 1, next_tire_wear, pit_stops, pit_laps, lap_data.copy())
            heapq.heappush(pq, (next_time + (total_laps - (lap + 1)) * lap_time(next_tire_wear, lap_length_km, average_speed_kmh), next_state))

        if pit_stops < 5 and tire_wear > 60:
            next_tire_wear = 0
            next_time = time_so_far + lap_time(tire_wear, lap_length_km, average_speed_kmh) + pit_stop_time
            next_state = (next_time, lap + 1, next_tire_wear, pit_stops + 1, pit_laps + [lap + 1], lap_data.copy())
            heapq.heappush(pq, (next_time + (total_laps - (lap + 1)) * lap_time(next_tire_wear, lap_length_km, average_speed_kmh), next_state))

# Membaca data sirkuit dari CSV
df_sirkuit = pd.read_csv('data_sirkuit.csv')

# Streamlit app
st.title("Simulasi Strategi Pit Stop F1")

# Pilih sirkuit
sirkuit_terpilih = st.selectbox("Pilih Sirkuit", df_sirkuit['nama'])

# Tampilkan informasi sirkuit
sirkuit_info = df_sirkuit[df_sirkuit['nama'] == sirkuit_terpilih].iloc[0]
st.write(f"Nama Sirkuit: {sirkuit_info['nama']}")
st.write(f"Jumlah Lap: {sirkuit_info['lap']}")
st.write(f"Panjang 1 Lap: {sirkuit_info['jarak']} km")

# Gambar sirkuit
image = Image.open(sirkuit_info['gambar'])
st.image(image, caption=sirkuit_info['nama'])

# Input yang bisa diubah
jumlah_lap = st.number_input("Jumlah Lap", min_value=1, max_value=100, value=int(sirkuit_info['jumlah lap']))
average_speed_kmh = st.number_input("Kecepatan Rata-rata (km/h)", min_value=100, max_value=400, value=325)
wear_increase_per_lap = st.number_input("Tingkat Keausan Ban per Lap (%)", min_value=1.0, max_value=10.0, value=3.5)

# Tombol untuk menjalankan simulasi
if st.button("Jalankan Simulasi"):
    best_time, pit_laps, lap_data = a_star_pit_strategy(jumlah_lap, sirkuit_info['jarak'], average_speed_kmh, wear_increase_per_lap, 22, 80)

    # Membuat DataFrame dari lap_data
    df_lap = pd.DataFrame(lap_data, columns=['Waktu Lap (detik)', 'Pit Stop', 'Tingkat Keausan Ban (%)'])
    df_lap.index += 1  # Untuk menampilkan lap mulai dari 1

    # Output waktu terbaik berdasarkan strategi pit stop
    st.write(f"Waktu total optimal dengan A* adalah: {best_time / 3600:.2f} jam ({best_time:.2f} detik)")
    st.write(f"Pit stop dilakukan pada lap: {pit_laps}")

    # Tampilkan tabel data lap
    st.write("Tabel Data Per Lap:")
    st.dataframe(df_lap)
