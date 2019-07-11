#!/usr/bin/env python3

import os
import signal
import sys
import time
import json

from flask import Flask, render_template
app = Flask(__name__)


def signal_handler(signal, frame):
    sys.exit(0)


signal.signal(signal.SIGTERM, signal_handler)
signal.signal(signal.SIGINT, signal_handler)

try:
    from G2Engine import G2Engine
    from G2Audit import G2Audit
    from G2Product import G2Product
except:
    print("ERROR: Could not import G2Engine, G2Audit, G2Product")
    print("Possible causes:")
    print("    SENZING_DIR not available.")
    print("    PYTHONPATH environment variable not set correctly.")
    print("    LD_LIBRARY_PATH environment variable not set correctly.")
    print("Ctrl-C to exit")
    time.sleep(3600)
    sys.exit(0)

# -----------------------------------------------------------------------------
# Initialization
# -----------------------------------------------------------------------------

# Establish directories and paths

senzing_directory = os.environ.get("SENZING_DIR", "/opt/senzing")
senzing_python_directory = "{0}/g2/python".format(senzing_directory)
g2module_ini_pathname = "{0}/G2Module.ini".format(senzing_python_directory)
verbose_logging = False
config_id = bytearray([])

# Add python directory to System Path

sys.path.append(senzing_python_directory)

# Initialize Senzing G2 modules.

g2_engine = G2Engine()
g2_engine.init('pyG2', g2module_ini_pathname, verbose_logging)

g2_audit = G2Audit()
g2_audit.init('pyG2Audit', g2module_ini_pathname, verbose_logging)

g2_product = G2Product()
g2_product.init('pyG2Product', g2module_ini_pathname, verbose_logging)

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

    # Get summary and format it.

    summary_string = bytearray()
    result = g2_audit.getSummaryDataDirect(summary_string)
    summary_dictionary = json.loads(summary_string)
    summary = json.dumps(summary_dictionary, sort_keys=True, indent=4)

    # Render template in to HTML page.

    return render_template("index.html", version=version, config=config, summary=summary, license=license)

# -----------------------------------------------------------------------------
# Main
# -----------------------------------------------------------------------------


if __name__ == '__main__':
    app.run()

