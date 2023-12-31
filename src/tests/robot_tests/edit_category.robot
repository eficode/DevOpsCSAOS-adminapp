*** Settings ***
Resource  resource.robot
Resource  resource_login.robot
Resource  resource_edit_category.robot
Suite Setup  Open And Configure Browser
Suite Teardown  Close Browser
Test Setup  Go To Home Page

*** Test Cases ***

Logged In User Can Create Categories
    Login Through Backdoor
    Go To Survey  1
    Wait Until Keyword Succeeds  30s  5s  Page Should Contain  Categories
    Click Link  Add category
    Create New Category
    Wait Until Keyword Succeeds  30s  5s  Page Should Contain  nimi
    Page Should Contain  kuvaus

Category Result Module Not Displayed When Creating Category
    Go To Survey  1
    Click Link  Add category
    Wait Until Keyword Succeeds  30s  5s  Page Should Not Contain  Category has no results
    Page Should Not Contain  Manage Category Results

Category Edit View Should Display Survey Name
    Go To Survey  1
    Click Link  edit_button_1
    Wait Until Keyword Succeeds  30s  5s  Page Should Contain  test_name


Back Button Opens Correct Survey Page On New Category Page
    Go To Survey  1
    Click Link  Add category
    Wait Until Page Contains Element  partial link:Back to survey
    Click Link  partial link:Back to survey
    Wait Until Keyword Succeeds  30s  5s  Page Should Contain  test_name
    Page Should Contain  test_title
    Page Should Contain  test_text

Back Button Opens Correct Survey Page On Edit Category Page
    Go To Survey  1
    Click Link  edit_button_1
    Wait Until Page Contains Element  partial link:Back to survey
    Click Link  partial link:Back to survey
    Wait Until Keyword Succeeds  30s  5s  Page Should Contain  test_name
    Page Should Contain  test_title
    Page Should Contain  test_text

Logged In User Cannot Create Categories Without Name
    Go To Survey  1
    Click Link  Add category
    Create New Category Without Name
    Page Should Not Contain  Add content link

Logged In User Cannot Create Categories Without Description
    Go To Survey  1
    Click Link  Add category
    Create New Category Without Description
    Page Should Not Contain  Add content link

Logged In User Can Create Categories Without Content Links
    Go To Survey  1
    Click Link  Add category
    Create New Category Without Content Links
    Wait Until Keyword Succeeds  30s  5s  Page Should Contain  abc
    Page Should Contain  123
    Page Should Contain  Your skills in this topic are excellent!
    Click Element  categoryresults
    Wait Until Keyword Succeeds  30s  5s  Page Should Contain Element  expandable-result-1

Logged Out User Cannot Create Categories
    Logout
    Go To Survey  1
    Wait Until Keyword Succeeds  30s  5s  Page Should Contain  Please login

User Is Shown Error Message When Deleting Category Which Is Only Non Zero Weight For Questions
    Go To Backdoor Login Page
    Login With Correct Credentials
    Go To Survey  1
    Wait Until Keyword Succeeds  30s  5s  Page Should Contain  Categories
    Click Button  delete_button_1
    Notification Is Displayed
    Wait Until Keyword Succeeds  30s  5s  Page Should Contain    Check the following questions category weights before deleting 'Category 1': 'Question 8', 'Why', 'kysymys1'

User Can Delete Category Which Is Not The Only Non Zero Weight For Questions
    Go To Survey  1
    Click Button  delete_button_4
    Notification Is Displayed
    Wait Until Keyword Succeeds  30s  5s  Page Should Contain  Successfully deleted category


Logged In User Can Edit Category Name and Description
    Go To Survey  1
    Click Link  edit_button_1
    Wait Until Keyword Succeeds  30s  5s  Page Should Contain  Edit a category
    Edit Category Name and Description
    Wait Until Keyword Succeeds  30s  5s  Page Should Contain  uusi nimi
    Page Should Contain  uusi kuvaus

Logged In User Can Add a New Content Link
    Go To Survey  1
    Click Link  edit_button_1
    Add Content Link
    Wait Until Keyword Succeeds  30s  5s  Page Should Contain  uusi url
    Page Should Contain  uusi tyyppi

Logged In User Can Edit a Content Link
    Go To Survey  1
    Click Link  edit_button_1
    Edit Content Link
    Wait Until Keyword Succeeds  30s  5s  Page Should Contain  kissa
    Page Should Contain  koira

Logged In User Can Delete a Content Link
    Go To Survey  1
    Click Link  edit_button_1
    Wait Until Keyword Succeeds  30s  5s  Page Should Contain  kissa
    Click Button  delete_url_0
    Handle Alert  Accept
    Page Should Not Contain  kissa

