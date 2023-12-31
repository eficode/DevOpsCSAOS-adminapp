*** Settings ***
Resource  resource.robot
Resource  resource_login.robot
Resource  resource_manage_results.robot
Resource  resource_create_survey.robot
Suite Setup  Open And Configure Browser
Suite Teardown  Close Browser
Test Setup  Go To Home Page


*** Test Cases ***
User Can Create New Survey Result
    Go To Backdoor Login Page
    Login With Correct Credentials
    Go To Survey  8
    Click Link  partial link:Manage results
    Set Result Text  You most resemble an African elephant
    Save Result
    Go To Survey  8
    Click Link  partial link:Manage results
    Wait Until Keyword Succeeds  30s  5s  Page Should Contain  Result at cutoff point
    Expand Result Card  1
    Wait Until Keyword Succeeds  30s  5s  Page Should Contain  You most resemble an African elephant


First Survey Result Must Have Cutoff Value Of One
    Go To Survey  7
    Click Link  partial link:Manage results
    Set Result Text  You're Hanko!
    Set Result Cutoff  0.5
    Save Result
    Page Should Not Contain  Result at cutoff point

User Can Create Subsequent Survey Results With Cutoff Values Between 0 And 1
    Go To Survey  8
    Click Link  partial link:Manage results
    Set Result Text  You look like an Indian elephant
    Set Result Cutoff  0.5
    Save Result
    Go To Survey  8
    Click Link  partial link:Manage results
    Expand Result Card  1
    Wait Until Keyword Succeeds  30s  5s  Page Should Contain Element  xpath: //*[contains(text(), "0.5:")]
    Wait Until Keyword Succeeds  30s  5s  Page Should Contain Element  xpath: //*[contains(text(), "You look like an Indian elephant")]


Survey Results Can't Have Duplicate Cutoff Values
    Go To Survey  8
    Click Link  partial link:Manage results
    Set Result Text  First result at 0.6
    Set Result Cutoff  0.6
    Save Result
    Go To Survey  8
    Click Link  partial link:Manage results
    Set Result Text  Second result at 0.6
    Set Result Cutoff  0.6
    Save Result
    Expand Result Card  1
    Expand Result Card  2
    Page Should Not Contain  Second result at 0.6
    Wait Until Keyword Succeeds  30s  5s  Page Should Contain Element  xpath: //*[contains(text(), "There must not be any identical cutoff values")]

Subsequent Survey Results Must Have Cutoff Value Between 0 And 1
    Go To Survey  8
    Click Link  partial link:Manage results
    Set Result Text  You transcend all earthly elephants
    Set Result Cutoff  15
    Save Result
    Page Should Not Contain  Result at cutoff point 15

Survey Result Can Be Deleted
    Go To Survey  8
    Click Link  partial link:Manage results
    Expand Result Card  1
    Wait Until Page Contains  Delete result
    Click Button  Delete result
    Handle Alert  Accept
    Page Should Not Contain  0.5:

Survey Result With Cutoff Value One Can not Be Deleted
    Go To Survey  8
    Click Link  partial link:Manage results
    Expand Result Card  1
    Click Button  Delete result
    Handle Alert  Accept
    Sleep  2s
    Expand Result Card  1
    Wait Until Page Does Not Contain  Delete

New Survey Has Survey Result For Cutoff Value 1.0
    Click Link  partial link:New survey
    Make A Survey
    Wait Until Keyword Succeeds  30s  5s  Page Should Contain  0% - 100% of the max points
    Page Should Contain  Your skills in this topic are excellent!

Survey Result Can Be Edited
    Go To Survey  8
    Click Link  partial link:Manage results
    Set Result Text  You hate elephants
    Set Result Cutoff  0
    Save Result
    Go To Survey  8
    Click Link  partial link:Manage results
    Expand Result Card  1
    Wait Until Keyword Succeeds  30s  5s  Page Should Contain Element  xpath: //*[contains(text(), "0.0:")]
    Wait Until Keyword Succeeds  30s  5s  Page Should Contain Element  xpath: //*[contains(text(), "You hate elephants")]
    Edit Result  You love elephants  0.98  1
    Go To Survey  8
    Click Link  partial link:Manage results
    Expand Result Card  1
    Wait Until Keyword Succeeds  30s  5s  Page Should Contain Element  xpath: //*[contains(text(), "0.98:")]
    Wait Until Keyword Succeeds  30s  5s  Page Should Contain Element  xpath: //*[contains(text(), "You love elephants")]

Survey Result Cannot Be Edited To Have Duplicate Cutoffs
    Go To Survey  8
    Click Link  partial link:Manage results
    Expand Result Card  1
    Wait Until Keyword Succeeds  30s  5s  Page Should Contain Element  xpath: //*[contains(text(), "You love elephants")]
    Edit Result  You hate elephants  1  1
    Expand Result Card  1
    ${innerhtml}=  Get Element Attribute  xpath://*[contains(@class, 'py-8')]  innerHTML
    Log To Console  ${innerhtml}
    Wait Until Keyword Succeeds  30s  5s  Page Should Contain Element  xpath: //*[contains(text(), "You love elephants")]
    Wait Until Keyword Succeeds  30s  5s  Page Should Not Contain Element  xpath: //*[contains(text(), "You hate elephants")]
    Wait Until Keyword Succeeds  30s  5s  Page Should Contain Element  id:notification
    Wait Until Keyword Succeeds  30s  5s  Page Should Contain Element  xpath: //*[contains(text(), "Error")]

