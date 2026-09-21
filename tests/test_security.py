import pytest
from backend.rate_limiter import RateLimiter
from backend.security import contains_malicious_content, sanitize_text, validate_conversation

def test_rate_limit():
    limiter = RateLimiter(2, 60); assert limiter.allow('x'); assert limiter.allow('x'); assert not limiter.allow('x')

def test_security_helpers():
    assert contains_malicious_content('<script>alert(1)</script>'); assert sanitize_text(' hi\x00 ') == 'hi'
    with pytest.raises(ValueError): validate_conversation([{'role': 'user', 'content': '<script>x</script>'}])
