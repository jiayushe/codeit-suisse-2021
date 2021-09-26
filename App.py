import logging
from codeitsuisse import app
from flask import render_template, request, send_from_directory
import os
import glob

logger = logging.getLogger(__name__)
logger = logging.getLogger()
handler = logging.StreamHandler()
formatter = logging.Formatter('%(asctime)s %(name)-12s %(levelname)-8s %(message)s')
handler.setFormatter(formatter)
logger.addHandler(handler)
logger.setLevel(logging.INFO)

@app.route('/', methods=['GET'])
def default_route():
    root = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'challenges')
    paths = glob.glob(os.path.join(root, '*.html'))
    pages = [path.split('/')[-1] for path in paths]
    pages.sort()
    return render_template('index.html', base=request.url + 'challenges/', pages=pages)

@app.route('/challenges/<path:path>', methods=['GET'])
def challenges(path):
    root = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'challenges')
    return send_from_directory(root, path)

if __name__ == "__main__":
    logging.info("Starting application ...")
    app.run(port=8000)
