from rich.console import Console
import logging
from rich.logging import RichHandler

# Generic console
console = Console()

# Logs
def logger():
    logging.basicConfig(
        level="NOTSET",
        format="%(message)s",
        datefmt="[%X]",
        handlers=[RichHandler(rich_tracebacks=True)]
    )

    log = logging.getLogger("rich")

    return log