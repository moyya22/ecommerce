import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.ticker as mticker
import seaborn as sns

# ── Konfigurasi halaman ──────────────────────────────────────────────────────
st.set_page_config(
    page_title="E-Commerce Olist Dashboard",
    page_icon="🛒",
    layout="wide"
)

# ── Load data ────────────────────────────────────────────────────────────────
@st.cache_data
def load_data():
    orders         = pd.read_csv("dashboard/main_data.csv", parse_dates=["order_purchase_timestamp"])
    return orders

df = load_data()

# ── Sidebar ──────────────────────────────────────────────────────────────────
st.sidebar.title("🛒 Olist Dashboard")
st.sidebar.markdown("**E-Commerce Public Dataset**")
st.sidebar.markdown("---")

year_options = sorted(df["order_purchase_timestamp"].dt.year.unique())
selected_years = st.sidebar.multiselect(
    "Filter Tahun",
    options=year_options,
    default=[2017, 2018]
)

min_orders = st.sidebar.slider(
    "Minimal jumlah order per kategori (filter review)",
    min_value=10, max_value=500, value=100, step=10
)

st.sidebar.markdown("---")
st.sidebar.caption("Dibuat untuk Proyek Akhir Dicoding — Analisis Data dengan Python")

# ── Filter data ──────────────────────────────────────────────────────────────
df_filtered = df[df["order_purchase_timestamp"].dt.year.isin(selected_years)].copy()

# ── Header ───────────────────────────────────────────────────────────────────
st.title("📊 Dashboard Analisis E-Commerce Olist")
st.markdown("Analisis tren revenue dan kepuasan pelanggan berdasarkan E-Commerce Public Dataset (Brazil, 2016–2018).")
st.markdown("---")

# ── KPI Cards ────────────────────────────────────────────────────────────────
col1, col2, col3, col4 = st.columns(4)

total_revenue  = df_filtered["total_revenue"].sum()
total_orders   = df_filtered["order_id"].nunique()
avg_review     = df_filtered["review_score"].mean()
avg_delivery   = df_filtered["delivery_days"].mean() if "delivery_days" in df_filtered.columns else 0

col1.metric("💰 Total Revenue", f"R$ {total_revenue:,.0f}")
col2.metric("📦 Total Orders", f"{total_orders:,}")
col3.metric("⭐ Avg Review Score", f"{avg_review:.2f} / 5")
col4.metric("🚚 Avg Delivery (hari)", f"{avg_delivery:.1f}")

st.markdown("---")

# ── Visualisasi 1: Revenue Trend ──────────────────────────────────────────────
st.subheader("📈 Pertanyaan 1: Tren Revenue Bulanan (2017–2018)")
st.markdown(
    "Bagaimana tren total pendapatan (revenue) bulanan platform e-commerce Olist "
    "sepanjang periode 2017–2018, dan pada bulan mana terjadi puncak serta penurunan terbesar?"
)

revenue_monthly = (
    df_filtered
    .groupby(df_filtered["order_purchase_timestamp"].dt.to_period("M"))["total_revenue"]
    .sum()
    .reset_index()
)
revenue_monthly.columns = ["order_month", "total_revenue"]
revenue_monthly = revenue_monthly.sort_values("order_month")
revenue_monthly["order_month_str"] = revenue_monthly["order_month"].astype(str)

fig1, ax1 = plt.subplots(figsize=(14, 5))
x = range(len(revenue_monthly))
rev_vals = revenue_monthly["total_revenue"].values
labels   = revenue_monthly["order_month_str"].values

ax1.bar(x, rev_vals, color="steelblue", alpha=0.6, width=0.6, label="Revenue Bulanan")
ax1.plot(x, rev_vals, color="navy", linewidth=2, marker="o", markersize=4, label="Tren")

if len(rev_vals) > 0:
    idx_max = rev_vals.argmax()
    idx_min = rev_vals.argmin()
    ax1.annotate(
        f"PUNCAK\nR$ {rev_vals[idx_max]:,.0f}",
        xy=(idx_max, rev_vals[idx_max]),
        xytext=(max(0, idx_max - 2), rev_vals[idx_max] * 1.05),
        arrowprops=dict(arrowstyle="->", color="red"),
        color="red", fontsize=8, fontweight="bold"
    )

ax1.set_xticks(x)
ax1.set_xticklabels(labels, rotation=45, ha="right", fontsize=8)
ax1.yaxis.set_major_formatter(mticker.FuncFormatter(lambda v, _: f"R$ {v/1e6:.1f}M"))
ax1.set_title("Tren Revenue Bulanan Platform Olist", fontsize=13, fontweight="bold")
ax1.set_xlabel("Bulan")
ax1.set_ylabel("Total Revenue (BRL)")
ax1.legend()
ax1.grid(axis="y", alpha=0.4)
sns.despine()
plt.tight_layout()
st.pyplot(fig1)

with st.expander("💡 Insight"):
    st.markdown("""
    - Revenue tumbuh positif sepanjang 2017 dengan **puncak di November 2017** (Black Friday).
    - Terjadi penurunan di Desember–Januari (efek post-holiday), lalu kembali naik stabil di 2018.
    - Tren keseluruhan menunjukkan pertumbuhan bisnis yang sehat dari tahun ke tahun.
    """)

st.markdown("---")

# ── Visualisasi 2: Review Score per Kategori ──────────────────────────────────
st.subheader("⭐ Pertanyaan 2: Review Score per Kategori Produk")
st.markdown(
    "Kategori produk apa yang memiliki rata-rata review score tertinggi dan terendah, "
    "dan berapa selisihnya?"
)

review_by_cat = (
    df_filtered.dropna(subset=["review_score", "product_category_name_english"])
    .groupby("product_category_name_english")
    .agg(avg_review=("review_score", "mean"), total_orders=("order_id", "nunique"))
    .reset_index()
)
review_by_cat = review_by_cat[review_by_cat["total_orders"] >= min_orders].sort_values("avg_review", ascending=False)

top_n  = st.slider("Tampilkan N kategori terbaik & terburuk", 5, 15, 10)
top10  = review_by_cat.head(top_n)
bot10  = review_by_cat.tail(top_n)

fig2, (ax2a, ax2b) = plt.subplots(1, 2, figsize=(16, 6))

bars_top = ax2a.barh(top10["product_category_name_english"], top10["avg_review"],
                     color="seagreen", alpha=0.85)
ax2a.set_xlim(3.5, 5.1)
ax2a.bar_label(bars_top, fmt="%.2f", padding=3, fontsize=9, fontweight="bold", color="seagreen")
ax2a.set_title(f"Top {top_n} Kategori — Review Tertinggi", fontsize=11, fontweight="bold")
ax2a.set_xlabel("Rata-rata Review Score (1–5)")
ax2a.invert_yaxis()
ax2a.grid(axis="x", alpha=0.3)
sns.despine(ax=ax2a, left=True)

bars_bot = ax2b.barh(bot10["product_category_name_english"], bot10["avg_review"],
                     color="tomato", alpha=0.85)
ax2b.set_xlim(2.5, 4.5)
ax2b.bar_label(bars_bot, fmt="%.2f", padding=3, fontsize=9, fontweight="bold", color="tomato")
ax2b.set_title(f"Bottom {top_n} Kategori — Review Terendah", fontsize=11, fontweight="bold")
ax2b.set_xlabel("Rata-rata Review Score (1–5)")
ax2b.invert_yaxis()
ax2b.grid(axis="x", alpha=0.3)
sns.despine(ax=ax2b, left=True)

plt.suptitle("Perbandingan Rata-rata Review Score per Kategori", fontsize=12, fontweight="bold")
plt.tight_layout()
st.pyplot(fig2)

if len(review_by_cat) >= 2:
    best  = review_by_cat.iloc[0]
    worst = review_by_cat.iloc[-1]
    st.info(
        f"**Kategori terbaik:** {best['product_category_name_english']} "
        f"({best['avg_review']:.2f}) &nbsp;|&nbsp; "
        f"**Kategori terburuk:** {worst['product_category_name_english']} "
        f"({worst['avg_review']:.2f}) &nbsp;|&nbsp; "
        f"**Selisih:** {best['avg_review'] - worst['avg_review']:.2f}"
    )

with st.expander("💡 Insight"):
    st.markdown("""
    - Kategori **gift vouchers** dan **fashion accessories** mendapat review tertinggi karena ekspektasi pelanggan mudah terpenuhi.
    - Kategori **office furniture** dan **diapers/hygiene** mendapat review terendah, kemungkinan karena standar fungsional yang tinggi dan risiko kekecewaan lebih besar.
    - Selisih antar kategori terbaik dan terburuk mencapai **>0.7 poin** dari skala 5 — signifikan untuk ditindaklanjuti.
    """)
