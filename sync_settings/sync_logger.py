# -*- coding: utf-8 -*-

from .libs.logger import Logger
import sublime

class SyncLogger:

  LOG_LEVEL_ERROR = 1
  LOG_LEVEL_WARNING = 2
  LOG_LEVEL_SUCCESS = 3

  @classmethod
  def log(cls, log_message, log_level):
    """Writes and show the log message to the user

    Arguments:
      log_message {dict|string}: The message to show
    """

    m = l = ''
    is_error = log_level == cls.LOG_LEVEL_ERROR

    if isinstance(log_message, Exception):
      log_message = log_message.to_json()
      m = log_message.get('app_message')
      l = '%s, File: %s - Line: %s' % (
        log_message.get('error_description'),
        log_message.get('filename'),
        log_message.get('line')
      )
      Logger.log(l, is_error)
    elif isinstance(log_message, str):
      m = log_message

    cls.__show_app_message('Sync Settings: %s' % (m), log_level)

  @classmethod
  def __show_app_message(cls, message, level):
    """Shows a popup with the specified message

    Arguments:
      message {str}: Message to show
      level {int}: Log type
    """

    ST_MIN_VERSION = 3070

    if (int(sublime.version()) >= ST_MIN_VERSION):
      cls.show_popup(message, level)
    else:
      sublime.status_message(message)

  @classmethod
  def show_popup(cls, content, level):
    """Show a popup using the sublime API

    Arguments:
      content {string}: Message to show
      level {int}: Log type
    """

    current_view = sublime.active_window().active_view()
    message = cls.get_message_template(content, level)

    current_view.show_popup(content=message, max_width=400)

  @classmethod
  def get_message_template(cls, message, type):
    """Generates a template using HTML tags

    Arguments:
      message {string}: Message to render
      type {int}: Log type
    """

    if (type == cls.LOG_LEVEL_WARNING):
      message = '<div class = "warning">👉 - %s</div>' % (message)
    elif (type == cls.LOG_LEVEL_ERROR):
      message = '<div class = "error">💩 - %s</div>' % (message)
    elif (type == cls.LOG_LEVEL_SUCCESS):
      message = '<div class = "success">⚡️ - %s</div>' % (message)

    return '''
      <style>
        body {
          margin: 0;
          font-size: 16px;
        }

        div {
          padding: 10px 15px;
        }

        div.success {
          color: #43783b;
          background-color: #ace1ae;
        }

        div.warning {
          color: #9c9759;
          background-color: #f6f0a6;
        }

        div.error {
          background-color: #f89d9d;
          color: #751414;
        }
      </style>

      %s
    ''' % (message)
