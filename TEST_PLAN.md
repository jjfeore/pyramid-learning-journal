# Test plan for pyramid-learning-journal project

## Unit tests: view functions
- list_view populates list template with journal entries
- detail_view populates detail template with journal entry that matches request id
- update_view populates form with journal entry that matches request id (when 'update' route hit with GET method)
- update_view accepts valid POST request
- update_view raises error if POST request missing data
- create_view accepts valid POST request
- create_view raises error if POST request missing data
- detail_view raises HTTPNotFound error if JournalEntries doesn't exist
- update_view raises HTTPNotFound error if JournalEntries doesn't exist

## Unit tests: models
- generated journal entries are instances of JournalEntries model class 
- model can be added successfully to database
- model can be updated in database
- list view returns empty when database empty
- list view shows same number of items as database

## Functional tests: system
- update_view redirects to detail view of journal entry
- create_view redirects to detail view of journal entry
- general invalid route returns 404
- invalid update route returns 404
- invalid create route returns 404
- invalid list route returns 404
- invalid detail route returns 404
- valid update route returns 200
- valid update route results in correct content rendered on page
- valid create route returns 200
- valid detail route returns 200
- valid detail route results in correct content rendered on page
- valid list route returns 200
- valid list route results in correct content rendered on page