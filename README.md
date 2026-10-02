# Analisis Sentimen Ulasan Aplikasi di Google Play Store

Proyek analisis sentimen berbahasa Indonesia untuk ulasan aplikasi **Shopee, Tokopedia, Gojek, dan Lazada** di Google Play Store. Model mengklasifikasikan ulasan ke dalam tiga kelas: **negatif, netral, positif**.

## Struktur Folder

| File | Keterangan |
|---|---|
| `scraping.py` | Kode scraping ulasan dari Google Play Store |
| `reviews_playstore.csv` | Dataset hasil scraping mandiri |
| `notebook_pelatihan_sentimen.ipynb` | Notebook preprocessing, pelabelan, pelatihan 3 skema, dan inference |
| `requirements.txt` | Daftar library yang dibutuhkan |
| `README.md` | Dokumentasi proyek |

## Cara Menjalankan

1. Buat environment dan pasang library (disarankan Python 3.9 - 3.12):
   ```bash
   conda create -n sentimen python=3.12 -y
   conda activate sentimen
   python -m pip install -r requirements.txt
   python -m pip install notebook ipykernel
   ```
2. Jalankan scraping (opsional, dataset sudah disertakan):
   ```bash
   python scraping.py
   ```
3. Buka `notebook_pelatihan_sentimen.ipynb` dan jalankan semua cell secara berurutan. Notebook yang dikirim sudah berisi output.

## Pengumpulan Data

- **Sumber:** Google Play Store (bahasa `id`, negara `id`) lewat library `google-play-scraper`.
- **Aplikasi:** Shopee, Tokopedia, Gojek, Lazada.
- **Strategi:** mengambil ulasan terbaru untuk setiap tingkat bintang (1 - 5) agar variasi opini seimbang.
- **Etika:** hanya ulasan publik yang diambil. Nama dan foto pengguna tidak disimpan, dan scraper memberi jeda antar-request.
- **Jumlah data:** `ISI_JUMLAH` ulasan setelah pembersihan.

## Tahapan

1. **Preprocessing:** lowercase, hapus URL dan simbol, normalisasi huruf berulang, normalisasi kata slang, hapus stopword (kata negasi dipertahankan), hapus duplikat.
2. **Pelabelan:** berbasis leksikon **InSet** dengan skor total bobot kata dan penanganan negasi sederhana. Skor > 0 positif, < 0 negatif, 0 netral.
3. **Pembersihan label:** sampel dengan skor lemah dan sampel yang bertentangan kuat dengan rating bintang dibuang untuk mengurangi label ambigu.
4. **Ekstraksi fitur:** TF-IDF (unigram dan bigram) serta Tokenizer + Embedding.
5. **Pelatihan:** tiga skema berbeda (lihat tabel di bawah).
6. **Inference:** fungsi `predict_sentiment()` menghasilkan kelas kategorikal (negatif, netral, positif).

## Skema Pelatihan dan Hasil

| Skema | Algoritma | Ekstraksi Fitur | Split | Akurasi Train | Akurasi Test |
|---|---|---|---|---|---|
| 1 | LinearSVC | TF-IDF (1-2 gram) | 80/20 | `ISI` | `ISI` |
| 2 | BiLSTM | Tokenizer + Embedding | 80/20 | `ISI` | `ISI` |
| 3 | BiGRU | Tokenizer + Embedding | 70/30 | `ISI` | `ISI` |

> Isi nilai `ISI` dengan angka dari tabel ringkasan di notebook setelah dijalankan.

## Contoh Inference

```
POSITIF  (0.xx) | Aplikasinya bagus banget, pengiriman cepat dan mudah dipakai
NEGATIF  (0.xx) | Aplikasi sering error, kecewa banget, tidak bisa login
NETRAL   (0.xx) | Biasa saja, fiturnya standar
```

Hasil lengkap ada di bagian *Inference* pada notebook.

## Catatan

- Pelabelan memakai leksikon sehingga label bersifat otomatis dan bisa mengandung noise, terutama pada ulasan sarkastik.
- Hasil dapat sedikit berbeda antar-eksekusi karena sifat acak pada pelatihan jaringan saraf.
- Leksikon InSet digunakan hanya untuk pelabelan. Data ulasan sepenuhnya hasil scraping mandiri.
