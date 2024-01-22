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
from anvil.js.window import jQuery
from anvil.js import get_dom_node

class Project(ProjectTemplate):
  def __init__(self, project_name, **properties):
    # Set Form properties and Data Bindings.
    self.init_components(**properties)
    
    # Any code you write here will run before the form opens.
    self.project_name = project_name
    list_of_vms = anvil.server.call('get_project_vms',project_name)
    for vm in list_of_vms.keys():
      button_tmp = Button(text=vm)
      self.vm_tabs.add_component(button_tmp)
      button_tmp.add_event_handler('click',self.vm_button_clicked)
    list_of_views = anvil.server.call('get_web_views',project_name)
    for view in list_of_views.keys():
      button_tmp = Button(text=view)
      button_tmp.tag.target = list_of_views[view]
      button_tmp.add_event_handler('click',self.view_button_clicked)
      self.vm_tabs.add_component(button_tmp)

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

  def view_button_clicked(self, **event_args):
    target = event_args['sender'].tag.target
    self.content_panel.clear()
    panel_tmp = XYPanel(width="1000px",height="1000px")
    self.content_panel.add_component(panel_tmp)
    #code = "<div id='web_forward_external'></div> <script type='text/javascript'> $(document).ready(function (){$('#web_forward_external').load(%s);});</script>"%(target)
    #code = "<object data=\"https://10.0.0.1\" width=\"400\" height=\"300\" type=\"text/html\"> Alternative Content </object>"
    code = "<iframe src=\"https://10.0.0.1\" style=\"border:0px #ffffff none;\" name=\"myiFrame\" scrolling=\"no\" frameborder=\"1\" marginheight=\"0px\" marginwidth=\"0px\" height=\"400px\" width=\"600px\" allowfullscreen></iframe>"
    print(code)
    iframe = jQuery(code)
    iframe.appendTo(get_dom_node(panel_tmp))

