# -*- coding: utf-8 -*-
#Credits to @wbond package_control

import sublime, threading

class ThreadProgress():

  """
    Animates an indicator, [=   ], in the status area while a thread runs

    :param thread:
      The thread to track for activity

    :param message:
      The message to display next to the activity indicator

    :param success_message:
      The message to display once the thread is complete
  """

  def __init__(self, thread_target, message, success_message):
    self.message = message
    self.success_message = success_message
    self.addend = 1
    self.size = 8
    self.last_view = None
    self.window = None

    self.thread = threading.Thread(target=thread_target)
    self.thread.start()
    sublime.set_timeout(lambda: self.run(0), 100)

  def run(self, i):
    if self.window is None:
      self.window = sublime.active_window()
    active_view = self.window.active_view()

    if self.last_view is not None and active_view != self.last_view:
      self.last_view.erase_status('_sync_settings')
      self.last_view = None

    if not self.thread.is_alive():
      active_view.erase_status('_sync_settings')
      return

    before = i % self.size
    after = (self.size - 1) - before

    active_view.set_status('_sync_settings', '%s [%s=%s]' % (self.message, ' ' * before, ' ' * after))
    if self.last_view is None:
      self.last_view = active_view

    if not after:
      self.addend = -1
    if not before:
      self.addend = 1
    i += self.addend

    sublime.set_timeout(lambda: self.run(i), 100)
