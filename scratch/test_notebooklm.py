import urllib.request
import ssl

cookie_header = (
    "__Secure-1PSID=g.a000BAlsXTqNfk7D4fvnWBRR5kumRS0iumSto7emnQm6HP8KQlivylwlj3jlDyBk9FLEzQDzcAACgYKASYSARISFQHGX2MiLLKIKZVJb_pk3EDPpaMVrRoVAUF8yKpm-C2EtYkW4_bcQtxsswuP0076; "
    "__Secure-3PSID=g.a000BAlsXTqNfk7D4fvnWBRR5kumRS0iumSto7emnQm6HP8KQlivBlBIq3CxCnB4nX4vhCUbogACgYKAZ8SARISFQHGX2MiqJlduIIklxfWqs3KnoNiRhoVAUF8yKoLSn6TodIHvrXtFHSEkQKF0076"
)

url = "https://notebooklm.google.com"

req = urllib.request.Request(url, headers={
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, Gecko) Chrome/120.0.0.0 Safari/537.36",
    "Cookie": cookie_header
})

ctx = ssl._create_unverified_context()

try:
    with urllib.request.urlopen(req, context=ctx, timeout=10) as resp:
        content = resp.read().decode('utf-8')
        if resp.status == 200:
            print("SUCCESS: NotebookLM Session Verified! Response Code: 200 OK")
            print("Content Length:", len(content))
        else:
            print("RESPONSE STATUS:", resp.status)
except Exception as e:
    print("ERROR connecting to NotebookLM:", e)
