#!/usr/bin/env python3

"""
# Demonstration of calling Senzing.
"""

# Import from standard library. https://docs.python.org/3/library/

import json
import os
import signal
import sys

# Import from https://pypi.org/

from flask import Flask, render_template
from senzing import G2Engine, G2Product

# Signal handling.


def signal_handler(the_signal, frame):
    ''' Exit. '''
    print(f'Signal: {the_signal}')
    print(f'Frame: {frame}')
    sys.exit(0)


signal.signal(signal.SIGTERM, signal_handler)
signal.signal(signal.SIGINT, signal_handler)

# Flask application.

APP = Flask(__name__)

# Metadata

__all__ = []
__version__ = "1.5.4"  # See https://www.python.org/dev/peps/pep-0396/
__date__ = '2018-10-29'
__updated__ = '2023-09-29'

# -----------------------------------------------------------------------------
# Senzing configuration.
# -----------------------------------------------------------------------------


def get_g2_configuration_dictionary():
    ''' Construct a dictionary in the form of the old ini files. '''\

    result = {
        "PIPELINE": {
            "CONFIGPATH": os.environ.get("SENZING_CONFIG_PATH", "/etc/opt/senzing"),
            "RESOURCEPATH": os.environ.get("SENZING_RESOURCE_PATH", "/opt/senzing/g2/resources"),
            "SUPPORTPATH": os.environ.get("SENZING_SUPPORT_PATH", "/opt/senzing/data"),
        },
        "SQL": {
            "CONNECTION": os.environ.get("SENZING_SQL_CONNECTION", "sqlite3://na:na@/var/opt/senzing/sqlite/G2C.db"),
        }
    }
    return result


def get_g2_configuration_json():
    ''' Return a JSON string of Senzing Engine configuration. '''
    return json.dumps(get_g2_configuration_dictionary())

# -----------------------------------------------------------------------------
# Initialization
# -----------------------------------------------------------------------------

# Establish directories and paths.


G2_CONFIGURATION_JSON = get_g2_configuration_json()
VERBOSE_LOGGING = False
CONFIG_ID = bytearray([])

# Initialize Senzing G2Engine.

G2_ENGINE = G2Engine()
G2_ENGINE.init('pyG2', G2_CONFIGURATION_JSON, VERBOSE_LOGGING)

# Initialize Senzing G2Product.

G2_PRODUCT = G2Product()
G2_PRODUCT.init('pyG2Product', G2_CONFIGURATION_JSON, VERBOSE_LOGGING)

# -----------------------------------------------------------------------------
# @APP.routes
# -----------------------------------------------------------------------------


@APP.route("/")
def app_root():
    ''' Handle / path. '''

    # Get version and format it.

    version_string = G2_PRODUCT.version()
    version_dictionary = json.loads(version_string)
    version = json.dumps(version_dictionary, sort_keys=True, indent=4)

    # Get license and format it.

    license_string = G2_PRODUCT.license()
    license_dictionary = json.loads(license_string)
    license_pretty_string = json.dumps(license_dictionary, sort_keys=True, indent=4)

    # Get config and format it.

    config_string = bytearray()
    G2_ENGINE.exportConfig(config_string, CONFIG_ID)
    config_dictionary = json.loads(config_string)
    config = json.dumps(config_dictionary, sort_keys=True, indent=4)

    # Render template in to HTML page.

    return render_template("index.html", version=version, config=config, license=license_pretty_string)

# -----------------------------------------------------------------------------
# Main
# -----------------------------------------------------------------------------


if __name__ == '__main__':
    APP.run()
