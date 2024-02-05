from flask import Flask, jsonify
from selenium import webdriver
from io import BytesIO


app = Flask(__name__)


def take_screenshot(url):
    options = webdriver.ChromeOptions()
    options.add_argument("headless")
    driver = webdriver.Chrome(options=options)

    driver.get(url)

    screenshot = driver.get_screenshot_as_png()

    driver.quit()

    return screenshot


def screenshot_to_byte_list(screenshot):
    # Convert screenshot to byte array
    screenshot_bytes = BytesIO(screenshot)
    byte_list = []
    for byte in screenshot_bytes.getvalue():
        byte_list.append(byte)

    return byte_list


@app.route("/", methods=["GET"])
def handleMain():
    return "hey there, how'd you end up here? this is the main website: https://clear.adithya.zip"


@app.route("/api", methods=["GET"])
def handleScreenshot():
    response = "w"

    url = "https://google.com"  # URL of the website to take screenshot
    screenshot = take_screenshot(url)
    screenshot_bytes = screenshot_to_byte_list(screenshot)

    response = {"img": screenshot_bytes}

    response = jsonify(response)

    response.headers.add(
        "Access-Control-Allow-Origin",
        "*",
    )
    return response


# command to run python -m flask run --debug --port 5002
