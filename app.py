from flask import Flask, jsonify
from flask import request
from selenium import webdriver
from selenium.webdriver.edge.options import Options
from io import BytesIO
from time import sleep

app = Flask(__name__)

# ! Uncomment the following code if you want to change the browser from Chrome to Edge

# opt = Options()
# opt.add_argument("--headless")
# driver = webdriver.Edge(options=opt)


@app.route("/", methods=["GET"])
def handleMain():
    return "hey there, how'd you end up here?"


@app.route("/api", methods=["GET", "POST"])
def handleScreenshot():

    url = str(request.args.get("url"))
    width = str(request.args.get("width"))
    height = str(request.args.get("height"))

    def takeScreenshot(url):
        opt = Options()
        opt.add_argument("--headless")
        opt.add_argument(f"--window-size={width},{height}")

        # ! Uncomment the following code if you want to change the browser from Chrome to Edge
        # driver = webdriver.Edge(options=opt)

        driver = webdriver.Chrome(options=opt)  # ! And comment this one out

        driver.get(url)

        sleep(2)

        screenshot = driver.get_screenshot_as_png()

        driver.quit()

        return screenshot

    def screenshotToBytesList(screenshot):
        screenshotBytes = BytesIO(screenshot)
        byteList = []
        for byte in screenshotBytes.getvalue():
            byteList.append(byte)

        return byteList

    screenshot = takeScreenshot(url)
    screenshotBytes = screenshotToBytesList(screenshot)

    response = {"img": screenshotBytes}

    response = jsonify(response)

    response.headers.add(
        "Access-Control-Allow-Origin",
        "*",
    )
    return response


# command to run python -m flask run --debug --port 5002
