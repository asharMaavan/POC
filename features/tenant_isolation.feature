@bdd
Feature: Tenant isolation
  As a multi-tenant system
  I want data isolated by tenant
  So that tenants cannot see each other

  @api @smoke @regression
  Scenario: Tenant B cannot see boards created by tenant A
    Given I am logged in as "adminA@example.com"
    And I create a board named "Tenant A Board" via API
    When I log in as "adminB@example.com"
    And I list boards via API
    Then the board should not appear in the list
    And all boards belong to my tenant
