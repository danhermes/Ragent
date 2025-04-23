import logging
import unicodedata

def enable_strict_logging():
    def strict_log(self, msg, *args, **kwargs):
        bad_chars = [c for c in str(msg) if unicodedata.category(c)[0] == 'C']
        if bad_chars:
            hex_chars = ', '.join(f'U+{ord(c):04X}' for c in bad_chars)
            #raise ValueError(f"Unprintable control characters in log message: {hex_chars}")
        self._original_info(msg, *args, **kwargs)

    logging.Logger._original_info = logging.Logger.info
    logging.Logger.info = strict_log
