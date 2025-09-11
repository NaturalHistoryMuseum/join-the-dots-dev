## v0.2.2 (2025-09-11)

### Fix

- literal logic error fix for build

## v0.2.1 (2025-09-11)

### Build System(s)

- adding package.find to pyproject

## v0.2.0 (2025-09-11)

### Feature

- name and email checked against o365 and will update if different
- improving help text
- user permissions functionality completed
- user management page added for managers
- account page dropdowns functional
- account page reformmated, message overlay now based on store
- unit permissions page completed and hooked in, fixed rescore not saving
- assigning editors now submits to db
- curator assignment added to view unit page
- score viewability improved
- rescore page improvements - review, errors and ui changed
- remove vue js dev tools
- unit actions will reload the view units table
- unit actions added - improvement to viewing units
- view unit fields rendered dynamically from config
- adding units functionality added
- minor improvements to rescore page and bulk edit modal
- action button colour changed
- **rescore-criterion**: criterion code added into rescore criterions
- **bulk-edit**: adding selected units to bulk edit review
- add stepper to rescore and other various changes
- view unit mentions editing if user able to
- **rescore-page**: review proccess added to rescore
- **view-unit-editability**: unit fields will only be editable if the user is assinged the unit
- **tablecheckbox**: table checkbox only allows assinged units to be selected
- **tablecheckbox-rows-per-page-option**: rows per page for the table comp now stores the row number in local storage
- testing commit

### Fix

- fix unit search on account page and mistaken decimals on rescore
- removed red error when adding scores on new unit page
- various fixes to spelling and functionality - new unit assigned editor now mandatory
- adding extension to required list
- only reset rank data if a change is made - fixes scores being overwritten by saving
- token issue resolved
- resolve csrf token issue
- **login-system**: access token refresh issue temp changess
- **sidebar-filter-and-account-page**: minor fixes to the search and select boxes
- generic fixes to remove errors
- typo in requirements
- temporarily adding flask requirements back in
- pagination with table checkbox fixed

### Refactor

- readded toml to project
- refactored code formatting, adjusted pyproject
- change endpoints for k8s
- refaction config
- removing unused add unit files
- removed prints and console logs
- removing commented code
- code changes to attempt csrf fix
- flask_jwt_extended added to improve route security
- changed api to k8s endpoints
- backend code improvements
- **flask-config**: remove dot env import
- config and extensions improved
- pre-commit changes applied
- k8s endpoints added
- **view-units-table**: viewunits table split into separate components

### Style

- pre commit formatting

## v0.1.0 (2025-06-19)

### Feature

- actions modal added
- warning added for required fields
- Saving changes added to units and save message displayed
- footer added
- Architecture diagram added
- Remove old app flask file
- Docs added
- Bulk rescore submits scores, messages componet created
- Generic cleanup, Rescore now submits data, Bulk Rescore started. (local endpoints)
- Rescore process added. Login page added. (k8s endpoints)
- fields for view unit page complete (local endpoints)
- additions to view unit page
- View unit page improvements and various fixes
- View units and Rescore have major design and functionality overhauls.
- various front end additions, backend now allows reloading user details without log out
- tabs, login and report exports added
- Azure login added. Various small front end changes
- login system added with azure. will store the user details in the local storage
- flask backend modulised for better management. Additional front end changes
- Added git ignore file and config managment

### Fix

- view unit component broken up into many sub components
- score changes returned to bulk modal
- toptabs now don't error when no unit provided

### Style

- fix trailing whitespace and file endings on other files
- python formatting
- prettier formatting

### Build System(s)

- update vue devtools to add compatibility with vite 6
- update name and version of node project
- add pyproject.toml and move dependencies
- Adding session secret (k8s endpoints)
- fixing python requirements
- fix spelling error in endpoints
- add host to server run file
- workaround for auth not pulling from app config
- fix mismatch in db variables
- auth now uses app config
- configured endpoints for k8s url
- add mysql-connector to requirements
- remove unneeded dependencies

### CI System(s)

- install npm packages in pr validation workflow
- add node setup to pr validation
- add github workflow configs

### Chores/Misc

- set major_version_zero while project is in dev
- use npm cz version provider with pyproject as additional file
- fix eslint error
- limit eslint to src folder
- format eslint and editorconfig files
- add pre-commit config
- ignore when eslint ignores files
- update prettier config and add plugin to organise imports
- rename .prettierrc
- use generic eslint prettier config
- add a license
- ignore .egg-info
- update editorconfig to match prettier default options
