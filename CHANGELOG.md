## v1.6.2 (2026-01-15)

### Build System(s)

- add name to commitizen file

## v1.6.1 (2026-01-15)

### Fix

- reduced textbox autosave frequency

### Refactor

- **headers**: improve headers accessibility by not skipping levels

## v1.6.0 (2026-01-06)

### Feature

- adds change log and admin management for change log
- adds filtering for draft units

### Fix

- **enhancements-table**: enhancement are now stored dynamically and can be edited by admin
- fixes issue with tablecheckbox selecting units and filtering

### CI System(s)

- move add enhancement button
- commitizen file added for cicd pipeline

## v1.5.0 (2025-12-18)

### Feature

- allows for comments to be added when adding units and can save imcomplete scores as drafts
- **draft-units**: adds ability to add draft units

### Fix

- **curator-field**: editors field updated by curator field change

## v1.4.1 (2025-12-08)

### Fix

- **issues-management**: can edit and manage issues in the admin area

### Refactor

- remove redundant code comments

### Docs

- change file types for documentation
- removing diagram images

## v1.4.0 (2025-11-28)

### Feature

- **delete-modal**: adds justification textbox to delete action
- lets admins edit everyones permissions
- **issues**: add admin ability to see and manage issues

### Fix

- admin able to see all units to rescore
- **admin-unit-management**: admins can now edit any unit

## v1.3.0 (2025-11-21)

### Feature

- **guidance**: add ability to include recording embed link to guidance

## v1.2.0 (2025-11-20)

### Feature

- **guidance**: added admin ability to edit guidance stored in a table

### Refactor

- add main tag to app

## v1.1.1 (2025-11-13)

### Fix

- **help-page**: resolve issue of md content not showing on help page

### Refactor

- bump cz version change

## v1.1.0 (2025-11-13)

### Feature

- adds ability to raise issues in the app
- **help-page**: add guidance and issues to help page
- help page concept added

### Refactor

- ruff file formatting

### Minor UI Changes

- move issue modal button

## v1.0.1 (2025-11-07)

### Minor UI Changes

- change page title

## v1.0.0 (2025-11-07)

### Minor UI Changes

- remove login prod error

## v0.6.4 (2025-11-07)

### Fix

- stopping % loophole to add over 100

### Minor UI Changes

- remove login prod error

## v0.6.3 (2025-11-07)

### Fix

- **rescore-metrics**: fixes errors for metrics and adds warning for %'s

## v0.6.2 (2025-11-06)

### Fix

- remove actions for only one unit rescore

## v0.6.1 (2025-11-06)

### Fix

- pre live final fixes

## v0.6.0 (2025-11-05)

### Feature

- managers can upgrade viewers permissions
- **power-bi-api**: add new flexible data api

## v0.5.2 (2025-11-03)

### Fix

- **accessibility**: fixed accessibility issue on criterion modal
- **login**: fix for new viewers not being able to access application

## v0.5.1 (2025-11-03)

### Minor UI Changes

- Adding warning message to login page

## v0.5.0 (2025-11-03)

### Feature

- **power-bi-api**: added multiple endpoints to facili tate reporting
- **power-bi-api**: adding more apis for the power bi data
- **rescore-management**: added ability to mark no change on units
- add selected units count to table comp
- remove last rescore total
- bulk unit scores warning messages appear when changes made
- rename department to discipline
- **unit-actions**: unit actions will not perform on open rescore units
- **audit-tracking**: app data changes tracked in audit tables

### Fix

- revert the front end env variables to use vite
- **headers**: change how headers are managed in app
- fix action modals listing too many units and rescore table select issue
- fix removing editors and restrict user role changes
- multiple fixes from uat feedback
- **front-end-env-vars**: front end ev variables now passed through config that will be serviced through k8s
- unit permissions fetch fix

### Refactor

- refactor ruff formatting
- formatting and removing redundant file
- moving modal comps to own folder

### Minor UI Changes

- **accessibility**: changes based on accessibility review

## v0.4.1 (2025-10-20)

### Fix

- temp fix for api url issue

## v0.4.0 (2025-10-10)

### Feature

- api for powerbi to access db started

### Fix

- change how the user/person tables are used by the app
- adding more simple powerbi data api

### Refactor

- removing sql queries and gitignoring them
- removing old view unit tabs
- removing accidental backend build folder
- updating packages for security

### Chores/Misc

- change api url into the env variables

## v0.3.2 (2025-09-26)

### Build System(s)

- **deps**: bump form-data from 4.0.1 to 4.0.4

## v0.3.1 (2025-09-19)

### Fix

- adding unit - adding scores will now add up to 100%

## v0.3.0 (2025-09-18)

### Feature

- users can submit changes to assigned units

### Fix

- fix account page, rescore issues and other minor fixes

## v0.2.5 (2025-09-16)

### Fix

- unit action will duplicate scores corrently and assigned units listed on account page

## v0.2.4 (2025-09-16)

### Fix

- fixes issues on account and view unit

## v0.2.3 (2025-09-11)

### Refactor

- change endpoints to k8s

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
