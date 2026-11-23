"""THE HARBOUR LIGHT kepunyaan @oktaviascreamo0243 (Akun 13) — NI22 Wave 7.

Seperti lampu pelabuhan, edisi ini memberi penanda jelas di tengah
banjir kabar yang datang bertubi-tubi sejak pagi. Programnya menjaga satu hal saja: gambar yang dikirim
harus lolos cek ukuran dan tersalin persis sama ke tempat tujuan.
"""

import hashlib
import os
import shutil
import struct
import sys
from pathlib import Path

CONCEPT = "THE HARBOUR LIGHT"
ACCOUNT = "@oktaviascreamo0243"
ACCOUNT_LABEL = "Akun 13"
BOUNTY = "news-image-20261122"
STORIES = 36
MAX_SIDE = 1024

EXPECTED_MAGIC = bytes([0x89, 0x50, 0x4E, 0x47, 0x0D, 0x0A, 0x1A, 0x0A])


def die(text):
    print(f"ditolak: {text}", file=sys.stderr)
    raise SystemExit(1)


def start():
    base = Path(__file__).resolve().parent
    pic = base / "entry.png"
    if not pic.is_file():
        die("entry.png tidak ada")

    prefix = pic.read_bytes()[:33]
    if len(prefix) < 33:
        die("berkas kependekan, header PNG tidak lengkap")
    if prefix[:8] != EXPECTED_MAGIC:
        die("magic bytes bukan PNG")
    if prefix[12:16] != b"IHDR":
        die("chunk pertama bukan IHDR")
    lebar, tinggi = struct.unpack(">II", prefix[16:24])
    if lebar > MAX_SIDE or tinggi > MAX_SIDE:
        die(f"sisi {lebar}x{tinggi} melebihi {MAX_SIDE}")

    blob = pic.read_bytes()
    nbytes = len(blob)
    checksum = hashlib.sha256(blob).hexdigest()

    folder_out = Path(os.environ.get("MAKEFUN_OUTPUT_DIR", "/output"))
    folder_out.mkdir(parents=True, exist_ok=True)
    hasil = folder_out / "entry.png"
    shutil.copyfile(pic, hasil)

    check = hasil.read_bytes()
    if len(check) != nbytes or hashlib.sha256(check).hexdigest() != checksum:
        die("salinan di output tidak identik")

    print(f"Concept: {CONCEPT}")
    print(f"Account: {ACCOUNT} ({ACCOUNT_LABEL})")
    print(f"Bounty: {BOUNTY}")
    print("File: entry.png")
    print(f"Size: {nbytes}")
    print(f"Dim: {lebar}x{tinggi}")
    print(f"SHA256: {checksum}")
    print(f"Stories: {STORIES}")
    print("Copy verified byte-identical.")
    return 0


if __name__ == "__main__":
    sys.exit(start())
