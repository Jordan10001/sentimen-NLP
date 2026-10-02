"""
Scraping ulasan aplikasi e-commerce/transportasi di Google Play Store (bahasa Indonesia).
Hanya mengambil ulasan publik, tanpa data pribadi (nama/foto pengguna dibuang), dengan jeda antar-request.
Jalankan: python scraping.py   -> menghasilkan reviews_playstore.csv
"""
import time
import pandas as pd
from google_play_scraper import reviews, Sort

APPS = {
    "Shopee": "com.shopee.id",
    "Tokopedia": "com.tokopedia.tkpd",
    "Gojek": "com.gojek.app",
    "Lazada": "com.lazada.android",
}
PER_APP_PER_SCORE = 1000   # 4 app x 5 bintang x 1000 = ~20.000 ulasan mentah
BATCH = 200
SLEEP = 1.5                # jeda sopan agar tidak membebani server

rows = []
for app_name, app_id in APPS.items():
    for score in [1, 2, 3, 4, 5]:
        token, got = None, 0
        while got < PER_APP_PER_SCORE:
            try:
                batch, token = reviews(
                    app_id, lang="id", country="id",
                    sort=Sort.NEWEST, count=BATCH,
                    filter_score_with=score, continuation_token=token,
                )
            except Exception as e:
                print("Error:", e); time.sleep(10); break
            if not batch:
                break
            for r in batch:
                rows.append({
                    "reviewId": r["reviewId"], "app": app_name,
                    "content": r["content"], "score": r["score"], "at": r["at"],
                })
            got += len(batch)
            print(f"{app_name} | bintang {score} | {got}")
            if token is None:
                break
            time.sleep(SLEEP)

df = pd.DataFrame(rows).drop_duplicates("reviewId")
df = df.dropna(subset=["content"])
df = df[df["content"].str.split().str.len() >= 3]   # buang ulasan terlalu pendek
df.to_csv("reviews_playstore.csv", index=False)
print("Total ulasan:", len(df))
