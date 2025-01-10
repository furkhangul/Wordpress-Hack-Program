import requests

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


url = input("Lütfen Taratmak istediğiniz Web Sitenizi Giriniz: ")
if WordPressCheck(url):
    print("Girdiğiniz site WordPress tabanını kullanmaktadır!")
else:
    print("Girdiğiniz site WordPress tabanını kullanmamaktadır!")
