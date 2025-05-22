import structlog

def logger():
    structlog.configure(
    processors=[
        structlog.processors.JSONRenderer()
    ]
    )

    log = structlog.get_logger()

    return log

    # use cases
    #
    # log.debug("debug")
    # log.info("info")
    # log.warning("warning")
    # log.error("error")
    # log.critical("critical")
