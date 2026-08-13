import urllib.request, json

urls_to_test = [
    ("POST", "http://127.0.0.1:5001/api/draft-reservations/delete/test_id_123"),
    ("DELETE", "http://127.0.0.1:5001/api/draft-reservations/test_id_123"),
    ("POST", "http://127.0.0.1:5001/api/draft-reservations-delete/test_id_123"),
]

for method, url in urls_to_test:
    try:
        req = urllib.request.Request(url, method=method)
        with urllib.request.urlopen(req) as resp:
            print(f"PASS {method} {url} -> Status: {resp.status}, Body: {resp.read().decode()}")
    except urllib.error.HTTPError as e:
        print(f"FAIL {method} {url} -> Status: {e.code}, Body: {e.read().decode()}")
    except Exception as e:
        print(f"ERROR {method} {url} -> {e}")
