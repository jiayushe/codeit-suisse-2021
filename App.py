import logging
from codeitsuisse import app

logger = logging.getLogger(__name__)
logger = logging.getLogger()
handler = logging.StreamHandler()
formatter = logging.Formatter('%(asctime)s %(name)-12s %(levelname)-8s %(message)s')
handler.setFormatter(formatter)
logger.addHandler(handler)
logger.setLevel(logging.INFO)

@app.route('/', methods=['GET'])
def default_route():
    return "Python Template"

if __name__ == "__main__":
    logging.info("Starting application ...")
    app.run(port=8000)
