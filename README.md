# tfepy

_A Pyton Client for Terraform Enterprise._

README to be fleshed out after completing more of the following endpoints. 

TODO: 
    - Raise exceptions rather than just log errors. 
    - More code comments. 
    - Pep8 linting. 
    - Set global test vars somewhere (like an org, user, etc)
    - Make sure I'm using `pass` only where appropriate
    - Naming convention for test methods
    - Code coverage tool
    - Try to create a scraper that pulls in the docs info for the code / finds deltas from the website.
    - Compare to https://github.com/hashicorp/go-tfe
    - Make it more clear which endpoints do or do not work with TFE SaaS.
    - Rename project for something python/terra related (terrasnek)
    - Add comments to all the tests
    - Use delete or destroy consistently across the API.
    - Have err cases return results and log to debug, rather than err

- [ ] Accounts
- [ ] Configuration Versions
- [ ] OAuth Clients
- [ ] OAuth Tokens
- [X] Organizations
- [ ] Organization Tokens
- [ ] Policies
- [ ] Policy Sets
- [ ] Policy Checks
- [ ] Registry Modules
- [ ] Runs
- [ ] SSH Keys
- [ ] State Versions
- [X] Team Access
- [X] Team Memberships
- [ ] Team Tokens
- [X] Teams
- [ ] Variables
- [/] Workspaces
- [X] Users (show endpoint doesn't work)
- [X] Admin Users
- [X] Admin Organizations
- [ ] Admin Settings
- [ ] Admin Runs
- [ ] Admin Workspaces
- [ ] Admin Terraform Versions