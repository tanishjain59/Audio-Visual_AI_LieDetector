import logging
import sys
import traceback

from VideoRecognition import ExtractEmotionFromVideoProcessor
from splitmedia import SplitMediaProcessor
from audiotranscription import ExtractTextFromAudioProcessor
from audiosplitter import AudioSplitter
from audioemotiondetector import ExtractEmotionFromAudioProcessor
from scoringsystem import ScoringSystem

def main():
    SplitMediaProcessor().run()
    ExtractEmotionFromVideoProcessor().run()
    AudioSplitter().run()
    ExtractTextFromAudioProcessor().run()
    ExtractEmotionFromAudioProcessor().run()
    ScoringSystem().run()

    return


if __name__ == '__main__':
    logging.basicConfig(
        format='%(asctime)s [%(levelname)s]: %(message)s',
        level=logging.INFO,
        datefmt='%m/%d/%Y %I:%M:%S %p'
    )
    exit_code = 0
    try:
        main()
    except Exception as ex:
        exc_type, exc_value, exc_traceback = sys.exc_info()
        print(f"******* Exception : {exc_value} *******")
        traceback.print_tb(exc_traceback)
        logging.exception(exc_value)
        exit_code = -1

    exit(exit_code)
