import logging


def setup_logger(name, log_file, level=logging.INFO):
    """Function to setup as many loggers as you want"""

    # 创建一个logger
    logger = logging.getLogger(name)
    logger.setLevel(level)

    # 创建用于写入日志文件的handler
    file_handler = logging.FileHandler(log_file)
    file_handler.setFormatter(logging.Formatter('%(asctime)s - %(levelname)s | %(message)s'))

    # 创建用于输出到控制台的handler
    console_handler = logging.StreamHandler()
    console_handler.setFormatter(logging.Formatter('%(asctime)s - %(levelname)s | %(message)s'))

    # 添加handlers到logger
    logger.addHandler(file_handler)
    logger.addHandler(console_handler)

    return logger

