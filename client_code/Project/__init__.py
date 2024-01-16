from ._anvil_designer import ProjectTemplate
from anvil import *
import anvil.server
import anvil.google.auth, anvil.google.drive
from anvil.google.drive import app_files
import anvil.users
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables
from ..ProjectOverview import ProjectOverview
from ..VM import VM

class Project(ProjectTemplate):
  def __init__(self, project_name, **properties):
    # Set Form properties and Data Bindings.
    self.init_components(**properties)
    
    # Any code you write here will run before the form opens.
    self.project_name = project_name
    list_of_vms = anvil.server.call('get_project_vms',project_name)
    for vm in list_of_vms:
      button_tmp = Button(text=vm)
      self.vm_tabs.add_component(button_tmp)
      button_tmp.add_event_handler('click',self.vm_button_clicked)

  def overview_button_clicked(self, **event_args):
    self.content_panel.clear()
    self.content_panel.add_component(ProjectOverview())
    self.highlight_tab_button(event_args['sender'])

  def vm_button_clicked(self, **event_args):
    self.content_panel.clear()
    self.content_panel.add_component(VM())
    self.highlight_tab_button(event_args['sender'])
  
  def highlight_tab_button(self, button):
    for b in button.parent.get_components():
      b.role = ''
    button.role = 'elevated-button'