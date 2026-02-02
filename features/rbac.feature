@bdd
Feature: Role based access control
  As a tenant user
  I want permissions enforced by role
  So that viewers are read-only

  @ui @e2e @regression
  Scenario: Viewer controls are disabled in the UI
    Given a board exists for tenant A
    And I open the app
    And I log in as "viewerA@example.com" with password "Password123!" and remember me false
    Then viewer board controls are disabled

  @api @regression
  Scenario: Viewer cannot create a board via API
    Given I am logged in as "viewerA@example.com"
    When I create a board named "Should Fail" via API
    Then the response status should be 403
