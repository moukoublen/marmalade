from marmalade.main import cli
from marmalade import LOG
import traceback

try:
    cli.main()
except Exception as e:
    LOG.error(e)
    traceback.print_exc()
