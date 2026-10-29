#!/usr/bin/env python3
"""Exercise the Xiao UF2 packager's flash-boundary and vector checks."""

import contextlib
import importlib.util
import io
import pathlib
import struct
import tempfile
import unittest


spec = importlib.util.spec_from_file_location(
    "build_xiao", pathlib.Path(__file__).with_name("build-xiao.py")
)
build = importlib.util.module_from_spec(spec)
spec.loader.exec_module(build)


def block(address=0x27000, stack=0x20040000, reset=0x27021):
    data = bytearray(512)
    struct.pack_into("<8I", data, 0, 0x0A324655, 0x9E5D5157,
                     0x2000, address, 256, 0, 1, 0xADA52840)
    struct.pack_into("<II", data, 32, stack, reset)
    struct.pack_into("<I", data, 508, 0x0AB16F30)
    return data


class XiaoLayoutTest(unittest.TestCase):
    def verify(self, data):
        with tempfile.TemporaryDirectory() as directory:
            path = pathlib.Path(directory) / "firmware.uf2"
            path.write_bytes(data)
            with contextlib.redirect_stdout(io.StringIO()):
                build.validate_uf2(path)

    def test_valid_xiao_image(self):
        self.verify(block())

    def test_incompatible_or_incomplete_images(self):
        cases = {
            "standard S140 v6 address": block(0x26000),
            "journal overwrite": block(0x86000),
            "missing vector page": block(0x27100),
            "unaligned address": block(0x27001),
            "stack outside RAM": block(stack=0x10000000),
            "reset in SoftDevice": block(reset=0x26001),
            "reset beyond image": block(reset=0x28001),
            "non-Thumb reset": block(reset=0x27020),
            "truncated block": block()[:-1],
            "duplicate blocks": block() + block(),
            "empty image": b"",
        }
        wrong_family = block()
        struct.pack_into("<I", wrong_family, 28, 0x12345678)
        cases["wrong chip family"] = wrong_family
        for name, data in cases.items():
            with self.subTest(name=name), self.assertRaises(ValueError):
                self.verify(data)


if __name__ == "__main__":
    unittest.main()
