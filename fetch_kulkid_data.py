#!/usr/bin/env python3
import json, requests, os

API_VERSION = "2024-01"
ACCESS_TOKEN = os.getenv("SHOPIFY_ACCESS_TOKEN")

BASE_URL = f"https://qtpcki-ju.myshopify.com/admin/api/{API_VERSION}"
OUTPUT = "./snapshot/kulkid_live_dump.json"

headers = {"X-Shopify-Access-Token": ACCESS_TOKEN}

endpoints = {
    "products": f"{BASE_URL}/products.json?limit=250",
    "collections": f"{BASE_URL}/custom_collections.json?limit=250",
    "smart_collections": f"{BASE_URL}/smart_collections.json?limit=250",
    "pages": f"{BASE_URL}/pages.json?limit=250",
    "policies": f"{BASE_URL}/policies.json",
}


dump = {}
for key, url in endpoints.items():
    try:
        r = requests.get(url, headers=headers, timeout=20)
        r.raise_for_status()
        dump[key] = r.json()
        print(f"✓ fetched {key}")
    except Exception as e:
        print(f"⚠️ {key} failed: {e}")

os.makedirs(os.path.dirname(OUTPUT), exist_ok=True)
with open(OUTPUT, "w") as f:
    json.dump(dump, f, indent=2, ensure_ascii=False)
print(f"\n✅ Saved snapshot to {OUTPUT}")

