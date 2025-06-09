import uvicorn
from ..utils.log import logger

def start_backend(app, **kwargs):
    logger.info('The PaddleNLP SimpleServer is starting, backend component uvicorn arguments as follows:')
    for key, value in kwargs.items():
        if key != 'log_config':
            logger.info('   the starting argument [{}]={}'.format(key, value))
    uvicorn.run(app, **kwargs)