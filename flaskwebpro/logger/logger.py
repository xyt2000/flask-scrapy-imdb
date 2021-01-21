import logging

logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(name)s - %(levelname)s - %(message)s")

logger = logging.getLogger("syslogger")

formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")
fileHandler = logging.FileHandler("log.log")
fileHandler.setFormatter(formatter)
fileHandler.setLevel(logging.INFO)

logger.addHandler(fileHandler)

conHandler = logging.StreamHandler()
conHandler.setFormatter(formatter)
conHandler.setLevel(logging.INFO)
logger.addHandler(conHandler)