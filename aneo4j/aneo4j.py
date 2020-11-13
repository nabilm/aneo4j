from concurrent import futures

import logging
from neo4j import GraphDatabase, READ_ACCESS, WRITE_ACCESS
from neo4j.exceptions import ServiceUnavailable

import time
import traceback

# How long to wait after each successive failure.
RETRY_WAITS = [0, 1, 4]


class AsyncNeo4j:
    """
    Async neo4j connection/query wrapper
    """

    def __init__(self, config: dict, loop: object):
        """
        Create executer for running asyn calls
        """
        self.config = config
        self.loop = loop
        self.executer = futures.ThreadPoolExecutor(max_workers=30)
        # retry mechanism
        for retry_wait in RETRY_WAITS:
            try:
                self.init_driver()
                break
            except Exception:
                if retry_wait == RETRY_WAITS[-1]:
                    raise
                else:
                    logging.error("WARNING: retrying to Init DB; err:")
                    traceback.print_exc()
                    time.sleep(retry_wait)

    def init_driver(self):
        """
        neo4j driver initializer
        """
        self.driver = GraphDatabase.driver(
            self.config["uri"], auth=(self.config["user"], self.config["password"])
        )

    def create_transation(self, quey_function: object, query: str, mode=READ_ACCESS):
        """
        Create neo4j session transaction
        transactions allow the driver to handle retries and transient errors
        """

    @staticmethod
    def _run_query(tx, query: str, **kwargs):
        """
        Run neo4j query
        """
        result = tx.run(query, **kwargs)
        try:
            return [record for record in result]

        # Capture any errors along with the query and data for traceability
        except ServiceUnavailable as exception:
            logging.error(
                "{query} raised an error: \n {exception}".format(
                    query=query, exception=exception
                )
            )
            raise

    async def run_query(self, query: str, read: bool, **kwargs):
        """
        Read query neo4j
        """

        def run_transaction():
            """
            Run a read query
            """
            with self.driver.session() as session:
                # Write transactions allow the driver to handle
                # retries and transient errors
                if read:
                    result = session.read_transaction(self._run_query, query, **kwargs)
                else:
                    result = session.write_transaction(self._run_query, query, **kwargs)

                for record in result:
                    yield dict(record)

        return await self.loop.run_in_executor(None, run_transaction)