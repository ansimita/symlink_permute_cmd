# Copyright (c) 2020 ansimita
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

from pathlib import Path

import errno
import shutil
import subprocess
import unittest


def generate_args_bin(command):
    bin = Path.home() / 'bin'
    if not bin.exists() or not bin.is_dir():
        bin = Path.home() / '.local' / 'bin'
    return (['./symlink_permute_cmd', command], bin)


def run(args):
    return subprocess.run(args, capture_output=True, text=True)


class SymlinkPermuteTests(unittest.TestCase):

    def test_fail_if_command_not_found(self):
        r = run(['./symlink_permute_cmd', 'foo'])
        self.assertEqual(r.returncode, 127)
        self.assertEqual(r.stderr, 'foo: command not found\n')

    def test_symlink(self):
        if shutil.which('sl'):
            print(" 'sl' command exists. Skipping test_symlink.")
            return

        args, bin = generate_args_bin('ls')

        r = run(args)
        self.assertEqual(r.returncode, 0)

        link = bin / 'sl'
        self.assertTrue(link.exists())
        self.assertEqual(link.resolve(), Path('/bin/ls'))

        link.unlink()

    def test_symlink_absolute_path(self):
        if shutil.which('mr'):
            print(" 'mr' command exists."
                  ' Skipping test_symlink_absolute_path.')
            return

        args, bin = generate_args_bin('/bin/rm')

        r = run(args)
        self.assertEqual(r.returncode, 0)

        link = bin / 'mr'
        self.assertTrue(link.exists())
        self.assertEqual(link.resolve(), Path('/bin/rm'))

        link.unlink()

    def test_skip_existing_command(self):
        if shutil.which('vm'):
            print(" 'vm' command exists."
                  ' Skipping test_skip_existing_command.')
            return

        args, bin = generate_args_bin('mv')

        r = run(args)
        self.assertEqual(r.returncode, 0)

        link = bin / 'vm'
        self.assertTrue(link.exists())
        self.assertEqual(link.resolve(), Path('/bin/mv'))

        r = run(['./symlink_permute_cmd', 'vm'])
        self.assertEqual(r.returncode, 0)
        self.assertEqual(r.stdout, "'mv' command exists. Skipping...\n")

        link.unlink()

    def test_specified_symlink_at(self):
        if shutil.which('hs'):
            print(" 'hs' command exists."
                  ' Skipping test_specified_symlink_at.')
            return

        symlink_at = Path('/tmp')

        r = run(['./symlink_permute_cmd', 'sh', '-s', f'{symlink_at}'])
        self.assertEqual(r.returncode, 0)

        link = symlink_at / 'hs'
        self.assertTrue(link.exists())
        self.assertEqual(link.resolve(), Path('/bin/sh'))

        link.unlink()

    def test_specified_symlink_at_nonexistent_dir(self):
        if shutil.which('pc'):
            print(" 'pc' command exists."
                  ' Skipping test_specified_symlink_at_nonexistent_dir.')
            return

        symlink_at = Path('/tmp/foo')
        self.assertFalse(symlink_at.exists())

        r = run(['./symlink_permute_cmd', 'cp', '-s', f'{symlink_at}'])
        self.assertEqual(r.returncode, 0)

        link = symlink_at / 'pc'
        self.assertTrue(link.exists())
        self.assertEqual(link.resolve(), Path('/bin/cp'))

        link.unlink()
        symlink_at.rmdir()

    def test_specified_symlink_at_not_dir(self):
        symlink_at = Path('/tmp/bar')
        symlink_at.touch()

        r = run(['./symlink_permute_cmd', 'dd', '-s', f'{symlink_at}'])
        self.assertEqual(r.returncode, errno.ENOTDIR)
        self.assertEqual(r.stderr, f'{symlink_at}:'
                         ' Specified symlink at path exists but is'
                         ' not a directory\n')

        self.assertFalse(Path('/tmp/bar/dd').exists())

        symlink_at.unlink()


if __name__ == '__main__':
    unittest.main()
