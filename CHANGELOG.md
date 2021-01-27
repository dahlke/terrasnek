# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [0.1.1] - 2020-02-09

I started working on this project about a half a year or so ago, and never
thought it would get this far, but it did. This library has been tested in a
bunch of different places, and I feel confident in it going forward, so today
I will move it to `0.1.1`. There is certainly room for improvement (and I'd
like help to do so if you're willing), but I'm confident you can use this
library for it's utility at this stage.

- Cleared out a bunch of TODOs
- Implemented a bunch of TFC specific endpoints (like subscriptions, invoices, etc.)
- New TFCHTTPRequestRateLimit exception
- Tweaks to the documentation to include more of the library
- Added new TFC entitlements
- 196/196 Implemented endpoints at time of release

## [0.0.16] - 2020-12-23

- Adding new Admin Orgs API endpoint.
- Add the new Admin Module Sharing API
- Make it easier to understand when to run things against TFE or TFC.

## [0.0.15] - 2020-12-14

- Implement the get policy text function for the policies api.
- Implement paging for run triggers API.

## [0.0.14] - 2020-12-14

- Adding a list all function to:
  - workspaces
  - audit trails
  - config versions
  - state versions
  - org memberships
  - policies
  - policy sets
  - runs

## [0.0.13] - 2020-12-14

- Merge in the upload TF config version from string.
- Exceptions log to debug, let the app handle logging errors.

## [0.0.12] - 2020-12-02

- Updating some of the organization purge logic before running tests
- Making it easier to retrieve important values from the API class
- Making it easier to retrieve important values from the Endpoint class

## [0.0.11] - 2020-11-23

- More API tests.
- Purging org memberships and agent pools at the start of a test
- Implement new agent pool endpoints
- Add debug logic to all API requests for prod debugging
- Pass error information back up through exceptions

## [0.0.10] - 2020-11-17

- Make required entitlements a private method.
- Adding typing to the API endpoints per `mcandries` request.
- Raise exceptions for non 2XX 3XX HTTP error codes.
- Update the library to throw API exceptions.
- Update all the tests so to work with exceptions thrown>

## [0.0.9] - 2020-10-20

- Updating docstrings across all methods for method use clarity.
- Updating Registry Modules API to support all methods.
- Standardize how payloads are taken by each endpoint.
- More test streamlining.

## [0.0.8] - 2020-09-17

- Adding more information on query parameters for each relevant endpoint.
- Fix a bug in the Team Access API.
- Update the documentation to add the latest endpoints supported.

## [0.0.7] - 2020-08-26

- Added Agents API for Terraform Cloud Business Tier
- Added Agents Tokens API for Terraform Cloud Business Tier
- Added Audit Trails API for Terraform Cloud Business Tier
- Added missing endpoints in Module Registry, Plans, Policy Sets endpoints.

## [0.0.6] - 2020-07-01

- Make sure endpoint docstrings match the API docs path for automated checks
- Implemented APIs: Workspace Variables, Egress IP Ranges
- Added endpoints for Plans API JSON downloads
- Added endpoints for Team Access API statefile access
- Added endpoints for Teams API statefile access
- API method comparison script and output tables
- Markdown linting
- CircleCI testing docker image and script to upload env vars
- Hitting uncovered lines in Plan Exports, OAuth Clients, Registry Modules, Runs.
- Added TFE release notes links to README.
- Added methods implemented badge to README.

## [0.0.5] - 2020-05-22

### Added

- A CHANGELOG. :)
- All existing endpoints as of today are implemented, documented and tested.
