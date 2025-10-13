# from collections import deque
# from datetime import date
# import requests
# import os
# from dotenv import load_dotenv
# import time

# # ========= Load config =========
# load_dotenv()
# ACCESS_TOKEN = os.getenv("ACCESS_TOKEN")
# URL = os.getenv("API_URL")

# history_consumption = deque()
# FOLDER_ID = "08dd6783-bb5c-4ab4-837f-8b24c727aff2"


# MONTH_RANGES = [
#     (date(2025, 1, 3), date(2025, 2, 3)),
#     (date(2025, 2, 3), date(2025, 3, 3)),
#     (date(2025, 3, 3), date(2025, 4, 3)),
#     (date(2025, 4, 3), date(2025, 5, 3)),
#     (date(2025, 5, 3), date(2025, 6, 3)),
#     (date(2025, 6, 3), date(2025, 7, 3)),
#     (date(2025, 7, 3), date(2025, 8, 3)),
#     (date(2025, 8, 3), date(2025, 9, 3)),
#     (date(2025, 9, 3), date(2025, 10, 3)), 
# ]


# def fetch_monthly_range():
#     if not ACCESS_TOKEN or not URL:
#         raise RuntimeError("⚠️ Thiếu ACCESS_TOKEN hoặc API_URL trong .env")

#     headers = {"Authorization": f"Bearer {ACCESS_TOKEN}"}

#     for start_date, end_date in MONTH_RANGES:
#         params = {
#             "folderId": FOLDER_ID,
#             "itemType": "ELECTRICITY",
#             "timeType": "month",   
#             "startMonth": start_date.isoformat(),
#             "endMonth": end_date.isoformat(),
#         }

#         print(f"🔍 Fetching {start_date} → {end_date}")
#         try:
#             resp = requests.get(URL, headers=headers, params=params, timeout=20)
#         except requests.RequestException as e:
#             print(f"❌ Request error {start_date}: {e}")
#             continue

#         if resp.status_code == 200:
#             try:
#                 data = resp.json()
#                 data_info = data.get("data", {})
#                 for info in data_info.get("spaces", []):
#                     history_consumption.append({
#                         "startMonth": start_date.isoformat(),
#                         "endMonth": end_date.isoformat(),
#                         "name": info.get("name"),
#                         "total": info.get("total"),
#                         "currentTotal": info.get("currentTotal"),
#                         "proportion": info.get("proportion"),
#                         "totalCarbon": data_info.get("totalCarbon"),
#                         "lastTotalCarbon": data_info.get("lastTotalCarbon"),
#                         "qoQDecimal": data_info.get("qoQDecimal"),
#                         "qoQ": data_info.get("qoQ"),
#                     })
#                 print(f"✅ Done {start_date} → {end_date}")
#             except Exception as e:
#                 print(f"⚠️ JSON parse error ({start_date}): {e}")
#         else:
#             print(f"⚠️ HTTP {resp.status_code} for {start_date}: {resp.text[:200]}")

#         time.sleep(0.3)  # tránh spam server


# def get_history_consumption():
#     # print(list(history_consumption))
#     return list(history_consumption)

# # ========= Chạy =========
# print("🕐 Fetching monthly ranges (03-01 → 03-09)...")
# fetch_monthly_range()
