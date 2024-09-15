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
        
        if lap < total_laps:
            current_lap_data = (tire_wear, lap_time(tire_wear, lap_length_km, average_speed_kmh), pit_stops)
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

def manual_pit_strategy(total_laps, lap_length_km, average_speed_kmh, pit_stop_time, manual_pit_laps, initial_tire_wear, wear_increase_per_lap):
    time_so_far = 0
    tire_wear = initial_tire_wear
    pit_stops = 0
    lap_data = []

    for lap in range(1, total_laps + 1):
        if lap in manual_pit_laps:
            time_so_far += lap_time(tire_wear, lap_length_km, average_speed_kmh) + pit_stop_time
            tire_wear = 0  # Reset keausan ban setelah pit stop
            pit_stops += 1
        else:
            time_so_far += lap_time(tire_wear, lap_length_km, average_speed_kmh)
            tire_wear += wear_increase_per_lap

        lap_data.append((lap_time(tire_wear, lap_length_km, average_speed_kmh), pit_stops, tire_wear))

    return time_so_far, lap_data, manual_pit_laps

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
jumlah_lap = st.number_input("Jumlah Lap", min_value=1, max_value=100, value=int(sirkuit_info['lap']))
average_speed_kmh = st.number_input("Kecepatan Rata-rata (km/h)", min_value=100, max_value=400, value=325)
wear_increase_per_lap = st.number_input("Tingkat Keausan Ban per Lap (%)", min_value=1.0, max_value=10.0, value=3.5)

# Tombol untuk menjalankan simulasi
if st.button("Jalankan Simulasi"):
    best_time, pit_laps, lap_data = a_star_pit_strategy(jumlah_lap, sirkuit_info['jarak'], average_speed_kmh, wear_increase_per_lap, 22, 80)

    # Membuat DataFrame dari lap_data
    df_lap = pd.DataFrame(lap_data, columns=['Tingkat Keausan Ban (%)', 'Waktu Lap (detik)', 'Pit Stop'])
    df_lap.index += 1  # Untuk menampilkan lap mulai dari 1

    # Output waktu terbaik berdasarkan strategi pit stop
    st.write(f"Waktu total optimal dengan A* adalah: {best_time / 3600:.2f} jam ({best_time:.2f} detik)")
    st.write(f"Pit stop dilakukan pada lap: {pit_laps}")

    # Tampilkan tabel data lap
    st.write("Tabel Data Per Lap:")
    st.dataframe(df_lap)

    st.write("Masukkan lap untuk pit stop manual (maksimal 5 pit stop):")
    manual_pit_laps = []
    for i in range(5):
        pit_stop_input = st.number_input(
            f"Pit stop {i+1} (opsional):", 
            min_value=0, 
            max_value=jumlah_lap, 
            value=0, 
            key=f'pit_stop_{i+1}'
        )
        if pit_stop_input > 0:
            manual_pit_laps.append(pit_stop_input)
    
    # Strategi Manual (jika input pit stop manual diberikan)
    if manual_pit_laps:
        manual_pit_laps = sorted(set(manual_pit_laps))  # Menghapus duplikat dan mengurutkan lap
        manual_time, manual_lap_data, manual_pit_laps = manual_pit_strategy(
            jumlah_lap, sirkuit_info['jarak'], average_speed_kmh, 22, manual_pit_laps, 0, wear_increase_per_lap
        )
    
        df_manual = pd.DataFrame(manual_lap_data, columns=['Waktu Lap (detik)', 'Pit Stop', 'Tingkat Keausan Ban (%)'])
        df_manual.index += 1
    
        st.subheader("Strategi Pit Stop Manual")
        st.write(f"Waktu total dengan strategi pit stop manual adalah: {manual_time / 3600:.2f} jam ({manual_time:.2f} detik)")
        st.write(f"Pit stop dilakukan pada lap: {manual_pit_laps}")
        st.write(df_manual)
    else:
        st.write("Anda belum memasukkan lap untuk pit stop manual.")
