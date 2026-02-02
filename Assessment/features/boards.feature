@bdd
Feature: Boards
  As a user
  I want to manage boards
  So that I can organize my work

  @ui @e2e @regression
  Scenario: Create rename and archive a board
    Given I open the app
    And I log in as "adminA@example.com" with password "Password123!" and remember me false
    When I create a board named "Board UI"
    And I rename the board to "Board UI Renamed"
    And I archive the board
    Then the board should not be listed

  @api @regression
  Scenario: Audit log captures create and update events
    Given I am logged in as "adminA@example.com"
    When I create a board named "Audit Board" via API
    And I rename the board to "Audit Board Updated" via API
    Then an audit entry exists for action "create" on the board
    And an audit entry exists for action "update" on the board

  @api @regression
  Scenario: Board name is required
    Given I am logged in as "adminA@example.com"
    When I attempt to create a board without a name
    Then the response status should be 400 or 422
