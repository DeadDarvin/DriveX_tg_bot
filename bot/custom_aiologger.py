import aiologger
from tempfile import NamedTemporaryFile

def get_custom_loger(name: str) -> aiologger.Logger:
    """Logger wrapper"""
    handler = logging.FileHandler(f"{name}.log", mode="w")
    formater = logging.Formatter("%(name)s %(asctime)s %(levelname)s %(message)s")
    console_out = logging.StreamHandler()

    logger = logging.getLogger(name)
    logger.setLevel(logging.DEBUG)

    handler.setFormatter(formater)
    logger.addHandler(handler)
    logger.addHandler(console_out)

    return logger