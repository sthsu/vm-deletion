import pytest
from unittest import mock
import azure.functions as func
from function_app import main  # Import the main function from function_app module

@pytest.fixture
def mock_environment_variables(monkeypatch):
    monkeypatch.setenv("SUBSCRIPTION_ID", "dummy-subscription-id")
    monkeypatch.setenv("RESOURCE_GROUP_LIST", "rg1,rg2,rg3")

@pytest.fixture
def mock_timer_request():
    # Mock the TimerRequest object
    timer_request = mock.Mock(spec=func.TimerRequest)
    timer_request.past_due = False
    return timer_request

def test_main_function(mock_environment_variables, mock_timer_request):
    with mock.patch('function_app.logger') as mock_logger:
        main(mock_timer_request)

        # Verify the timer trigger log message
        mock_logger.info.assert_any_call('Azure Function timer trigger executed at: %s', False)

        # Verify the successful execution log message
        mock_logger.info.assert_any_call("Cleanup VMs function executed successfully")


def test_missing_subscription_id(monkeypatch, mock_timer_request):
    monkeypatch.delenv("SUBSCRIPTION_ID", raising=False)
    monkeypatch.setenv("RESOURCE_GROUP_LIST", "rg1,rg2,rg3")
    resp = main(mock_timer_request)
    print(resp)

# def test_invalid_resource_group_list(monkeypatch, mock_timer_request):
#     monkeypatch.setenv("SUBSCRIPTION_ID", "dummy-subscription-id")
#     monkeypatch.setenv("RESOURCE_GROUP_LIST", "[invalid_json")

#     with mock.patch('function_app.logger') as mock_logger:
#         main(mock_timer_request)

#         # Check if the appropriate error log was generated
#         mock_logger.error.assert_any_call("Failed to parse RESOURCE_GROUP_LIST: %s", mock.ANY)
