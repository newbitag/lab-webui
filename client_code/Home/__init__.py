from ._anvil_designer import HomeTemplate
from anvil import *
import plotly.graph_objects as go
import anvil.server
import anvil.google.auth, anvil.google.drive
from anvil.google.drive import app_files
import anvil.users
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables

class Home(HomeTemplate):
  def __init__(self, **properties):
    # Set Form properties and Data Bindings.
    self.init_components(**properties)

    # Any code you write here will run before the form opens.
    resources = anvil.server.call('get_resources')
    cpu_total = resources['cpu_total']
    cpu_used = resources['cpu_used']
    memory_total = resources['memory_total']
    memory_used = resources['memory_used']

    self.plot_cpu.data = [
      go.Pie(labels=["Cpu Used","Cpu Free"],
             values=[cpu_used,(cpu_total-cpu_used)],
             hole=.5
            )
    ]

    self.plot_memory.data = [
      go.Pie(labels=["Memory Used","Memory Free"],
             values=[memory_used,(memory_total-memory_used)],
             hole=.5
            )
    ]

    projects = anvil.server.call('get_user_projects',anvil.users.get_user()['email'])
    for project in projects:
      list_of_vms = anvil.server.call('get_project_vms',project)
      project_panel = LinearPanel()
      project_label = Label(text=project,font_size=16)
      project_vm_panel = ColumnPanel()
      for vm in list_of_vms:
        vm_label = Label(text=vm)
        project_vm_panel.add_component(vm_label)
      project_panel.add_component(project_label)
      project_panel.add_component(project_vm_panel)
      self.projects_panel.clear()
      self.projects_panel.add_component(project_panel)