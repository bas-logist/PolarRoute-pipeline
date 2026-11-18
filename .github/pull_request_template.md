## Title

- Replace the 'Title' with a good title for your PR!


## Aim and background

- State background in a sentence or two
    - E.g. 'Users reported that API calls were failing under high load'.
    - E.g. 'Users were asking for an easier way to obtain data as files'.
- Link any relevant bugs or enhancements
    - E.g. The original API call bug ticket.
    - E.g. The enhancement request for data export.
- State the aim of your PR
    - E.g. 'Stop API complaints from users by making code handle API interruptions more elegantly'.
    - E.g. 'Add a data export function in the web interface'.


## Changes made

- Briefly describe the changes you've made:
    - E.g. 'A longer wait time was added between API calls'.
    - E.g. 'I built an export function, which queries the database for entries made by a user in a date range, and outputs a CSV'.


## Pre-review checklist - for the author

- [ ] Branch has been updated from its parent branch recently (e.g by merging or rebasing)
- [ ] Code formatters (e.g. Ruff, Black) have been run, either manually or automatically, e.g. through GitHub Actions
- [ ] Any unit tests have been run, either manually or automatically, e.g. through GitHub Actions
- [ ] '.gitignore' file is present and up-to-date.
- [ ] Changelog file is present and up-to-date.
- [ ] Readme/docs are present and up-to-date. If 'properdocs' or similar is used, they have been shown to build correctly.
- [ ] Dependencies are recorded and up-to-date (e.g uv 'pyproject.toml', pip 'requirements.txt', etc)

*The Black PEP8 formatter is available as a VS Code extension, called 'Black Formatter'.


## Unit testing

- If you've written unit tests - do they pass? 
    - If not set up in GitHub Actions: provide summary output.
    - If possible, provide a summary coverage report for the sections of code you've changed.
    - Explain where you left gaps and why.
- If there are unit tests failing which you didn't write - show that you've checked this isn't caused by your code.
    - If this is a known bug: Link known issues for this repository.
    - If the unit test failure was already occurring on the main repo: Make a bug ticket, and link to it.


## New behaviour of code

- Carry out sense checking - prove that you've achieved your aim.
- MAKING SURE TO OMIT SENSITIVE DATA - Show screenshots or pasted code for the following, where relevant:
    - The GUI
    - Database outputs (e.g. if you're working on a Django app, run 'shell plus' commands to demonstrate changes)
    - Migration success messages (e.g. if you've changed the db for a Django/Flask app)
    - Files
    - And anything else that might be relevant


## Documentation and validation
> [!NOTE] 
> This section is **important** if this PR is to create a deployment version. Otherwise, it can be skipped where appropriate (e.g. release still some way off)
- List documentation that will need changing or writing, which may include risk assessments, and manuals for users and developers.


## Are acceptance criteria met?

- If this change was requested by another person: would the requester be happy with what you've done?


## Tickets closed by this PR

- You can use the 'Closes' keyword to make tagged tickets auto-close when the PR is merged.
- See formatting here: https://docs.github.com/en/issues/tracking-your-work-with-issues/using-issues/linking-a-pull-request-to-an-issue

