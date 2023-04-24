import io
import unittest
import sys

import xml.etree.ElementTree as ET

sys.path.append("./src")
sys.path.append("./src/objit")
from objit import objit


class ObjitTest(unittest.TestCase):
    namespaces = {
        "inkscape": "http://www.inkscape.org/namespaces/inkscape",
        "sodipodi": "http://sodipodi.sourceforge.net/DTD/sodipodi-0.dtd",
        "": "http://www.w3.org/2000/svg",
        "svg": "http://www.w3.org/2000/svg",
    }

    def test_dimension_embedding(self):
        for v in (0, 0.5, 0.99):
            with self.subTest(v=v):
                actual = objit.embed(v + 1e-6)
                expected = objit.embed(v - 1e-6)
                self.assertTrue(
                    actual.is_close(expected, 0.01, 0.01),
                    f"{actual} != {expected}",
                )

    def test_1(self):
        output = io.BytesIO()
        root = ET.parse("test1.svg")
        selection = [
            f"--id={e.get('id')}" for e in root.findall(".//use", self.namespaces)[:1]
        ]

        args = ["./test1.svg"] + selection
        print(args)
        objit.Objit().run(args, output)
