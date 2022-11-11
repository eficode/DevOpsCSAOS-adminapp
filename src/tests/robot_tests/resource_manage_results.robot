*** Keywords ***

Set Result Text
    [Arguments]  ${text}
    Input Text  text  ${text}

Set Result Cutoff
    [Arguments]  ${value}
    Input Text  cutoff  ${value}

Save Result
    Click Button  Save changes

Expand Result Card
    [Arguments]  ${result_index}
    Click Element  id:expandable-result-${result_index}