#!/usr/bin/env python
# -*- coding: utf-8 -*-
import logging
import os
from logging.handlers import RotatingFileHandler
from lamp import config



class Logger(object):
    def __init__(self):
        logging.getLogger().setLevel(config.logger['level'])
        self.logger = logging.getLogger('lamp')
        self.logger.setLevel(config.logger['level'])
        log_file_dir = config.logger['path']
        if not os.path.exists(log_file_dir):
            os.mkdir(log_file_dir)

        formatter = logging.Formatter("[%(asctime)s] - %(name)s - %(levelname)s: %(message)s",
                                      "%Y-%m-%d %H:%M:%S")

        handler = RotatingFileHandler(
            os.path.join(log_file_dir, config.logger['file']), maxBytes=config.logger['maxBytes'], backupCount=config.logger['backupCount'])
        handler.setFormatter(formatter)
        self.logger.addHandler(handler)

        if config.logger['term_logger']:
            term_handler = logging.StreamHandler()
            term_handler.setFormatter(formatter)
            self.logger.addHandler(term_handler)


