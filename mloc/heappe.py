import json

import heappeac as hp

from .settings import (HEAPPE_USERNAME, HEAPPE_PASSWORD)


class Heappe:
    @staticmethod
    def _get_client():
        configuration = hp.Configuration()
        api_instance = hp.ApiClient(configuration)
        return api_instance

    @staticmethod
    def _authenticate(client=None):
        api_instance = client if client else Heappe._get_client()
        cred = {
            "_preload_content": False,
            "body": {
                "credentials": {
                    "password": HEAPPE_PASSWORD,
                    "username": HEAPPE_USERNAME
                }
            }
        }
        ulm = hp.api.UserAndLimitationManagementApi(api_instance)
        r = ulm.authenticate_user_password(**cred)
        session_code = json.loads(r.data)
        return session_code

    @staticmethod
    def _create_job(session_code, client=None):
        api_instance = client if client else Heappe._get_client()
        jm = hp.api.JobManagementApi(api_instance)
        job_spec_body = {
            "_preload_content": False,
            "body": {
                "jobSpecification": {
                    "name": "my_job",
                    "minCores": 1,
                    "maxCores": 24,
                    "priority": 4,
                    "project": "test_project",
                    "waitingLimit": 0,
                    "walltimeLimit": 600,
                    "clusterNodeTypeId": 7,
                    "environmentVariables": [],
                    "tasks": [
                        {
                            "name": "my_job",
                            "minCores": 1,
                            "maxCores": 24,
                            "walltimeLimit": 600,
                            "standardOutputFile": "stdout",
                            "standardErrorFile": "stderr",
                            "progressFile": "stdprog",
                            "logFile": "stdlog",
                            "commandTemplateId": 2,
                            "environmentVariables": [],
                            "dependsOn": [],
                            "templateParameterValues": [
                                {
                                    "commandParameterIdentifier": "inputParam",
                                    "parameterValue": "test"
                                }
                            ]
                        }
                    ]
                },
                "sessionCode": session_code
            }
        }
        r = jm.create_job(**job_spec_body)
        r_data = json.loads(r.data)
        job_id = r_data["id"]
        return job_id

    @staticmethod
    def _submit_job(job_id, session_code, client=None):
        api_instance = client if client else Heappe.get_client()
        jm = hp.api.JobManagementApi(api_instance)
        submit_body = {
            "_preload_content": False,
            "body":
                {
                    "createdJobInfoId": job_id,
                    "sessionCode": session_code
                }
        }
        r = jm.submit_job(**submit_body)
        r_data = json.loads(r.data)

    @staticmethod
    def submit_fit(fit_id, **kwargs):
        client = Heappe._get_client()
        session_code = Heappe._authenticate(client)
        job_id = Heappe._create_job(session_code, client)
        Heappe._submit_job(job_id, session_code, client)
