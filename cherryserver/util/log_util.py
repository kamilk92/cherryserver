import logging.config

import yaml


def setup_logging(log_file):
    with open(log_file) as logging_config_file:
        config = yaml.safe_load(logging_config_file.read())
    logging.config.dictConfig(config)
