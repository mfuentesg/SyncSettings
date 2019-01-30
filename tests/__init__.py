import sys
from .mocks import sublime_mock

sys.modules['sublime'] = sublime_mock
