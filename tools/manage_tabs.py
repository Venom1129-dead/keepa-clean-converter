import urllib.request
import json
import sys

def list_tabs():
    try:
        req = urllib.request.urlopen("http://127.0.0.1:9222/json", timeout=3)
        tabs = json.loads(req.read().decode('utf-8'))
        return tabs
    except Exception as e:
        print(f"Error connecting to 9222: {e}")
        return []

def close_tab(tab_id):
    try:
        url = f"http://127.0.0.1:9222/json/close/{tab_id}"
        req = urllib.request.Request(url, method='PUT')
        with urllib.request.urlopen(req, timeout=3) as resp:
            return resp.status == 200
    except Exception as e:
        print(f"Error closing tab {tab_id}: {e}")
        return False

if __name__ == "__main__":
    tabs = list_tabs()
    print(f"Total targets reported on port 9222: {len(tabs)}")
    for t in tabs:
        print(f"ID: {t.get('id')} | Type: {t.get('type')} | Title: {t.get('title')} | URL: {t.get('url')}")
