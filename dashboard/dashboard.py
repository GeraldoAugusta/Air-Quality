import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st

sns.set(style="darkgrid")

# =========================
# Konfigurasi halaman
# =========================
st.set_page_config(
    page_title="Air Quality Dashboard",
    page_icon="🌫️",
    layout="wide"
)

# =========================
# Helper functions
# =========================
@st.cache_data
def load_data():
    df = pd.read_csv("dashboard/main_data.csv")
    df["date"] = pd.to_datetime(df["date"])
    df.sort_values("date", inplace=True)
    df.reset_index(drop=True, inplace=True)
    return df


def aggregate_by_period(df, period="yearly"):
    if period == "yearly":
        grouped = df.resample("Y", on="date").agg({
            "PM2.5": "mean",
            "PM10": "mean",
            "SO2": "mean",
            "NO2": "mean",
            "CO": "mean",
            "O3": "mean"
        }).reset_index()
        grouped["label"] = grouped["date"].dt.strftime("%Y")

    elif period == "monthly":
        grouped = df.resample("M", on="date").agg({
            "PM2.5": "mean",
            "PM10": "mean",
            "SO2": "mean",
            "NO2": "mean",
            "CO": "mean",
            "O3": "mean"
        }).reset_index()
        grouped["label"] = grouped["date"].dt.strftime("%Y-%m")

    else:  # daily
        grouped = df.resample("D", on="date").agg({
            "PM2.5": "mean",
            "PM10": "mean",
            "SO2": "mean",
            "NO2": "mean",
            "CO": "mean",
            "O3": "mean"
        }).reset_index()
        grouped["label"] = grouped["date"].dt.strftime("%Y-%m-%d")

    return grouped


def station_comparison(df):
    result = (
        df.groupby("station")[["PM2.5", "PM10", "SO2", "NO2", "CO", "O3"]]
        .mean()
        .reset_index()
    )
    return result


def pollutant_overview(df):
    pollutant_cols = ["PM2.5", "PM10", "SO2", "NO2", "CO", "O3"]
    available_cols = [col for col in pollutant_cols if col in df.columns]

    result = df[available_cols].mean().reset_index()
    result.columns = ["pollutant", "average_value"]
    return result


# =========================
# Load data
# =========================
all_df = load_data()

# =========================
# Sidebar
# =========================
with st.sidebar:
    st.markdown("## 🌫️ Air Quality Explorer")
    st.caption("Eksplorasi kualitas udara berdasarkan stasiun dan periode waktu.")

    st.markdown("### Filter Utama")

    station_list = sorted(all_df["station"].dropna().unique().tolist())
    station_option = st.selectbox(
        "Pilih Stasiun",
        options=["Semua Stasiun"] + station_list,
        index=0
    )

    period_option = st.radio(
        "Pilih Granularitas Waktu",
        options=["Tahunan", "Bulanan", "Harian"],
        index=0
    )

    min_date = all_df["date"].min().date()
    max_date = all_df["date"].max().date()

    start_date, end_date = st.date_input(
        "Pilih Rentang Tanggal",
        value=[min_date, max_date],
        min_value=min_date,
        max_value=max_date
    )

    st.markdown("---")
    st.markdown("### Tentang Tampilan")
    st.info(
        "Dashboard menampilkan tren untuk stasiun terpilih serta perbandingan overall antar stasiun pada rentang waktu yang sama."
    )

# =========================
# Validasi filter tanggal
# =========================
if isinstance(start_date, tuple) or isinstance(start_date, list):
    start_date, end_date = start_date[0], start_date[1]

# =========================
# Filter tanggal
# =========================
filtered_df = all_df[
    (all_df["date"].dt.date >= start_date) &
    (all_df["date"].dt.date <= end_date)
].copy()

# Filter stasiun untuk tren utama
if station_option == "Semua Stasiun":
    focus_df = filtered_df.copy()
else:
    focus_df = filtered_df[filtered_df["station"] == station_option].copy()

if filtered_df.empty or focus_df.empty:
    st.warning("Tidak ada data yang cocok dengan filter yang dipilih.")
    st.stop()

# =========================
# Mapping periode
# =========================
period_map = {
    "Tahunan": "yearly",
    "Bulanan": "monthly",
    "Harian": "daily"
}
selected_period = period_map[period_option]

trend_df = aggregate_by_period(focus_df, selected_period)
comparison_df = station_comparison(filtered_df)
pollutant_df = pollutant_overview(filtered_df)

# =========================
# Header utama
# =========================
st.title("Dashboard Analisis Kualitas Udara Beijing")
st.markdown(
    f"""
    Menampilkan tren kualitas udara untuk **{station_option}**  
    pada rentang waktu **{start_date} hingga {end_date}** dengan tampilan **{period_option.lower()}**.
    """
)

# =========================
# KPI cards
# =========================
st.subheader("Ringkasan Utama")

col1, col2, col3, col4 = st.columns(4)

with col1:
    st.metric("Rata-rata PM2.5", f"{focus_df['PM2.5'].mean():.2f}")

with col2:
    st.metric("Rata-rata PM10", f"{focus_df['PM10'].mean():.2f}")

with col3:
    st.metric("Jumlah Observasi", f"{focus_df.shape[0]:,}")

with col4:
    st.metric("Jumlah Stasiun Terlibat", f"{filtered_df['station'].nunique()}")

st.markdown("---")

# =========================
# Tren utama
# =========================
st.subheader("Tren Kualitas Udara Berdasarkan Pilihan Stasiun dan Waktu")

fig, ax = plt.subplots(figsize=(16, 6))
ax.plot(
    trend_df["label"],
    trend_df["PM2.5"],
    marker="o",
    linewidth=2,
    label="PM2.5"
)
ax.plot(
    trend_df["label"],
    trend_df["PM10"],
    marker="o",
    linewidth=2,
    label="PM10"
)
ax.set_title(f"Tren PM2.5 dan PM10 - {station_option}", fontsize=16)
ax.set_xlabel("Periode")
ax.set_ylabel("Rata-rata Konsentrasi")
ax.tick_params(axis="x", rotation=45)
ax.legend()
st.pyplot(fig)

st.caption(
    "Grafik ini menunjukkan perubahan rata-rata PM2.5 dan PM10 sesuai stasiun serta granularitas waktu yang dipilih."
)

st.markdown("---")

# =========================
# Perbandingan overall antar stasiun
# =========================
st.subheader("Perbandingan Overall Antar Stasiun pada Rentang Waktu Terpilih")

col_left, col_right = st.columns(2)

with col_left:
    compare_metric = st.selectbox(
        "Pilih Polutan untuk Dibandingkan Antar Stasiun",
        options=["PM2.5", "PM10", "SO2", "NO2", "CO", "O3"],
        index=0
    )

with col_right:
    sort_order = st.selectbox(
        "Urutan",
        options=["Tertinggi ke Terendah", "Terendah ke Tertinggi"],
        index=0
    )

ascending_flag = True if sort_order == "Terendah ke Tertinggi" else False
comparison_sorted = comparison_df.sort_values(by=compare_metric, ascending=ascending_flag)

fig, ax = plt.subplots(figsize=(14, 7))
sns.barplot(
    data=comparison_sorted,
    x=compare_metric,
    y="station",
    palette="Blues_r",
    ax=ax
)
ax.set_title(f"Perbandingan {compare_metric} Antar Stasiun", fontsize=16)
ax.set_xlabel(f"Rata-rata {compare_metric}")
ax.set_ylabel("Stasiun")
st.pyplot(fig)

st.caption(
    "Bagian ini selalu menampilkan perbandingan overall semua stasiun dalam rentang tanggal yang dipilih, meskipun pada bagian tren Anda memilih satu stasiun tertentu."
)

st.markdown("---")

# =========================
# Pola polutan & top stations
# =========================
st.subheader("Ringkasan Polutan dan Stasiun Dominan")

col1, col2 = st.columns(2)

with col1:
    fig, ax = plt.subplots(figsize=(10, 6))
    sns.barplot(
        data=pollutant_df.sort_values(by="average_value", ascending=False),
        x="average_value",
        y="pollutant",
        palette="Greys",
        ax=ax
    )
    ax.set_title("Rata-rata Konsentrasi Polutan", fontsize=15)
    ax.set_xlabel("Nilai Rata-rata")
    ax.set_ylabel(None)
    st.pyplot(fig)

with col2:
    top_station_pm25 = comparison_df.sort_values(by="PM2.5", ascending=False).head(5)

    fig, ax = plt.subplots(figsize=(10, 6))
    sns.barplot(
        data=top_station_pm25,
        x="PM2.5",
        y="station",
        palette="Reds_r",
        ax=ax
    )
    ax.set_title("Top 5 Stasiun dengan PM2.5 Tertinggi", fontsize=15)
    ax.set_xlabel("Rata-rata PM2.5")
    ax.set_ylabel(None)
    st.pyplot(fig)

st.markdown("---")

# =========================
# Tabel data
# =========================
st.subheader("Preview Data Hasil Filter")

preview_cols = [
    col for col in [
        "date", "station", "PM2.5", "PM10", "SO2", "NO2", "CO", "O3", "TEMP", "PRES", "RAIN", "wd"
    ] if col in filtered_df.columns
]

st.dataframe(filtered_df[preview_cols].head(100), use_container_width=True)

st.caption("Copyright © Proyek Analisis Data 2026")