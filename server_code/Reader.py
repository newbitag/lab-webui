import anvil.google.auth, anvil.google.drive, anvil.google.mail
from anvil.google.drive import app_files
import anvil.users
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables
import anvil.server

# This is a server module. It runs on the Anvil server,
# rather than in the user's browser.
#
# To allow anvil.server.call() to call functions here, we mark
# them with @anvil.server.callable.
# Here is an example - you can replace it with your own:

@anvil.server.callable
def get_user_projects(user_email):
  projects = ['demo1','demo2','demo3']
  return projects
  
@anvil.server.callable
def get_project_vms(project_name):
  vms = ["vm1","vm2","vm3"]
  return vms


@anvil.server.callable
def get_resources():
  resources = {'cpu_total':32,'cpu_used':14.5,'memory_total':128,'memory_used':48.3}
  return resources
