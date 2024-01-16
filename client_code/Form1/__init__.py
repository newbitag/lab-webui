from ._anvil_designer import Form1Template
from anvil import *
import anvil.server
import anvil.google.auth, anvil.google.drive
from anvil.google.drive import app_files
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables
import anvil.users
from ..Home import Home
from ..Project import Project

class Form1(Form1Template):
  def __init__(self, **properties):
    # Set Form properties and Data Bindings.
    self.init_components(**properties)
    anvil.users.login_with_form()
    # Any code you write here will run before the form opens.
    self.user_banner.text = anvil.users.get_user()['email']

    
    self.content_panel.clear()
    self.content_panel.add_component(Home())
    list_of_projects = anvil.server.call('get_user_projects',anvil.users.get_user()['email'])
    for project in list_of_projects:
      tmp_button = Button(text=project)
      self.navigation_bar.add_component(tmp_button)
      tmp_button.add_event_handler('click',self.project_button_clicked)
  


  def logout_button_handler(self, **event_args):
    anvil.users.logout()
    anvil.users.login_with_form()

  def project_button_clicked(self, **event_args):
    project_name = event_args['sender'].text
    self.content_panel.clear()
    self.content_panel.add_component(Project(project_name))
    self.highlight_tab_button(event_args['sender'])

  def home_button_clicked(self, **event_args):
    self.content_panel.clear()
    self.content_panel.add_component(Home())
    self.highlight_tab_button(event_args['sender'])
    
  def highlight_tab_button(self, button):
    for b in button.parent.get_components():
      b.role = ''
    button.role = 'elevated-button'