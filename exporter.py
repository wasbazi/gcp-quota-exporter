from time import sleep
from os import environ

from googleapiclient import discovery
from prometheus_client import Gauge, start_http_server
from oauth2client.client import GoogleCredentials

credentials = GoogleCredentials.get_application_default()
service = discovery.build('compute', 'v1', credentials=credentials)

project = environ.get("GOOGLE_PROJECT_ID")
region = environ.get("GOOGLE_PROJECT_REGION")


labels = ('project', 'region', 'quota')
limit_guage = Gauge('gcp_quota_stats_limit',  'quota limits in google cloud',
                    labels)
usage_guage = Gauge('gcp_quota_stats_usage',  'quota limits in google cloud',
                    labels)


def record_quota(quota, region):
    name = quota["metric"].lower()
    limit = quota["limit"]
    usage = quota["usage"]

    limit_guage.labels(project=project, region=region, quota=name).set(limit)
    usage_guage.labels(project=project, region=region, quota=name).set(usage)


def get_global_quotas():
    return service.projects().get(project=project).execute()


def get_regional_quotas():
    return service.regions().get(project=project, region=region).execute()


def load_quotas():
    regional_quotas = get_regional_quotas()['quotas']
    for q in regional_quotas:
        record_quota(q, region)

    global_quotas = get_global_quotas()['quotas']
    for q in global_quotas:
        record_quota(q, "global")


def main():
    start_http_server(environ.get("PORT", 8080))

    while True:
        load_quotas()
        sleep(15)


if __name__ == "__main__":
    main()
