#!/usr/bin/env python3

# Import from standard library. https://docs.python.org/3/library/

import json
import os
import signal
import sys
import time

# Import from https://pypi.org/

from flask import Flask, render_template

# Determine "Major" version of Senzing SDK.

senzing_sdk_version_major = None

# Import from Senzing.

try:
    from senzing import G2Engine, G2Product
    senzing_sdk_version_major = 3

except:

    # Fall back to pre-Senzing-Python-SDK style of imports.

    try:
        from G2Engine import G2Engine
        from G2Product import G2Product
        senzing_sdk_version_major = 2
    except:
        print("ERROR: Could not import G2Engine, G2Audit, G2Product")
        print("Ctrl-C to exit")
        time.sleep(3600)
        sys.exit(0)

# Signal handling.


def signal_handler(signal, frame):
    sys.exit(0)


signal.signal(signal.SIGTERM, signal_handler)
signal.signal(signal.SIGINT, signal_handler)

# Flask application.

app = Flask(__name__)

# Metadata

__all__ = []
__version__ = "1.4.4"  # See https://www.python.org/dev/peps/pep-0396/
__date__ = '2018-10-29'
__updated__ = '2022-03-22'

# -----------------------------------------------------------------------------
# Senzing configuration.
# -----------------------------------------------------------------------------


def get_g2_configuration_dictionary():
    ''' Construct a dictionary in the form of the old ini files. '''\

    # Special case: /opt/senzing/data/2.0.0

    senzing_support_path = "/opt/senzing/data"

    if senzing_sdk_version_major == 3:
        string_template = "{0}/3.0.0"
    else:
        string_template = "{0}/2.0.0"

    test_data_dir_path = string_template.format(senzing_support_path)
    if os.path.exists(test_data_dir_path):
        senzing_support_path = test_data_dir_path

    result = {
        "PIPELINE": {
            "CONFIGPATH": os.environ.get("SENZING_CONFIG_PATH", "/etc/opt/senzing"),
            "RESOURCEPATH": os.environ.get("SENZING_RESOURCE_PATH", "/opt/senzing/g2/resources"),
            "SUPPORTPATH": os.environ.get("SENZING_SUPPORT_PATH", senzing_support_path),
        },
        "SQL": {
            "CONNECTION": os.environ.get("SENZING_SQL_CONNECTION", "sqlite3://na:na@/var/opt/senzing/sqlite/G2C.db"),
        }
    }
    return result


def get_g2_configuration_json():
    return json.dumps(get_g2_configuration_dictionary())

# -----------------------------------------------------------------------------
# Initialization
# -----------------------------------------------------------------------------

# Establish directories and paths.


g2_configuration_json = get_g2_configuration_json()
senzing_python_directory = "/opt/senzing/g2/python"
verbose_logging = False
config_id = bytearray([])

# Add python directory to System Path.

sys.path.append(senzing_python_directory)

# Initialize Senzing G2Engine.

g2_engine = G2Engine()

# Backport methods from earlier Senzing versions.

if senzing_sdk_version_major == 2:
    g2_engine.init = g2_engine.initV2
    g2_engine.reinit = g2_engine.reinitV2
    g2_engine.initWithConfigID = g2_engine.initWithConfigIDV2

g2_engine.init('pyG2', g2_configuration_json, verbose_logging)

# Initialize Senzing G2Product.

g2_product = G2Product()

# Backport methods from earlier Senzing versions.

if senzing_sdk_version_major == 2:
    g2_product.init = g2_product.initV2

g2_product.init('pyG2Product', g2_configuration_json, verbose_logging)

# -----------------------------------------------------------------------------
# @app.routes
# -----------------------------------------------------------------------------


@app.route("/")
def app_root():

    # Get version and format it.

    version_string = g2_product.version()
    version_dictionary = json.loads(version_string)
    version = json.dumps(version_dictionary, sort_keys=True, indent=4)

    # Get license and format it.

    license_string = g2_product.license()
    license_dictionary = json.loads(license_string)
    license = json.dumps(license_dictionary, sort_keys=True, indent=4)

    # Get config and format it.

    config_string = bytearray()
    result = g2_engine.exportConfig(config_string, config_id)
    config_dictionary = json.loads(config_string)
    config = json.dumps(config_dictionary, sort_keys=True, indent=4)

    # Render template in to HTML page.

    return render_template("index.html", version=version, config=config, license=license)

# -----------------------------------------------------------------------------
# Main
# -----------------------------------------------------------------------------


if __name__ == '__main__':
    app.run()

