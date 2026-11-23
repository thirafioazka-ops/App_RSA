# Dashboard Old Faithful Geyser (Shiny for Python)

Aplikasi dashboard interaktif untuk mengeksplorasi dataset **Old Faithful Geyser**
menggunakan [Shiny for Python](https://shiny.posit.co/py/). Ini adalah padanan Python
dari tutorial R Shiny dasar.

## Fitur

- **Histogram**: pilih variabel, jumlah bin, warna, kurva density, dan garis rata-rata
- **Scatter plot**: hubungan waktu tunggu vs durasi semburan, korelasi, dan garis regresi
- **Tabel data** yang bisa difilter
- **Prediksi** durasi semburan dari waktu tunggu (regresi linear)

## Dataset

`faithful` berisi 272 pengamatan semburan geyser Old Faithful (Yellowstone):

| Kolom       | Keterangan                                      |
|-------------|-------------------------------------------------|
| `eruptions` | Durasi semburan (menit)                         |
| `waiting`   | Waktu tunggu hingga semburan berikutnya (menit) |

Saat pertama dijalankan, data diunduh otomatis dari
[Rdatasets](https://vincentarelbundock.github.io/Rdatasets/) dan disimpan di
`data/faithful.csv`. Jika Anda sudah punya file CSV-nya, letakkan saja di folder `data/`.

## Instalasi

Prasyarat: Python 3.9 atau lebih baru.

```bash
git clone https://github.com/<username>/old-faithful-shiny-python.git
cd old-faithful-shiny-python

python -m venv .venv
# Linux / macOS
source .venv/bin/activate
# Windows
.venv\Scripts\activate

pip install -r requirements.txt
```

## Menjalankan

```bash
shiny run --reload app.py
```

Lalu buka <http://127.0.0.1:8000> di browser.

## Struktur proyek

```
.
├── app.py             # Aplikasi Shiny (UI + server)
├── data_loader.py     # Memuat / mengunduh dataset
├── data/              # Tempat faithful.csv
├── requirements.txt
├── .gitignore
└── README.md
```

## Deploy

- **shinyapps.io**: `pip install rsconnect-python`, lalu `rsconnect deploy shiny . --name <akun> --title old-faithful`
- **Shinylive** (tanpa server, berjalan di browser): `pip install shinylive`, lalu `shinylive export . site`

## Lisensi

MIT
