
from function_app import main 
import azure.functions as func
from unittest import mock
timer_request = mock.Mock(spec=func.TimerRequest)

main(timer_request)