"""
Deal with general setup stuff
"""

import threading

import gi
gi.require_version('Gst', '1.0')
from gi.repository import GObject, Gst


class Decoder(object):
    def __init__(self):
        """ Init all the gi things
        """
        GObject.threads_init()
        Gst.init(None)

        self.pipeline = None
        self.loopy = None
        self.command_list = []

    def add_command(self, Command):
        self.command_list.append(Command())

    def handle_result(self, hyp, conf=None):
        """ Handle results of pocketsphinx
        """
        if conf is None: # is partial result
            return

        for cmd in self.command_list:
            if cmd.text == hyp:
                cmd.fire()

    def setup_pipeline(self, lm_file, dic_file):
        """ Setup speech2text pipeline by setting parameters and adding callbacks
        """
        self.pipeline = Gst.parse_launch('alsasrc ! audioconvert ! audioresample ! pocketsphinx name=asr ! fakesink')

        asr = self.pipeline.get_by_name('asr')
        asr.set_property('lm', lm_file)
        asr.set_property('dict', dic_file)
        asr.set_property('configured', True)

        bus = self.pipeline.get_bus()
        bus.add_signal_watch()
        bus.connect('message::element', self.handle_bus_message)

    def handle_bus_message(self, bus, msg):
        """ Prefilter messages from pipeline bus
        """
        msgtype = msg.get_structure().get_name()
        if msgtype != 'pocketsphinx':
            return

        if msg.get_structure()['final']:
            self.handle_result(msg.get_structure()['hypothesis'], msg.get_structure()['confidence'])
        elif msg.get_structure()['hypothesis']:
            self.handle_result(msg.get_structure()['hypothesis'])

    def start(self):
        """ Run GObject main loop in seperate thread
        """
        self.pipeline.set_state(Gst.State.PLAYING)

        self.loopy = GObject.MainLoop()
        g_loop = threading.Thread(target=self.loopy.run)
        g_loop.daemon = True

        g_loop.start()
        return g_loop

    def stop(self):
        """ Shutdown everything
        """
        self.loopy.quit()


def get_decoder():
    decoder = Decoder()
    decoder.setup_pipeline('models/9149.lm', 'models/9149.dic')
    return decoder
