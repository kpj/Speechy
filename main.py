import time

import utils
from pipeliner import get_decoder


dec = get_decoder()
loop = dec.start()

cmds = utils.get_available_commands()
dec.add_command(cmds[0])

loop.join()
