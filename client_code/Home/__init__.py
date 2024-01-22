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

    self.projects_panel.clear()
    projects = anvil.server.call('get_user_projects',anvil.users.get_user()['email'])
    for project in projects:
      list_of_vms = anvil.server.call('get_project_vms',project)
      project_panel = LinearPanel(role='tonal-card')
      project_headlinepanel = FlowPanel(align='left')
      project_headlinepanel.tag.project = project
      project_label = Label(text=project,font_size=16)
      project_delete_button = Button(text="Delete Project")
      project_delete_button.add_event_handler('click',self.delete_project)
      project_headlinepanel.add_component(project_label)
      project_headlinepanel.add_component(project_delete_button)
      project_vm_panel = ColumnPanel()
      project_vm_panel.role = 'outlined-card'
      for vm in list_of_vms.keys():
        vm_panel = FlowPanel(align='left',role='elevated-card')
        vm_panel.tag.project = project
        vm_panel.tag.vm = vm
        vm_label = Label(text=vm)
        vm_start_button = Button(text="Start",role='tonal-button')
        vm_shutdown_button = Button(text="Shutdown",role='tonal-button')
        vm_destroy_button = Button(text="Force Off",role='tonal-button')
        vm_start_button.add_event_handler('click',self.start_vm_clicked)
        vm_shutdown_button.add_event_handler('click',self.stop_vm_clicked)
        vm_destroy_button.add_event_handler('click',self.destroy_vm_clicked)

        if list_of_vms[vm]:
          vm_panel.background = app.theme_colors['Started']
          vm_start_button.enabled = False
          vm_shutdown_button.enabled = True
          vm_destroy_button.enabled = True
        else:
          vm_panel.background = app.theme_colors['Shutdown']
          vm_start_button.enabled = True
          vm_shutdown_button.enabled = False
          vm_destroy_button.enabled = False
        vm_panel.add_component(vm_label)
        vm_panel.add_component(vm_start_button)
        vm_panel.add_component(vm_shutdown_button)
        vm_panel.add_component(vm_destroy_button)
        project_vm_panel.add_component(vm_panel)
      project_panel.add_component(project_headlinepanel)
      project_panel.add_component(project_vm_panel)
      self.projects_panel.add_component(project_panel)

  def delete_project(self, **event_args):
    sender_parent_tags = event_args['sender'].parent.tag
    c = confirm("Do you really want to delete %s"%(sender_parent_tags.project))
    if c:
      anvil.server.call('remove_project',sender_parent_tags.project)

  
  def start_vm_clicked(self, **event_args):
    sender_parent_tags = event_args['sender'].parent.tag
    print(sender_parent_tags)
    anvil.server.call('start_vm',sender_parent_tags.project,sender_parent_tags.vm)
    self.refresh_data_bindings()

  def stop_vm_clicked(self, **event_args):
    sender_parent_tags = event_args['sender'].parent.tag
    print(sender_parent_tags)
    anvil.server.call('stop_vm',sender_parent_tags.project,sender_parent_tags.vm)
    self.refresh_data_bindings()

  def destroy_vm_clicked(self, **event_args):
    sender_parent_tags = event_args['sender'].parent.tag
    print(sender_parent_tags)
    anvil.server.call('stop_vm',sender_parent_tags.project,sender_parent_tags.vm,True)
    self.refresh_data_bindings()