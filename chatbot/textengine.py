import sys
import time

class TextEngine:
    @staticmethod
    def textengine(text, delay=0.05):
        """Print text character by character with an optional delay."""
        for ch in text:
            sys.stdout.write(ch)
            sys.stdout.flush()
            time.sleep(delay)
        print()
