from flask import Flask, jsonify, request
import requests
import random
import string

def RandomCharacterGenerator(length):
    return ''.join(random.choices(string.ascii_letters + string.digits, k=length))

def RandomStringGenerator(length):
    return ''.join(random.choices(string.ascii_letters, k=length))

def RandomDigitGenerator(length):
    return ''.join(random.choices(string.digits, k=length))

def IPAddressGenerator():
    ip = ".".join(str(random.randint(0, 255)) for _ in range(4))
    return ip

def UserAgentGenerator():
    # Random iOS version
    ios_version = f"{random.randint(10, 14)}_{random.randint(0, 9)}"

    # Random iPhone model
    iphone_models = ["iPhone 12", "iPhone 11", "iPhone XS", "iPhone XR", "iPhone X", "iPhone 8", "iPhone 7"]
    iphone_model = random.choice(iphone_models)

    # Random Safari version
    safari_version = f"{random.randint(600, 605)}.{random.randint(0, 9)}.{random.randint(10, 99)}"

    # Constructing the user agent string
    user_agent = f"Mozilla/5.0 (iPhone {iphone_model}; CPU iPhone OS {ios_version} like Mac OS X) AppleWebKit/{safari_version} (KHTML, like Gecko) Version/{safari_version} Mobile/15E148 Safari/{safari_version}"
    
    return user_agent

def UserAgentGenerator2():
    browsers = ['chrome', 'firefox']
    browser = random.choice(browsers)

    android_versions = [8, 9, 10, 11, 12, 13]
    android_version = random.choice(android_versions)

    if browser == 'chrome':
        user_agent = (
            f"Mozilla/5.0 (Linux; Android {android_version}.0; "
            f"Build/R{random.randint(1, 9999)}; wv) AppleWebKit/537.36 "
            f"(KHTML, like Gecko) Chrome/{random.randint(80, 90)}.0."
            f"{random.randint(4000, 5000)}.{random.randint(100, 900)} "
            f"Mobile Safari/537.36"
        )
    else:  # Firefox
        user_agent = (
            f"Mozilla/5.0 (Android {android_version}.0; Mobile; rv:{random.randint(70, 90)}.0) "
            f"Gecko/20100101 Firefox/{random.randint(70, 90)}.0"
        )

    return user_agent

def PhoneNumberGenerator():
    phone_number = "9"  # Start with 9

    for _ in range(9):  # Add 9 more random digits
        phone_number += str(random.randint(0, 9))

    return phone_number

def RandomEmailAddressGenerator():
    url = 'https://randomuser.me/api/?nat=us'
    response = requests.get(url)
    responseData = response.json()
    email1 = f"{responseData['results'][0]['email']}".replace(".", "").strip()
    email2 = email1.replace('@examplecom', f'{RandomDigitGenerator(5)}@gmail.com')
    lower_case = email2.lower()
    return lower_case

def UsernameGenerator():
    url = 'https://randomuser.me/api/?nat=us'
    response = requests.get(url)
    responseData = response.json()
    username = f"{responseData['results'][0]['name']['first']}{RandomDigitGenerator(6)}".strip()
    lower_case = username.lower()
    return lower_case

app = Flask(__name__)

@app.route('/apanalo_register', methods=['GET'])
def apanalo_register():
    invite_code = request.args.get('invite_code')
    phone_number = PhoneNumberGenerator()
    user_agent = UserAgentGenerator2()
    ip_address = IPAddressGenerator()
    password = f"{UsernameGenerator}{RandomDigitGenerator(4)}"
    url = "https://api.apanalo2.com/v2/user/phone_register"
    
    headers = {
        "accept": "application/json, text/plain, */*",
        "accept-language": "en-US,en;q=0.9",
        "authorization": ";",
        "content-type": "application/json",
        "sec-fetch-dest": "empty",
        "sec-fetch-mode": "cors",
        "sec-fetch-site": "same-site",
        "x-forwarded-for": ip_address,
        "Referer": "https://apanalo2.com/",
        "User-Agent": user_agent,
        "Referrer-Policy": "strict-origin-when-cross-origin"
    }
    
    data = {
        "phone": phone_number,
        "from": "act_raffle",
        "code": "",
        "password": password,
        "person": invite_code
    }

    response = requests.post(url, headers=headers, json=data)

    return jsonify({
        "status_code": response.status_code,
        "response_data": response.json()
    })

if __name__ == '__main__':
    app.run(debug=True)
