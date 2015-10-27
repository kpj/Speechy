import os


class BaseCommand(object):
    def __init__(self):
        self.text = None

    def fire(self):
        raise NotImplementedError('Command must do something')

class MusicCommand(BaseCommand):
    def __init__(self):
        self.text = 'PLAY MUSIC'

    def fire(self):
        os.system('mplayer a_new_beginning.mp3')
