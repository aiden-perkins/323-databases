
class Option:
    # Allow the action to be anything, rather than just a string.
    def __init__(self, prompt: str, action):
        """
        An option within a menu.
        :param prompt:  The text to tell the user what that selection will do.
        :param exec:    The code to be executed in response to that menu select.
        """
        self._prompt = prompt
        self._action = action

    @property
    def prompt(self) -> str:
        return self._prompt

    @property
    def action(self):
        return self._action

    def __str__(self):
        return f'prompt {self._prompt} calls for {self._action}'
