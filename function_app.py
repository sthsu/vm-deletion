import logging,os,json
import azure.functions as func
from service.managed_bastion.cleanup_vms import CleanupVmsFunction

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = func.FunctionApp()

@app.function_name(name="CleanupVMs")
@app.schedule(schedule="* */10 * * * *", arg_name="mytimer", run_on_startup=True, use_monitor=True)
def main(mytimer: func.TimerRequest):
    logging.info('Azure Function timer trigger executed at: %s', mytimer.past_due)
    try:
        subscription_id = os.environ.get("SUBSCRIPTION_ID")
        resource_group_list_str = os.environ.get("RESOURCE_GROUP_LIST")
        
        if not subscription_id:
            logger.error("SUBSCRIPTION_ID environment variable is not set")
        
        if not resource_group_list_str:
            logger.error("RESOURCE_GROUP_LIST environment variable is not set")

        try:
            resource_group_list = resource_group_list_str.split(",")
            if not isinstance(resource_group_list, list):
                raise ValueError("RESOURCE_GROUP_LIST is not a valid list")
        except json.JSONDecodeError as e:
            logger.error("Failed to parse RESOURCE_GROUP_LIST: %s", str(e))

        cleanup_function = CleanupVmsFunction(subscription_id, resource_group_list)
        cleanup_function.run()
      
        logger.info("Cleanup VMs function executed successfully")
    except ImportError as e:
        logger.error(f"Failed to import module: {str(e)}")        
    except Exception as e:
        logger.error("An error occurred: %s", str(e))
