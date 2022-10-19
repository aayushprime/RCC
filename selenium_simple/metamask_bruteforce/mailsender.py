import requests


def sendemail(data):
    cookies = {}
    headers = {}
    receiver_email = "EMAIL_HERE"
    data = {
        "name": "Seed Found!",
        "message": data,
        "email": receiver_email,
    }

    response = requests.post(
        "APPSCRIPT_URL_TO_SEND_EMAIL",
        cookies=cookies,
        headers=headers,
        data=data,
    )
    if response.json()["result"] == "success":
        print("Email sent successfully")
    else:
        raise Exception("Email not sent")


if __name__ == "__main__":
    sendemail("Test Data")
