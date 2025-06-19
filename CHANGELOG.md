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
