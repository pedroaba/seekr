from functools import wraps

from seekr.config import SeekrConfig
from seekr.texts.commit_disable_warning import CommitDisabledWarningText


def finish_command_execution(command):
    @wraps(command)
    def wrapper(self, namespace, *args, **kwargs):
        result = command(self, namespace, *args, **kwargs)
        if not hasattr(namespace, "no_commit"):
            return result

        if namespace.no_commit:
            CommitDisabledWarningText.display()
            return result

        has_execute_an_action = getattr(self, "has_execute_an_action", False)
        if has_execute_an_action:
            config = SeekrConfig.get_instance()
            config.commit()

        return result
    return wrapper
