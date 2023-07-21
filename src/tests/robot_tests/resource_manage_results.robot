*** Keywords ***

Set Result Text
    [Arguments]  ${text}
    Input Text  text  ${text}

Set Result Cutoff
    [Arguments]  ${value}
    Input Text  cutoff  ${value}

Save Result
    Click Button  value:Save changes

Expand Result Card
    [Arguments]  ${result_index}
    Wait Until Page Contains Element    id:expandable-result-${result_index}
    Click Element  id:expandable-result-${result_index}

Edit Result
    [Arguments]  ${result}  ${cutoff}  ${id}
    Input Text  result-${id}  ${result}
    Input Text  cutoff-${id}  ${cutoff}