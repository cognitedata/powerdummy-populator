"""
Function for creating deterministing hashes

Examples:

    >>> string = "foo"
    >>> hash_seq = deterministic_hash(string)
    >>> print(hash_seq)
    00000000-0000-0000-acbd-18db4cc2f85c
"""
import hashlib
import uuid


def deterministic_sequence(string: str) -> int:
    """
    Make md5 hex

    Args:
        string:
            string to create unique sequence from


    Returns:
        hex representation of md5 hash of name
    """
    return int(hashlib.md5(string.encode("utf-8")).hexdigest()[:16], 16)


def deterministic_hash(string: str) -> str:
    """
    Create a deterministic hash

    Args:
        string:
            string to create unique hash from 


    Returns:
        uuid hex representation of md5 hash of name
    """
    return str(uuid.UUID(int=deterministic_sequence(string)))
