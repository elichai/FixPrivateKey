__author__ = 'elichai2'
import unittest

from FixPrivateKey import (
    query_yes_no,
    swap_letters,
    check_duplicated_letters,
    check,
    check_length,
    change_letter
)


class TestUM(unittest.TestCase):

    def setUp(self):
        pass

    def test_swap_letters_right_key_compressed(self):
        self.assertEqual(swap_letters('Kwa6YeQwdScVwTvLjiPFonNMPqWFi58wUFvhLp7tWxY2Q9PCj5ji'),
                         'Kwa6YeQwdScVwTvLjiPFonNMPqWFi58wUFvhLp7tWxY2Q9PCj5ji')

    def test_swap_letters_right_key_uncompressed(self):
        self.assertEqual(swap_letters('5KMrSWx9EeNEtShQf5cL7hSAUSi846YKCwvzjSxdamzbsaPCJKs'),
                         '5KMrSWx9EeNEtShQf5cL7hSAUSi846YKCwvzjSxdamzbsaPCJKs')

    def test_swap_letters_swapped_key_compressed(self):
        self.assertEqual(swap_letters('L29UT6bAToznQioxpCpp8Cmq82xYL2VVGTvdt81Wk5gUZi5aqiUx'),
                         'L29UT6bAToznQioxpCppC8mq82xYL2VVGTvdt81Wk5gUZi5aqiUx')

    def test_swap_letters_swapped_key_uncompressed(self):
        self.assertEqual(swap_letters('5KkQCnGwvv3HxxeQudv4iXeArCqmXxjLLj81AumnpfxpHzUMpTv'),
                         '5KkQCnGwvv3HxxeQudvi4XeArCqmXxjLLj81AumnpfxpHzUMpTv')

    def test_swap_letters_broken_key_compressed(self):
        self.assertEqual(swap_letters('KxKUFSro9ZPUzYEtkeqbeGQvKcuDyMmNx123S8sVndJUGZx2ycwh'), None)

    def test_swap_letters_broken_key_uncompressed(self):
        self.assertEqual(swap_letters('5Jw2gu1w123gjz3wLJdfLHiRVnJZvhfdK1D9ovhSmemHfkT2drJ'), None)
# ------------------------------------------------------------------

    def test_check_right_key(self):
        self.assertEqual(check('5JTuiZmyxAQ67TRazkBGfz7dQANv7cXvDVFJWfYSRgnFUTL92Re'), True)

    def test_check_broken_key(self):
        self.assertEqual(check('5JTuiZmyxAQ67TRazkBGfz7dQ123312VFJWfYSRgnFUTL92Re'), False)

    def test_check_not_a_key(self):
        self.assertEqual(check('foo123'), False)
# ------------------------------------------------------------------

    def test_check_length_right_key_compressed(self):
        self.assertEqual(check_length(list('L3S2FNWzD688jp8xKXQ1cavnvuDKhdBUMYirASC3osVvjPTCMQ61')),
                         list('L3S2FNWzD688jp8xKXQ1cavnvuDKhdBUMYirASC3osVvjPTCMQ61'))

    def test_check_length_right_key_uncompressed(self):
        self.assertEqual(check_length(list('5KkMwrfDDU4Bp7NWdXmyaoAoXYskLpAqVUB84YyL5BeSTW9FQQH')),
                         list('5KkMwrfDDU4Bp7NWdXmyaoAoXYskLpAqVUB84YyL5BeSTW9FQQH'))

    def test_check_length_short_key_compressed(self):
        self.assertEqual(check_length(list('KxA9mGyYG2CL6yNTmEDyErMBveUQytUGyghyTGYzNaGTCM7NFzr'), lambda: "yes"),
                         list('KxA9mGyYG2CL6yNTmEDyErMBveUQytUGyghyTGYzNaGTCM7NFzr1'))

    def test_check_length_short_key_uncompressed(self):
        self.assertEqual(check_length(list('5KbRM2s4VJVYv9EfsMGxE4YuhsXjY9DLr79Ak4VNsEx2fpc3o1'), lambda: "yes"),
                         list('5KbRM2s4VJVYv9EfsMGxE4YuhsXjY9DLr79Ak4VNsEx2fpc3o11'))

    def test_check_length_long_key_compressed(self):
        self.assertEqual(check_length(list('L3Pc8gzDWRurLpxE2jJ6SWDyiJLmyexA5jWRz1TJzR9jZSjqjiuf1'), lambda: "yes"),
                         list('L3Pc8gzDWRurLpxE2jJ6SWDyiJLmyexA5jWRz1TJzR9jZSjqjiuf'))

    def test_check_length_long_key_uncompressed(self):
        self.assertEqual(check_length('5J5gXTX1KBJht7ChLGHB9NVzcveaZvkGq4Z2mFrYEyuDchAK4za1', lambda: "yes"),
                         list('5J5gXTX1KBJht7ChLGHB9NVzcveaZvkGq4Z2mFrYEyuDchAK4za'))

    def test_check_length_long_duplicated_key_uncompressed(self):
        self.assertEqual(check_length('5JvnZeWnGrG9AsxhJzwqTkpPEU8Q5KpPNF1cRJ3WzsZEgWxyyB6u', lambda: "duplicated"),
                         list('5JvnZeWnGrG9AsxhJzwqTkpPEU8Q5KpPNF1cRJ3WzsZEgWxyB6u'))

    def test_check_length_long_duplicated_key_compressed(self):
        self.assertEqual(check_length(list('KxjWGnwHr2DdfBarW2y4emPq1pp9XCLih9sVig2cF8JUts1rKZTYG'), lambda: "duplicated"),
                         list('KxjWGnwHr2DdfBarW2y4emPq1p9XCLih9sVig2cF8JUts1rKZTYG'))
# ------------------------------------------------------------------

    def test_change_letter_right_key_compressed(self):
        self.assertEqual(change_letter('L2NdgGDMb6RmX6CoCRrXRPyfr1q8jBBa3jkSjHhU39HxXReCrHr8'),
                         'L2NdgGDMb6RmX6CoCRrXRPyfr1q8jBBa3jkSjHhU39HxXReCrHr8')

    def test_change_letter_right_key_uncompressed(self):
        self.assertEqual(change_letter('5KNUh7ypiA3xQ4ZZwvz64kPjkjUBvD8NBU3FE4nxnBu4VobE7ee'),
                         '5KNUh7ypiA3xQ4ZZwvz64kPjkjUBvD8NBU3FE4nxnBu4VobE7ee')

    def test_change_letter_changed_compressed(self):
        self.assertEqual(change_letter('L433DdCPMDvkJ4RMR5LwNZU4p8UW8fTDMj2KpMaYU5bEusr9PcUq'),
                         'L433DdCPMDvkJ4RMR5LwNZU4p8UW8fTDMjTKpMaYU5bEusr9PcUq')

    def test_change_letter_changed_uncompressed(self):
        self.assertEqual(change_letter('5KBAYGwSZMU4b7ZPiuXXqjcatskoU3kM2azx6wyqn6N1B1nEobE'),
                         '5KBAYGwSZMU4a7ZPiuXXqjcatskoU3kM2azx6wyqn6N1B1nEobE')

    def test_change_letter_broken_compressed(self):
        self.assertEqual(change_letter('L2G8duFU7acvyxUiJd22sYurYW123TqFKambknhp2cYyvQiijWw8'), '\nCouldn\'t find any result')

    def test_change_letter_broken_uncompressed(self):
        self.assertEqual(change_letter('5K8urwsDdSrer52uNiXxw2YqAJ9owpNJVU3fQZpi4ThUNneM8PA'), '\nCouldn\'t find any result')

    # this test takes ~50 seconds
    def test_change_letter_changed_2_letters_compressed(self):
        self.assertEqual(change_letter('L2G8duFU7a1vyxUiJdBjsYurYWnRzTqFKambknhp2cY2vQiijWw8', 2),
                         'L2G8duFU7aSvyxUiJdBjsYurYWnRzTqFKambknhp2cYyvQiijWw8')



if __name__ == '__main__':
    unittest.main()