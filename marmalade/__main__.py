from marmalade.utils.logger import LOG
from marmalade.main import cli


try:
    cli.main()
except Exception as e:
    print("ERROR: {}".format(e))
