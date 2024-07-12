# import logging
# import azure.functions as func

# app = func.FunctionApp()

# @app.schedule(schedule="0 * * * * *", arg_name="myTimer", run_on_startup=True,
#               use_monitor=False) 
# def timer_trigger(myTimer: func.TimerRequest) -> None:
#     if myTimer.past_due:
#         logging.info('The timer is past due!')

#     logging.info('Python timer trigger function executed.')


import logging
import azure.functions as func
from service.managed_bastion.cleanup_vms import CleanupVmsFunction

app = func.FunctionApp()

@app.function_name(name="CleanupVMs")
@app.schedule(schedule="0 0 * * * *", arg_name="mytimer", run_on_startup=True, use_monitor=False)
def main(mytimer: func.TimerRequest):
    logging.info('Azure Function timer trigger executed at: %s', mytimer.past_due)
    cleanup_function = CleanupVmsFunction()
    cleanup_function.run()