import os

import pytest
from pathlib import Path

from container_ci_suite.openshift import OpenShiftAPI

test_dir = Path(os.path.abspath(os.path.dirname(__file__)))

VERSION=os.getenv("SINGLE_VERSION")
if not VERSION:
    VERSION="20-ubi8"

class TestNodeJSAppPostgreSQLExTemplate:

    def setup_method(self):
        self.oc_api = OpenShiftAPI(pod_name_prefix="nodejs-example")
        json_raw_file = self.oc_api.get_raw_url_for_json(
            container="s2i-nodejs-container", dir="imagestreams", filename="nodejs-rhel.json"
        )
        self.oc_api.import_is(path=json_raw_file, name="node")
        json_raw_file = self.oc_api.get_raw_url_for_json(
            container="postgresql-container", dir="imagestreams", filename="postgresql-rhel.json"
        )
        self.oc_api.import_is(path=json_raw_file, name="postgresql")

    def teardown_method(self):
        self.oc_api.delete_project()

    def test_local_template_inside_cluster(self):
        expected_output = "Node.js Crud Application"
        template_json = "../openshift/templates/nodejs-postgresql-persistent.json"
        assert self.oc_api.deploy_template(
            template=template_json, name_in_template="nodejs-example", expected_output=expected_output,
            openshift_args=[
                "SOURCE_REPOSITORY_REF=master",
                f"NODEJS_VERSION={VERSION}",
                "NAME=nodejs-example",
                "POSTGRESQL_VERSION=12-el8"
            ]
        )
        assert self.oc_api.template_deployed(name_in_template="nodejs-example")
        assert self.oc_api.check_response_inside_cluster(
            name_in_template="nodejs-example", expected_output=expected_output
        )


    def test_remote_template_inside_cluster(self):
        expected_output = "Node.js Crud Application"
        template_json = self.oc_api.get_raw_url_for_json(
            container="nodejs-ex", dir="openshift/templates", filename="nodejs-postgresql-persistent.json"
        )
        assert self.oc_api.deploy_template(
            template=template_json, name_in_template="dancer-example", expected_output=expected_output,
            openshift_args=[
                "SOURCE_REPOSITORY_REF=master",
                f"NODEJS_VERSION={VERSION}",
                "NAME=nodejs-example",
                "POSTGRESQL_VERSION=12-el8"
            ]
        )
        assert self.oc_api.template_deployed(name_in_template="nodejs-example")
        assert self.oc_api.check_response_inside_cluster(
            name_in_template="nodejs-example", expected_output=expected_output
        )

    def test_remote_template_by_request(self):
        expected_output = "Node.js Crud Application"
        template_json = self.oc_api.get_raw_url_for_json(
            container="nodejs-ex", dir="openshift/templates", filename="nodejs-postgresql-persistent.json"
        )
        assert self.oc_api.deploy_template(
            template=template_json, name_in_template="nodejs-example", expected_output=expected_output,
            openshift_args=[
                "SOURCE_REPOSITORY_REF=master",
                f"NODEJS_VERSION={VERSION}",
                "NAME=nodejs-example",
                "POSTGRESQL_VERSION=12-el8"
            ]
        )
        assert self.oc_api.template_deployed(name_in_template="nodejs-example")
        assert self.oc_api.check_response_outside_cluster(
            name_in_template="nodejs-example", expected_output=expected_output
        )
