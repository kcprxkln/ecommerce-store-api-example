import logging

class APILogger:
    def __init__(self, log_file):
        self.logger = logging.getLogger(__name__)
        self.logger.setLevel(logging.DEBUG)

        file_handler = logging.FileHandler(log_file)
        file_handler.setLevel(logging.DEBUG)

        formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
        file_handler.setFormatter(formatter)

        self.logger.addHandler(file_handler)

    def log_request(self, method, status_code, endpoint):
        log_msg = f"[{status_code}] {method}: {endpoint}"
        if status_code == 200:
            self.logger.info(log_msg)
            
        else:
            self.logger.error(log_msg)