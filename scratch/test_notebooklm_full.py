import urllib.request
import ssl

full_cookie = """SID=g.a000BAlsXTqNfk7D4fvnWBRR5kumRS0iumSto7emnQm6HP8KQlivDy6WE2Stlios-vv3UMPtaQACgYKAT0SARISFQHGX2Mi-_fzut4IAyeZ4uWjbQoWWhoVAUF8yKqKXHPEN8zHnLol0zOhoBi60076; __Secure-1PSID=g.a000BAlsXTqNfk7D4fvnWBRR5kumRS0iumSto7emnQm6HP8KQlivylwlj3jlDyBk9FLEzQDzcAACgYKASYSARISFQHGX2MiLLKIKZVJb_pk3EDPpaMVrRoVAUF8yKpm-C2EtYkW4_bcQtxsswuP0076; __Secure-3PSID=g.a000BAlsXTqNfk7D4fvnWBRR5kumRS0iumSto7emnQm6HP8KQlivBlBIq3CxCnB4nX4vhCUbogACgYKAZ8SARISFQHGX2MiqJlduIIklxfWqs3KnoNiRhoVAUF8yKoLSn6TodIHvrXtFHSEkQKF0076; SSID=AZBG6b3ZNqFGFkKoM; HSID=AvCsPXrjhYarWzAhc; APISID=r4cQ30-PUGCoYlfd/A1ntVGjdPtqQFvFRG; SAPISID=0hEwbkIj0GN-nL_P/AiabDRbp43hPM8eIP; __Secure-1PAPISID=0hEwbkIj0GN-nL_P/AiabDRbp43hPM8eIP; __Secure-3PAPISID=0hEwbkIj0GN-nL_P/AiabDRbp43hPM8eIP; SEARCH_SAMESITE=CgQIuaEB; AEC=AdJVEavLmlnhenoHC4lgNZH95z_5LkRYbAKwcqOFNrNgB4fa1xB9Gt2zdpk; OSID=g.a000BAlsXZVvJZSulsbrzm8CHEMjF2ljWzT1Q2w1EI_N688ziOYjZjF6DmvPmHSX1RTiqevWUgACgYKASASARISFQHGX2Mis82fGh37M9lYV56AsxQY3xoVAUF8yKq0Lz_W9jHH9x90cpZr6ovy0076; __Secure-OSID=g.a000BAlsXZVvJZSulsbrzm8CHEMjF2ljWzT1Q2w1EI_N688ziOYjaP8jBZQzXDOB0vUIqpZ6yQACgYKAWgSARISFQHGX2Mia_RnGlYVvCis30paJ2fTKBoVAUF8yKohSl6RlH9GvLLUpv4g1r_u0076; __Secure-BUCKET=CNgH; _gcl_au=1.1.229430996.1785487541; _ga=GA1.1.67570450.1785487539; NID=533=EkCJc7aYOSqrW1H5ppqwd3BcZc2mMd5t8nb1J7jdHHNaR-_uD7qTvKqNaj3IIcatfyVjVSj7k_shhDxxNjvZriq72BowzyKCSOS_mVkX9S5J-9uVZQHHcVw2qDL5Kd8G8jH3fkdfhxw68xmSKrWSc01zyjS8qeO1hkCmqIOzsrhDAULTgzTsdTM1vqe_qaCUD44Pi2NKocOFWgojwboiLs8szi6k4CUG4-eM0dsHHu1OqSHnIlArUXOyk7PyZNBZiSfhVQsWMqtGjuVVI9UoWyvvSC0CnKs4yt4zw1ah6PThztpQ2ogXgWRVRJpAqTmbOHW6fB8iSrI6vivG53WPXK-Ejk60javlqOAEiq-V; __Secure-1PSIDTS=sidts-CjIBPWEu2UwecarI6BctahiTGXbFhTe9rO8b_KeAi6hw7UGnGhvVF6pT1VymeguwIODw-hAA; __Secure-3PSIDTS=sidts-CjIBPWEu2UwecarI6BctahiTGXbFhTe9rO8b_KeAi6hw7UGnGhvVF6pT1VymeguwIODw-hAA; __Secure-STRP=ANmZwa1vHEIt4MkeidM792x2Z9VQUe3D58mswkbqe5SCrC2i-99SXcLfACXgvBIDrW4tuGYpVKCUHv4rACy_3noa9YEBM0hg3aTd; _gcl_aw=GCL.1785510064.CjwKCAjwj7HTBhBiEiwA8s35Ou059smTAOFwXioCOWXqrEDiXte26skrK5B79vvfhVCrGE6kcfOyghoCv94QAvD_BwE; GCL_AW_P=GCL.1785510064.CjwKCAjwj7HTBhBiEiwA8s35Ou059smTAOFwXioCOWXqrEDiXte26skrK5B79vvfhVCrGE6kcfOyghoCv94QAvD_BwE; _ga_W0LDH41ZCB=GS2.1.s1785510062$o2$g1$t1785510066$j56$l0$h0; SIDCC=AKEyXzVwjR8l8TKUcUwV1t3KgTWljwnTnPhgbeVHsWLapH3-yx3JP-20QiHpZuCFwLt4-eP-he8; __Secure-1PSIDCC=AKEyXzXOucSMGBfak-CkwzNBHQp7ZfNDS6sPr28Ye-0wPzAaGhSndsvV0xKI2tNO8MWFh0KP5M8; __Secure-3PSIDCC=AKEyXzXZpvNXPkVT_e1Ju3H6IeZfL6Gi8ua_ogI5hlOV7xtSDwoyTE9Diod-KtRTfvXz8NslUA"""

url = "https://notebook.google.com"

req = urllib.request.Request(url, headers={
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, Gecko) Chrome/120.0.0.0 Safari/537.36",
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
    "Cookie": full_cookie.strip()
})

ctx = ssl._create_unverified_context()

try:
    with urllib.request.urlopen(req, context=ctx, timeout=10) as resp:
        print("HTTP STATUS:", resp.status)
        content = resp.read().decode('utf-8')
        print("SUCCESS ON notebook.google.com! Content Length:", len(content))
except Exception as e:
    print("ERROR:", e)
