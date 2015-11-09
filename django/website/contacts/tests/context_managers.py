import contextlib
import pytest


@contextlib.contextmanager
def doesnt_raise(ExceptionClass, message=''):
    """
    This is a version of pytest.raises that checks that an exception isn't
    raised.
    """
    try:
        yield
    except ExceptionClass as e:
        error_message = message or e.message
        # TODO: Output the traceback of the original exception
        pytest.fail(error_message)
