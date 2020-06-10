# coding=utf-8
#
# catkin_lint
# Copyright (c) 2013-2020 Fraunhofer FKIE
#
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions
# are met:
#
#  * Redistributions of source code must retain the above copyright
#    notice, this list of conditions and the following disclaimer.
#  * Redistributions in binary form must reproduce the above copyright
#    notice, this list of conditions and the following disclaimer in the
#    documentation and/or other materials provided with the distribution.
#  * Neither the name of the Fraunhofer organization nor the names of its
#    contributors may be used to endorse or promote products derived from
#    this software without specific prior written permission.
#
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS
# IS" AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED
# TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A
# PARTICULAR PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT
# HOLDER OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL,
# SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED
# TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR
# PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF
# LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING
# NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS
# SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.

import unittest
from .helper import patch
import catkin_lint.util as util
import tempfile
import shutil
import os


def force_fail(*args, **kwargs):
    raise OSError("Mock fail")


class UtilTest(unittest.TestCase):
    def test_word_split(self):
        """Test word_split() utility function"""
        result = util.word_split("CamelCase")
        self.assertEqual(["camel", "case"], result)
        result = util.word_split("HTTPConnector")
        self.assertEqual(["http", "connector"], result)
        result = util.word_split("c_style_identifier")
        self.assertEqual(["c", "style", "identifier"], result)
        result = util.word_split("OpenSSL")
        self.assertEqual(["open", "ssl"], result)
        result = util.word_split("OGRE")
        self.assertEqual(["ogre"], result)
        result = util.word_split("getPS2Port")
        self.assertEqual(["get", "ps2", "port"], result)
        result = util.word_split("2BeOrNot2b")
        self.assertEqual(["2", "be", "or", "not2b"], result)
        result = util.word_split("C-3PO")
        self.assertEqual(["c", "3", "po"], result)
        result = util.word_split("c-3po")
        self.assertEqual(["c", "3po"], result)

    def test_is_sorted(self):
        """Test is_sorted() utility function"""
        self.assertTrue(util.is_sorted(["a", "b", "c", "d"]))
        self.assertFalse(util.is_sorted(["b", "a", "c", "d"]))
        self.assertFalse(util.is_sorted(["a", "c", "b", "d"]))
        self.assertFalse(util.is_sorted(["a", "b", "d", "c"]))

    def test_write_atomic(self):
        """Test write_atomic() utility function"""
        tmpdir = tempfile.mkdtemp()
        try:
            with patch("os.unlink", force_fail):
                with patch("os.rename", force_fail):
                    self.assertRaises(OSError, util.write_atomic, os.path.join(tmpdir, "test"), b"test")
                    self.assertFalse(os.path.exists(os.path.join(tmpdir, "test")))
        finally:
            shutil.rmtree(tmpdir, ignore_errors=True)
