import logging
import os
import sys
import threading

try:
    import snowboydecoder
except ImportError:
    import snowboy.snowboydecoder as snowboydecoder


class HotwordService(threading.Thread):
    """
    Hotword service that triggers assistant interaction upon recognized speech.

    Dependencies installation::

        ``pip install snowboy``

    You will also need a voice model for the hotword detection. You can find
    some under the ``resources/models`` directory of the Snowboy repository,
    or train/download other models from https://snowboy.kitt.ai.
    """

    def __init__(self, model, assistant, sensitivity=0.5, audio_gain=1.0):
        """
        :param model: Path to the voice model file. See https://snowboy.kitt.ai/ for training/downloading models.
        :type model: str

        :param assistant: Instance of :class:`assistant.Assistant` that will be invoked upon detected hotword.
        :type assistant: assistant.Assistant

        :param sensitivity: Model sensitivity for hotword detection between 0 and 1 (default: 0.5)
        :type sensitivity: float

        :param audio_gain: Audio gain. Default: 1.0
        :type audio_gain: float
        """

        super().__init__()
        self.model_file = os.path.abspath(os.path.expanduser(model))
        self.assistant = assistant
        self.sensitivity = sensitivity
        self.audio_gain = audio_gain
        self.logger = logging.getLogger(__name__)
        self.logger.addHandler(logging.StreamHandler(sys.stdout))

        self.detector = snowboydecoder.HotwordDetector(self.model_file,
                                                       sensitivity=self.sensitivity,
                                                       audio_gain=self.audio_gain)

        self.logger.info('Initialized hotword detection service')

    def hotword_detected(self):
        """
        Callback called on hotword detection
        """
        def callback():
            self.logger.info('Hotword detected')
            self.assistant.start_conversation()

        return callback

    def run(self):
        super().run()
        self.detector.start(detected_callback=self.hotword_detected())


# vim:sw=4:ts=4:et:
