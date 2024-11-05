import queue
import string
import threading
import time
import logging
import json
import uuid
from src.utilities.api_request import ApiRequest

logging.basicConfig()
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)


class WorkerService:
    def __init__(self, base_url: string = None):
        """
        :param base_url: string
        """
        # the queue for tasks
        self._worker_queue = queue.Queue()
        # number of seconds to run each process
        self._worker_queue_per_second = 0
        # number of worker
        self._worker_pool = 5
        self.api = ApiRequest()
        self.api.BASE_URL = base_url
        self.grand_total = 0
        self.total = 0
        self.success = 0
        self.failed = 0
        self.data_log = []

    def set_worker_pool(self, worker_pool: int):
        """
        number of workers
        :param worker_pool:
        :return:
        """
        self._worker_pool = worker_pool

    def set_wait_second_for_each_process(self, second: int):
        """
        Number of seconds to wait for each process to finish
        :param second:
        :return:
        """
        self._worker_queue_per_second = second

    def _worker(self):
        """
        _worker, handles each task
        :return:
        """
        while True:
            task = self._worker_queue.get()
            if task is None:
                # logger.warning("BREAK THREAD")
                break
            self.total += 1
            try:
                payload = json.dumps(task.get('payload'), ensure_ascii=True)
                # response = self.api.request(task.get('endpoint'), post_args=payload)
                response = self.api.request('/rest/V1/orders/create', post_args=payload, method='PUT')
                logger.info("RESPONSE:{}".format(response))
                # logger.info(f"TIME: {time.time()}")
                if response.get('status_code') == 200:
                    callback = task.get('callback')
                    callback_args = task.get('callback_args')
                    if callback is not None:
                        callback(*callback_args)
                    self.success += 1
            except Exception as e:
                logger.error(e)

            self._worker_queue.task_done()
            time.sleep(self._worker_queue_per_second)

    def _start_workers(self, worker_pool: int = 5):
        """
        start up your workers
        :param worker_pool: int
        :return:
        """
        threads = []
        for i in range(worker_pool):
            t = threading.Thread(target=self._worker)
            t.start()
            threads.append(t)
        return threads

    def _stop_workers(self, threads: list):
        """
        stop workers
        :param threads: list of thread
        :return:
        """
        for _ in threads:
            self._worker_queue.put(None)

        for t in threads:
            t.join()

    def create_queue(self, endpoint, task_item, callback=None, callback_args=()):
        """
        Create a queue
        :param endpoint:
        :param task_item:
        :param callback:
        :param callback_args:
        :return:
        """
        task = {
            'endpoint': endpoint,
            'payload': task_item,
            'callback': callback,
            'callback_args': callback_args,
        }
        print(task_item)
        self._worker_queue.put(task)
        self.data_log.append(task_item)

    @property
    def worker_queue(self):
        return self._worker_queue

    def run(self):
        """
        :return:
        """
        logger.info(f"== INIT")
        logger.info(f"== WORKER POOL: {self._worker_pool}")
        logger.info(f"== WAIT SECOND FOR EACH PROCESS: {self._worker_queue_per_second}")
        logger.info(f"========================================")

        # Start up your workers
        workers = self._start_workers(worker_pool=self._worker_pool)
        # Blocks until all tasks are complete
        self._worker_queue.join()
        self.save_to_file()
        self._stop_workers(workers)

        logger.info(f"========================================")
        logger.info(f"== GRAND TOTAL: {self.grand_total}")
        logger.info(f"== TOTAL PROCESS: {self.total}")
        logger.info(f"== SUCCESSES: {self.success}")
        logger.info(f"== FAILED: {self.total - self.success}")

    @staticmethod
    def callback(params):
        logger.info(f"Test callback: {params}")

    def save_to_file(self):
        """
        Save all payload to log
        :return:
        """
        with open('data_log.json', 'w', encoding='utf-8') as f:
            json.dump(self.data_log, f, ensure_ascii=False, indent=4)


if __name__ == "__main__":
    def gen_payload(external_order_id):
        return {
            "entity": {
                "order_origin": "ARS",
                "external_order_id": external_order_id,
                "base_currency_code": "CAD",
                "base_discount_amount": -4.5,
                "base_grand_total": 45.5,
                "base_shipping_amount": 5,
                "base_subtotal": 45,
                "base_tax_amount": 0,
                "customer_email": "gmq@yopmail.com",
                "customer_firstname": "Giap",
                "customer_group_id": 1,
                "customer_id": 336,
                "uuid": "fae009fe72114af28187092fd522da4a",
                "customer_is_guest": 0,
                "customer_lastname": "Minh Quan",
                "customer_note_notify": 1,
                "discount_amount": -4.5,
                "email_sent": 1,
                "coupon_code": "",
                "discount_description": "",
                "grand_total": 45.5,
                "is_virtual": 0,
                "order_currency_code": "CAD",
                "shipping_amount": 5,
                "shipping_description": "",
                "state": "processing",
                "status": "processing",
                "store_currency_code": "CAD",
                "store_id": 3,
                "store_name": "Canon CA Base\nCanon CA\nEN",
                "subtotal": 45,
                "subtotal_incl_tax": 45,
                "tax_amount": 0,
                "total_item_count": 1,
                "total_qty_ordered": 1,
                "weight": 1,
                "items": [
                    {
                        "external_order_item_id": "40201",
                        "base_discount_amount": 4.5,
                        "base_original_price": 0.43,
                        "base_price": 0.43,
                        "base_price_incl_tax": 45,
                        "base_row_invoiced": 0,
                        "base_row_total": 45,
                        "base_tax_amount": 0,
                        "base_tax_invoiced": 0,
                        "discount_amount": 4.5,
                        "discount_percent": 10,
                        "free_shipping": 1,
                        "is_virtual": 0,
                        "name": "Push It Messenger Bag",
                        "original_price": 45,
                        "price": 45,
                        "price_incl_tax": 45,
                        "product_id": 14,
                        "product_type": "simple",
                        "qty_ordered": 1,
                        "row_total": 45,
                        "row_total_incl_tax": 45,
                        "sku": "6882A003AA",
                        "store_id": 3
                    }
                ],
                "billing_address": {
                    "my_canon_address_id": "fd701613ef3b44829b6b53eacf471725ádasdasdasdasdasdasdz",
                    "address_type": "billing",
                    "city": "Winnipeg",
                    "company": "",
                    "country_id": "CA",
                    "email": "gmq@yopmail.com",
                    "firstname": "Giap",
                    "lastname": "Minh Quan",
                    "postcode": "R2K2Z4",
                    "region": "Manitoba",
                    "region_code": "ON",
                    "region_id": 68,
                    "street": [
                        "493 London St"
                    ],
                    "telephone": "2046543854"
                },
                "extension_attributes": {
                    "shipping_assignments": [
                        {
                            "shipping": {
                                "address": {
                                    "my_canon_address_id": "fd701613ef3b44829b6b53eacf471723",
                                    "address_type": "shipping",
                                    "city": "Winnipeg",
                                    "company": "",
                                    "country_id": "CA",
                                    "customer_address_id": 2,
                                    "email": "gmq@yopmail.com",
                                    "firstname": "Giap",
                                    "lastname": "Minh Quan",
                                    "postcode": "R2K2Z4",
                                    "region": "Manitoba",
                                    "region_code": "ON",
                                    "region_id": "68",
                                    "street": [
                                        "493 London St"
                                    ],
                                    "telephone": "2046543854"
                                },
                                "method": "freeshipping_freeshipping"
                            }
                        }
                    ]
                },
                "payment": {
                    "method": "moneris",
                    "moneris_token": "agpEL5LG8NMGdk1wEgU0Kfw44",
                    "cavv": "",
                    "eci": "7",
                    "credit_card_number": "0004***0004",
                    "credit_card_expired": "2311",
                    "three_ds_trans_id": "",
                    "three_ds_version": "",
                    "threeds_type": False
                }
            }
        }


    # Dummy tasks
    for i in range(10):
        worker = WorkerService("https://shop.qa.canon.ca/index.php")
        worker.api.access_token = 'eyJraWQiOiIxIiwiYWxnIjoiSFMyNTYifQ.eyJ1aWQiOjE3NzksInV0eXBpZCI6MiwiaWF0IjoxNjcwMzg0ODMxLCJleHAiOjE2NzAzODg0MzF9.mRGL-22qBW3xhK5d5QR5fvZCquzIECptr9ASSLxGMHo'
        worker.set_worker_pool(10)
        worker.set_wait_second_for_each_process(0)
        endpoint_url = None
        for idt in range(10):
            item = gen_payload(str(uuid.uuid4()))
            # worker.create_queue(endpoint_url, item, worker.callback, idt)
            worker.create_queue(endpoint_url, item, None, idt)
        worker.grand_total = i * 10
        worker.run()
        print("----------------------------------------")
        # time.sleep(2)
