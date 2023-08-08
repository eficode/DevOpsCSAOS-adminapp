*** Keywords ***
Set Answer Text
    [Arguments]  ${text}
    Wait Until Page Contains Element  answer_text
    Input Text  answer_text  ${text}

Set Points
    [Arguments]  ${points}
    Wait Until Page Contains Element  points
    Input Text  points  ${points}

Submit Answer
    Wait Until Page Contains Element  xpath://*[normalize-space()='Save changes']
    Click Button  Save changes

Add New Answer
    [Arguments]  ${text}  ${points}
    Set Answer Text  ${text}
    Set Points  ${points}
    Submit Answer

Expand Answer Card
    [Arguments]  ${answer_index}
    Wait Until Element Is Visible    id:expandable-answer-${answer_index}
    Click Element  id:expandable-answer-${answer_index}

Edit Answer
    [Arguments]  ${text}  ${points}  ${id}
    Wait Until Page Contains Element  answer-${id}
    Input Text  answer-${id}  ${text}
    Wait Until Page Contains Element  points-${id}
    Input Text  points-${id}  ${points}