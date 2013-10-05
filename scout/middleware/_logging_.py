import logging
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

class Middleware(object):
    def process(self, job):
        logger.debug('Calling method %s. args=%r, kwargs=%r' % (job['method'], job['args'], job['kwargs']))

    def exception(self):
        pass