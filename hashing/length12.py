import hashlib
import itertools
from tqdm import tqdm

def hash_cap_file(filename, algorithm="sha256"):
    hash_func = getattr(hashlib, algorithm)()
    with open(filename, "rb") as f:
        while chunk := f.read(8192):
            hash_func.update(chunk)
    return hash_func.hexdigest()

def run(pcap_file, found_event):
    print("[*] Trying length 12")
    target_hash = hash_cap_file(pcap_file)

    charset = (
        "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789"
        + r"""!"#$%&'()*+,-./:;<=>?@[\]^_`{|}~"""
    )

    for attempt in tqdm(itertools.product(charset, repeat=12), desc="Length 12"):
        if found_event.is_set():
            return None  # Exit early

        candidate = ''.join(attempt)
        candidate_hash = hashlib.sha256(candidate.encode()).hexdigest()

        if candidate_hash == target_hash:
            return candidate

    return None
