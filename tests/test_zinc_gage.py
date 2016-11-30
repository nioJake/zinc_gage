from unittest.mock import patch
from collections import defaultdict
from nio.block.terminals import DEFAULT_TERMINAL
from nio.signal.base import Signal
from nio.testing.block_test_case import NIOBlockTestCase
from ..zinc_gage_block import ReadZincGage


class TestGageRead(NIOBlockTestCase):

    def test_default_read(self):
        blk = ReadZincGage()
        with patch('serial.Serial') as mock_serial:
            mock_serial.return_value.readline.return_value = b'sample response'
            mock_serial.return_value.isOpen.return_value = True
            self.configure_block(blk, {})
            blk.start()
        from time import sleep
        sleep(1)
        blk.stop()
        self.assertDictEqual(
            self.last_notified[DEFAULT_TERMINAL][0].to_dict(), {
            "bytes": b"sample response"
        })
        blk._serial.write.assert_called_with(b"O")
