import os
import unittest

import bioblend
from bioblend.galaxy import GalaxyInstance
from . import test_util

bioblend.set_stream_logger("test", level="INFO")

BIOBLEND_TEST_JOB_TIMEOUT = int(os.environ.get("BIOBLEND_TEST_JOB_TIMEOUT", "60"))


@test_util.skip_unless_galaxy()
class GalaxyTestBase(unittest.TestCase):
    gi: GalaxyInstance

    @classmethod
    def setUpClass(cls):
        galaxy_key = os.environ["BIOBLEND_GALAXY_API_KEY"]
        galaxy_url = os.environ["BIOBLEND_GALAXY_URL"]
        cls.gi = GalaxyInstance(url=galaxy_url, key=galaxy_key)

    def _test_dataset(self, history_id: str, contents: str = "1\t2\t3", **kwds) -> str:
        tool_output = self.gi.tools.paste_content(contents, history_id, **kwds)
        return tool_output["outputs"][0]["id"]

    def _wait_and_verify_dataset(self, dataset_id, expected_contents, timeout_seconds=BIOBLEND_TEST_JOB_TIMEOUT):
        dataset_contents = self.gi.datasets.download_dataset(dataset_id, maxwait=timeout_seconds)
        assert dataset_contents == expected_contents
