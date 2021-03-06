#####################################################
#      GENERAL SETTINGS FOR HEROKU ENVIRONMENTS     #
#####################################################
# DATABASES, ALLOWED_HOSTS:
# Should not be specified at all on Heroku. They are
# dealt with using magic.
#
# DATABASE_URL, SECRET_KEY:
# Should be provided as environment variables. When
# running Heroku locally this can be done using an
# .env file. In the Heroku cloud DATABASE_URL is set
# automatically, but SECRET_KEY must be set manually.
#
# IS_HEROKU: Set this to "1" in the environment,
# in the .env file locally or via the interface in
# the cloud. Otherwise this file will not be read.

import os

# Now you can put DEBUG = "True" as an environment variable
# on Heroku to enable Django debugging!
if "DEBUG" in os.environ and os.environ["DEBUG"] == "True":
    DEBUG = True
    AUTH_PASSWORD_VALIDATORS = []  # Simple passwords during development
