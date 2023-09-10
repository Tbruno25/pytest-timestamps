import time
import pytest

def test_one():
    time.sleep(1)
    assert 1

@pytest.mark.skip 
def test_two():
    time.sleep(1)
    assert 1
    
def test_three():
    time.sleep(1)
    assert 1