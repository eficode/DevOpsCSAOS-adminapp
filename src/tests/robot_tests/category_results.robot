*** Settings ***
Resource  resource.robot
Resource  resource_login.robot
Resource  resource_add_question.robot
Resource  resource_edit_category.robot
Resource  resource_manage_results.robot
Suite Setup  Open And Configure Browser
Suite Teardown  Close Browser
Test Setup  Go To Home Page

*** Test Cases ***

Logged In User Can View Category Results
    Go To Backdoor Login Page
    Login With Correct Credentials
    Go To Survey  1
    Click Link  edit_button_1
    Wait Until Keyword Succeeds  30s  5s  Page Should Contain  0% - 40% of the max points
    Page Should Contain  Dynamically fetched feedback text for category score.
    Click Element  categoryresults
    Wait Until Keyword Succeeds  30s  5s  Page Should Contain  Category results for Category 1

Logged In User Can Delete Category Results
    Go To Survey  1
    Click Link  edit_button_1
    Click Element  categoryresults
    Expand Result Card  1
    Click Button  Delete
    Page Should Not Contain  Result at cutoff point 0.4

A Category Result Having Cutoff 1.0 Has No Delete Button
    Go To Survey  2
    Click Link  Add category
    Create New Category
    Wait Until Element Is Visible    id:categoryresults
    Click Element  categoryresults
    Expand Result Card  1
    Page Should Not Contain  Delete


User Can Create Subsequent Category Results With Cutoff Values Between 0 And 1
    Go To Survey  2
    Click Link  edit_button_8
    Click Element  categoryresults
    Set Result Text  User Can Create Subsequent Category Results With Cutoff Values Between 0 And 1
    Set Result Cutoff  0.5
    Save Result
    Expand Result Card  2
    Wait Until Keyword Succeeds  30s  5s  Page Should Contain  User Can Create Subsequent Category Results With Cutoff Values Between 0 And 1


User Can Not Create Category Results With Cutoff Values Above 1
    Go To Survey  2
    Click Link  edit_button_8
    Click Element  categoryresults
    Set Result Text  Invalid cutoff  
    Set Result Cutoff  1.1
    Save Result
    Expand Result Card  2
    Page Should Not Contain  Result at cutoff point 1.1


User Can Edit A Category Result
    Go To Survey  2
    Click Link  edit_button_8
    Click Element  categoryresults
    Expand Result Card  1
    Edit Result  User Can Edit A Category Result  0.2  1
    Expand Result Card  1
    Wait Until Keyword Succeeds  30s  5s  Page Should Contain Element  xpath: //*[contains(text(), "0.2")]
    Wait Until Keyword Succeeds  30s  5s  Page Should Contain  User Can Edit A Category Result


Category Result Cannot Be Edited To Have Duplicate Cutoffs
    Go To Survey  2
    Click Link  edit_button_8
    Click Element  categoryresults
    Expand Result Card  1
    Edit Result  Category Result Cannot Be Edited To Have Duplicate Cutoffs  1  1
    Expand Result Card  1
    Wait Until Keyword Succeeds  30s  5s  Page Should Contain  There must not be any identical cutoff values
    Wait Until Keyword Succeeds  30s  5s  Page Should Not Contain  Category Result Cannot Be Edited To Have Duplicate Cutoffs
