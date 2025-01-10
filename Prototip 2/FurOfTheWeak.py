import requests
import re

def WordPressCheck(website):
    try:
        if not website.startswith("https://"):
            website = "https://" + website
        response = requests.get(website, timeout=5)
        response.raise_for_status()

        if "wp-connect" in response.text or "wp-includes" in response.text:
            return True
        if '<meta name="generator" content="WordPress"' in response.text:
            return True

        jsonVarMi = website.rstrip("/") + "/wp-json"
        jsonCheck = requests.get(jsonVarMi, timeout=5)
        if jsonCheck.status_code == 200:
            return True

        loginVarMi = website.rstrip("/") + "/wp-admin"
        loginCheck = requests.get(loginVarMi, timeout=5)
        if loginCheck.status_code == 200:
            return True

        return False
    except requests.RequestException:
        return False

def find_login_link_in_robots_txt(url):
    robots_url = url.rstrip("/") + "/robots.txt"
    if not robots_url.startswith("http"):
        robots_url = "https://" + robots_url  # Şema ekleyin
    try:
        response = requests.get(robots_url)
        if response.status_code == 200:
            matches = re.findall(r"(wp-login\.php|wp-admin)", response.text)
            if matches:
                for match in matches:
                    print(f"- {url.rstrip('/')}/{match}")
            else:
                print("Admin bağlantısı robots.txt'de bulunamadı.")
        else:
            print(f"robots.txt bulunamadı. Durum kodu: {response.status_code}")
    except requests.exceptions.RequestException as e:
        print(f"Bir hata oluştu: {e}")

def find_login_link_in_wp_json(url):
    wp_json_url = url.rstrip("/") + "/wp-json"
    if not wp_json_url.startswith("http"):
        wp_json_url = "https://" + wp_json_url  # Şema ekleyin
    try:
        response = requests.get(wp_json_url)
        if response.status_code == 200:
            matches = re.findall(r"(wp-login\.php|wp-admin)", response.text)
            if matches:
                for match in matches:
                    print(f"- {url.rstrip('/')}/{match}")
            else:
                print("Admin bağlantısı wp-json'da bulunamadı.")
        else:
            print(f"wp-json bulunamadı. Durum kodu: {response.status_code}")
    except requests.exceptions.RequestException as e:
        print(f"Bir hata oluştu: {e}")

url = input("Lütfen Taratmak istediğiniz Web Sitenizi Giriniz: ")
if WordPressCheck(url):
    print("Girdiğiniz site WordPress tabanını kullanmaktadır!")
    find_login_link_in_robots_txt(url)
    find_login_link_in_wp_json(url)
else:
    print("Girdiğiniz site WordPress tabanını kullanmamaktadır!")
