import logging
import os


def test_something() -> None:
    logging.info("entry: ...")
    assert "" != os.name
