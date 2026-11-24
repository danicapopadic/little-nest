from pwdlib import PasswordHash

from little_nest.security import hash_password


def test_hash_password():
    password = "test-password-123"
    hashed_password = hash_password(password)

    assert hashed_password != password
    assert hashed_password.startswith("$argon2id$")
    assert PasswordHash.recommended().verify(password, hashed_password)
