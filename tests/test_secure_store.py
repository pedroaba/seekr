import unittest

from seekr.security.secure_store import SecureStore


class SecureStoreTest(unittest.TestCase):
    def setUp(self):
        pass

    def test_it_is_able_to_instantiate_a_secure_store(self):
        store = SecureStore()

        self.assertIsInstance(store, SecureStore)
        