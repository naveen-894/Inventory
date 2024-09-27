from datetime import datetime
import logging


def api_logging(log_data):
    """
    Function used to log all the API requests and responses along with error if any.
    Creates log files on daily basis.
    Params:
    1. log_data: list of individual logs having log type and message.
    """
    # Create Log file in logs folder:
    log_dir = 'logs'
    logging.basicConfig(
        filename=f"{log_dir}/api_requests_{datetime.now().date()}.log", level=logging.DEBUG)
    try:
        for log in log_data:
            message = log.split("||")
            if message[0] == 'info':
                logging.info(message[1])
            else:
                logging.error(message[1])
    except Exception as e:
        logging.error(f"Log function error: {str(e)}")
    logging.info("=" * 150)
    return True