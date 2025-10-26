import logging


logging.basicConfig(
    level=logging.ERROR,
    format="%(asctime)s - %(levelname)s - %(message)s",
    handlers=[
        logging.FileHandler("app/errors.log", encoding="utf-8"),
    ],
)

logger = logging.getLogger()
