# import os
from datetime import datetime
import os
import sys
import time

import stix2
import yaml
from src.lib.external_import import ExternalImportConnector
from pycti import OpenCTIConnectorHelper, get_config_variable

class CustomConnector(ExternalImportConnector):
    def __init__(self):
                # Instantiate the connector helper from config
        config_file_path = os.path.dirname(os.path.abspath(__file__)) + "/config.yml"
        config = (
            yaml.load(open(config_file_path), Loader=yaml.SafeLoader)
            if os.path.isfile(config_file_path)
            else {}
        )
        self.helper = OpenCTIConnectorHelper(config)
        self.custom_attribute = get_config_variable(
            "TEMPLATE_ATTRIBUTE", ["template", "attribute"], config
        )
        self.interval = '10s'
    
    

    def _collect_intelligence(self) -> []:
        """Collects intelligence from channels

        Add your code depending on the use case as stated at https://docs.opencti.io/latest/development/connectors/.
        Some sample code is provided as a guide to add a specific observable and a reference to the main object.
        Consider adding additional methods to the class to make the code more readable.

        Returns:
            stix_objects: A list of STIX2 objects."""
        self.helper.log_debug(
            f"{self.helper.connect_name} connector is starting the collection of objects..."
        )
        stix_objects = []

        # ===========================
        # === Add your code below ===
        # ===========================
        self.helper.log_debug("Creating a sample reference using STIX2...")
        main_reference = stix2.ExternalReference(
            source_name="GitHub",
            url="https://github.com/OpenCTI-Platform/connectors",
            description="A sample external reference used by the connector.",
        )

        self.helper.log_debug("Creating an observable for the IPv4...")
        ipv4_observable = stix2.IPv4Address(
            value="2.2.2.2",
            object_marking_refs=[stix2.TLP_GREEN],
            custom_properties={
                "description": "A sample observable created for the tutorial.",
                "labels": ["test", "tutorial"],
                "x_opencti_create_indicator": False,
                "external_references": [main_reference],
            },
        )
        stix_objects.append(ipv4_observable)
        bundle = self.helper.stix2_create_bundle(stix_objects)
        # ===========================
        # === Add your code above ===
        # ===========================
        timestamp = int(time.time())
        self.helper.log_info(
            f"{len(stix_objects)} STIX2 objects have been compiled by {self.helper.connect_name} connector. "
        )
        now = datetime.fromtimestamp(timestamp)
        friendly_name = "Custom connector run @ " + now.strftime(
                        "%Y-%m-%d %H:%M:%S"
                    )
        work_id = self.helper.api.work.initiate_work(
                        self.helper.connect_id, friendly_name
                    )
        self.helper.send_stix2_bundle(
                            bundle,work_id=work_id,
                        )
        message = "Connector successfully run, storing last_run as " + str(
                        timestamp
                    )
        self.helper.api.work.to_processed(work_id, message)
        return stix_objects

    def get_interval(self) -> int:
        return int(self.interval) * 60 * 60 * 24
    
if __name__ == "__main__":
    try:
        connector = CustomConnector()
        connector.run()
    except Exception as e:
        print(e)
        time.sleep(10)
        sys.exit(0)
