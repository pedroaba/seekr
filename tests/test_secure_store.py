import subprocess
import unittest
from contextlib import contextmanager
from unittest.mock import Mock, patch

from keyring.errors import KeyringError

from seekr.security.secure_store import SecureStore


class SecureStoreTest(unittest.TestCase):
    def setUp(self):
        self.__service = "seekr-test-service"
        self.__username = "seekr-test-user"
        self.__value = "secret-value"

    @contextmanager
    def __patched_secure_store_dependencies(self):
        with (
            patch("seekr.security.secure_store.getuser", return_value=self.__username),
            patch("seekr.security.secure_store.subprocess.run") as diagnose,
            patch("seekr.security.secure_store.keyring") as keyring,
        ):
            diagnose.return_value = Mock(stdout="keyring diagnose ok")
            yield diagnose, keyring

    def test_it_is_able_to_instantiate_a_secure_store(self):
        with self.__patched_secure_store_dependencies() as (diagnose, _):
            store = SecureStore()

        self.assertIsInstance(store, SecureStore)
        diagnose.assert_called_once()

    def test_it_able_to_save_a_value_on_secure_store(self):
        with self.__patched_secure_store_dependencies() as (_, keyring):
            store = SecureStore()

            result = store.set(self.__service, self.__value)

        self.assertTrue(result)
        keyring.set_password.assert_called_once_with(
            self.__service,
            self.__username,
            self.__value,
        )

    def test_it_is_able_to_get_a_value_from_secure_store(self):
        with self.__patched_secure_store_dependencies() as (_, keyring):
            keyring.get_password.return_value = self.__value
            store = SecureStore()

            result = store.get(self.__service)

        self.assertEqual(self.__value, result)
        keyring.get_password.assert_called_once_with(self.__service, self.__username)

    def test_it_is_able_to_update_a_value_on_secure_store(self):
        updated_value = "updated-secret-value"

        with self.__patched_secure_store_dependencies() as (_, keyring):
            store = SecureStore()

            result = store.update(self.__service, updated_value)

        self.assertTrue(result)
        keyring.set_password.assert_called_once_with(
            self.__service,
            self.__username,
            updated_value,
        )

    def test_it_is_able_to_delete_a_value_from_secure_store(self):
        with self.__patched_secure_store_dependencies() as (_, keyring):
            store = SecureStore()

            result = store.delete(self.__service)

        self.assertTrue(result)
        keyring.delete_password.assert_called_once_with(
            self.__service,
            self.__username,
        )

    def test_it_returns_false_when_secure_store_cannot_save_a_value(self):
        with (
            self.__patched_secure_store_dependencies() as (_, keyring),
            patch("builtins.print") as display_error,
        ):
            keyring.set_password.side_effect = RuntimeError("keyring failure")
            store = SecureStore()

            result = store.set(self.__service, self.__value)

        self.assertFalse(result)
        display_error.assert_called_once()

    def test_it_returns_false_when_secure_store_cannot_update_a_value(self):
        with (
            self.__patched_secure_store_dependencies() as (_, keyring),
            patch("builtins.print") as display_error,
        ):
            keyring.set_password.side_effect = RuntimeError("update failure")
            store = SecureStore()

            result = store.update(self.__service, self.__value)

        self.assertFalse(result)
        display_error.assert_called_once()

    def test_it_returns_false_when_secure_store_cannot_delete_a_value(self):
        with (
            self.__patched_secure_store_dependencies() as (_, keyring),
            patch("builtins.print") as display_error,
        ):
            keyring.delete_password.side_effect = RuntimeError("delete failure")
            store = SecureStore()

            result = store.delete(self.__service)

        self.assertFalse(result)
        display_error.assert_called_once()

    def test_it_raises_runtime_error_when_keyring_diagnose_command_fails(self):
        diagnose_error = subprocess.CalledProcessError(
            returncode=1,
            cmd=["python", "-m", "keyring", "diagnose"],
            stderr="diagnose failure",
        )

        with (
            patch("seekr.security.secure_store.subprocess.run") as diagnose,
            patch(
                "seekr.security.secure_store.KeyringTroubleshootingText.display",
            ) as display_troubleshooting,
        ):
            diagnose.side_effect = diagnose_error

            with self.assertRaisesRegex(RuntimeError, "Keyring diagnose failed."):
                SecureStore()

        display_troubleshooting.assert_called_once_with(
            error=str(diagnose_error),
            diagnose_output="diagnose failure",
        )

    def test_it_raises_runtime_error_when_keyring_backend_fails_during_diagnose(self):
        with (
            patch("seekr.security.secure_store.subprocess.run") as diagnose,
            patch(
                "seekr.security.secure_store.KeyringTroubleshootingText.display",
            ) as display_troubleshooting,
        ):
            diagnose.side_effect = KeyringError("backend failure")

            with self.assertRaisesRegex(RuntimeError, "Keyring backend failed."):
                SecureStore()

        display_troubleshooting.assert_called_once_with(error="backend failure")

    def test_it_raises_error_when_secure_store_cannot_get_a_value(self):
        with self.__patched_secure_store_dependencies() as (_, keyring):
            keyring.get_password.side_effect = RuntimeError("get failure")
            store = SecureStore()

            with self.assertRaisesRegex(RuntimeError, "get failure"):
                store.get(self.__service)
