# -*- coding: utf-8 -*-

import sys
from redminelib import Redmine
from git import Repo
from datetime import date, datetime, timedelta


# ================================
# ===== Connect to Redmine  ======
# ================================

REDMINE_URL = "http://afi-forge.afi-sa.net"
REDMINE_KEY = "85752a1a4bce459731262629258e742e3e903b95"
redmine = Redmine(REDMINE_URL, key=REDMINE_KEY) # access AFI Forge
project = redmine.project.get('odoo') # connect to the Odoo project
project.refresh()

print('INFO: Browse project at %s' % project.url)
print('INFO: Number of opened tickets: %s' % str(len(project.issues)))
ticket_ids = [] 
for issue in project.issues:
    ticket_ids.append(issue.id) # list of existing tickets

i = 0
while i < 5:
    i += 1
    search_id = int(raw_input('INPUT: Enter ticket number: '))
    if search_id not in ticket_ids:
        if i == 5:
            print('WARNING: Ticket #%d is not found!')
            sys.exit('Aborting')
        print('WARNING: Ticket #%d is not found! Enter a valid number! (%d attempts left)' % (search_id, 5-i))
        if i == 4:
            print('INFO: Currently opened tickets: ')
            print(ticket_ids)
    else:
        search_index = ticket_ids.index(search_id)
        ticket_subject = project.issues[search_index].subject.encode('utf-8') # title of the searched ticket
        print('INFO: Ticket #%d "%s"' % (search_id, ticket_subject)) 
        if raw_input('INPUT: Proceed with this ticket (y/n)? ') == 'y':
            break
        else:
            i = 0

custom_field = project.issues[search_index].custom_fields[4] 
if custom_field.value: # check if odoo module is specified for this ticket
    module = custom_field.value.encode('utf-8')
    print('INFO: Odoo module %s is affected' % module)
else:
    print('WARNING: Odoo module is not specified in the ticket!')
    sys.exit('Aborting')

branch_name = 'forge#%d_%s' % (search_id, module) # new branch name



# ================================
# ===== Local git repository =====
# ================================

repo = Repo("odoo_modules/.git") ####### TODO: ADD FUNCTIONALITY TO CHOOSE FOLDER
print('INFO: Accessing repository in ' + repo.common_dir[:-5])
print('INFO: %s -> %s' % (repo.head.name, repo.active_branch.name))
if branch_name == repo.active_branch.name:
    print('INFO: Already on "%s"' % branch_name)
    sys.exit('Exiting')
print('INFO: Local branches: ')
branch_names = []
for head in repo.heads:
    branch_names.append(head.name)
    if head == repo.active_branch:        
        print('* %s' % head.name)
    else:
        print('  %s' % head.name)        
    if head.name == branch_name:
        new_head = head
            
if branch_name in branch_names:
    print('INFO: Branch "%s" already exists' % branch_name)
    if raw_input('INPUT: Checkout this branch (y/n)? ') != 'y':
        sys.exit('Aborting')
    else:
        if repo.is_dirty():
            print('WARNING: Please commit your changes before you switch branches!')
#             print('\n    '.join(repo.untracked_files))
            sys.exit('Aborting')
        else:
            repo.head.reference = new_head
#             print('INFO: Reseting index and working copy')
            repo.head.reset(index=True, working_tree=True)
#             last_commit = repo.active_branch.commit
#             print('INFO: Last commit on "%s":' % last_commit.hexsha[:-6])
#             print('  Author: %s <%s>' % (last_commit.author.name.encode('utf-8'), last_commit.author.email.encode('utf-8')))
#             print('  Date: %s' % last_commit.committed_datetime.strftime("%d/%m/%Y %H:%M:%S"))
#             print('  Message: %s' % last_commit.message.encode('utf-8'))
else:
    if repo.is_dirty():
        print('WARNING: Please commit your changes before you switch branches!')
#         print('\n    '.join(repo.untracked_files))
        sys.exit('Aborting')
    else:
        repo.head.reference = repo.create_head(branch_name)
#         print('INFO: Reseting index and working copy')
        repo.head.reset(index=True, working_tree=True)    
     
print('INFO: Switched to branch "%s"' % repo.active_branch.name)

    

    
         

    
    
    
    
    
    
    