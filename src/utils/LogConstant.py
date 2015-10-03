import logging
import logging.config

__author__ = 'Sapocaly'

logging.config.fileConfig("conf/byyy_ba_logger.cfg")


DAL_DIGEST_LOGGER = logging.getLogger("sapocaly_dal")
DAL_DIGEST_LOGGER_ERROR = logging.getLogger("sapocaly_dal.err")
