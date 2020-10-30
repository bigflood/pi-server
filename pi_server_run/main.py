from typing import Optional, List
from flask import Flask
import logging
import pi_server

__version__ = pi_server.__version__

app = Flask(__name__)


@app.route('/')
def hello_world():
    return f'Hello World! {__version__}'


def main(args: Optional[List[str]] = None) -> int:
    logger = logging.getLogger()
    logger.info(f'version={__version__}')
    app.run(host='0.0.0.0')
    return 0
