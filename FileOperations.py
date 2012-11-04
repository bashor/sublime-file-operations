import sublime, sublime_plugin
import shutil
import os
from send2trash import send2trash

class EditFileCommand(sublime_plugin.WindowCommand):

  def run(self):
    branch = os.getenv("HOME")
    v = self.window.active_view()
    if v:
      branch, current_file = os.path.split(v.file_name())

    def on_done(leaf):
      self.window.open_file(os.path.join(branch, leaf))

    self.window.show_input_panel("Edit File:", branch + "/", on_done, None, None)

class RenameFileCommand(sublime_plugin.WindowCommand):

  def run(self):
    ask_for_name_relative_to_active_view(self.window, self.rename_and_retarget)

  def rename_and_retarget(self, src, dest):
    try:
      os.rename(src, dest)
      v = self.window.find_open_file(src)
      if v:
        v.retarget(dest)
    except:
      sublime.status_message("Unable to rename")

  def is_enabled(self):
      return self.window.active_view() != None

class DuplicateFileCommand(sublime_plugin.WindowCommand):

  def run(self):
    ask_for_name_relative_to_active_view(self.window, self.copy_and_open)

  def copy_and_open(self, src, dest):
    try:
      shutil.copy(src, dest)
      self.window.open_file(dest)
    except:
      sublime.status_message("Unable to copy")

  def is_enabled(self):
      return self.window.active_view() != None

class DeleteCurrentFileCommand(sublime_plugin.WindowCommand):

  def run(self):

    v = self.window.active_view()
    if v:
      send2trash(v.file_name())

  def is_enabled(self):
      return self.window.active_view() != None

class CopyNameCommand(sublime_plugin.TextCommand):
  def run(self, edit):
    if len(self.view.file_name()) > 0:
      sublime.set_clipboard(os.path.basename(self.view.file_name()))
      sublime.status_message("Copied file name")

  def is_enabled(self):
    return self.view.file_name() and len(self.view.file_name()) > 0

def ask_for_name_relative_to_active_view(window, on_done):
  old_path = window.active_view().file_name()
  branch, leaf = os.path.split(old_path)

  def on_input_given(new_leaf):
    new_path = os.path.join(branch, new_leaf)
    if old_path != new_path:
      on_done(old_path, new_path)

  show_input_panel_for_file_name(window, leaf, on_input_given)

def show_input_panel_for_file_name(window, placeholder, callback):
  v = window.show_input_panel("New Name:", placeholder, callback, None, None)
  name, ext = os.path.splitext(placeholder)
  v.sel().clear()
  v.sel().add(sublime.Region(0, len(name)))
