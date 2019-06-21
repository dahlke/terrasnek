from tfepy.api import TFE
import os

TFE_TOKEN = os.getenv("TFE_TOKEN", None)

if __name__ == "__main__":
    api = TFE(TFE_TOKEN)