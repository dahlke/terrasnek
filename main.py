from tfepy.api import TFE
import os

TOKEN = os.getenv("TFE_TOKEN", None)

if __name__ == "__main__":
    api = TFE(TOKEN)

    orgs = api.organizations.ls()