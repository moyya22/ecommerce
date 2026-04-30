# 📊 Proyek Analisis Data — E-Commerce Public Dataset (Olist)

Proyek analisis data menggunakan **Brazilian E-Commerce Public Dataset** dari Olist untuk menjawab pertanyaan bisnis terkait tren revenue dan kepuasan pelanggan.

## 📁 Struktur Direktori

```
submission/
├── dashboard/
│   ├── dashboard.py        # Aplikasi Streamlit
│   └── main_data.csv       # Data yang digunakan dashboard
├── data/
│   ├── orders_dataset.csv
│   ├── customers_dataset.csv
│   ├── order_items_dataset.csv
│   ├── order_payments_dataset.csv
│   ├── order_reviews_dataset.csv
│   ├── products_dataset.csv
│   ├── sellers_dataset.csv
│   └── product_category_name_translation.csv
├── notebook.ipynb          # Notebook analisis lengkap
├── requirements.txt        # Daftar library
└── README.md               # Dokumentasi ini
```

## 🔍 Pertanyaan Bisnis

1. **Tren Revenue Bulanan** — Bagaimana tren total pendapatan bulanan platform Olist sepanjang 2017–2018, dan pada bulan mana terjadi puncak tertinggi?

2. **Review Score per Kategori** — Kategori produk apa yang memiliki rata-rata review score tertinggi dan terendah, dan berapa selisihnya?

## 🚀 Cara Menjalankan Dashboard

### 1. Install Dependencies

```bash
pip install -r requirements.txt
```

### 2. Jalankan Streamlit

```bash
streamlit run dashboard/dashboard.py
```

Dashboard akan terbuka otomatis di browser pada alamat `http://localhost:8501`.

## 📦 Sumber Dataset

Dataset berasal dari [Brazilian E-Commerce Public Dataset by Olist](https://www.kaggle.com/datasets/olistbr/brazilian-ecommerce) yang juga disediakan oleh Dicoding Indonesia.
