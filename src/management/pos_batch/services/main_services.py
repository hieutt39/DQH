import logging
import coloredlogs
from .compare_data_services import CompareDataService
from .health_db_service import HealthDbService
from .compare_schema_service import CompareSchemaService
from .compare_api_service import CompareApiService

coloredlogs.DEFAULT_LOG_FORMAT = '%(asctime)s - %(levelname)s: %(message)s'
coloredlogs.DEFAULT_FIELD_STYLES['levelname'] = dict(color='magenta', bold=True)
coloredlogs.install()
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)


class MainService():

    def __init__(self, **options):
        pass

    def __enter__(self):
        return self

    def __exit__(self, type, value, traceback):
        pass

    def healthcheck(self):
        logger.info('=========================== TEST DB CONNECTION: START ===========================')
        HealthDbService().healthcheck()
        logger.info('=========================== TEST DB CONNECTION: END =============================')

    @staticmethod
    def healthcheck_table():
        logger.info('=========================== VERIFY STRUCTURE: START ===========================')
        HealthDbService().healthcheck_table()
        logger.info('=========================== VERIFY STRUCTURE: END =============================')

    def compare_schema(self):
        logger.info('=========================== COMPARE STRUCTURE: START ===========================')
        CompareSchemaService().process()
        logger.info('=========================== COMPARE STRUCTURE: END =============================')

    @staticmethod
    def compare_data():
        logger.info('=========================== COMPARE DATA: START ===========================')
        CompareDataService().process()
        logger.info('=========================== COMPARE DATA: END ===========================')

    @staticmethod
    def compare_api():
        logger.info('=========================== COMPARE API: START ===========================')
        CompareApiService().process()
        logger.info('=========================== COMPARE API: END ===========================')
