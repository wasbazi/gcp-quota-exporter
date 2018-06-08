# GCP Quota Exporter for Kubernetes

This repo handles providing quota metrics from GCP in Prometheus format.
Allowing the data to easily be scraped.


## Deploying

An example kubernetes deployment file has been included at `app.yaml`

It assums that you have a secret called `quota-secrets` with the following values:
- `google_project_id` - Project in GCP you want to monitor
- `google_project_region` - Region in GCP you want to monitor
- `google_auth.json` - Authentication file for a service account


## Environment Configuration

The configuration for quota exporter can be configured through environment
variables, these are exposed:

- `PORT` - defaults to `8080`
- `GOOGLE_PROJECT_ID` - specify the project from which you want to monitor quotas
- `GOOGLE_PROJECT_REGION` - specify the region from which you want to monitor
quotas


## Prometheus Configuration

This relies on a pod scraping configuration for prometheus:

```yaml
      # Example scrape config for pods
      #
      # The relabeling allows the actual pod scrape endpoint to be configured via the
      # following annotations:
      #
      # * `prometheus.io/scrape`: Only scrape pods that have a value of `true`
      # * `prometheus.io/path`: If the metrics path is not `/metrics` override this.
      # * `prometheus.io/port`: Scrape the pod on the indicated port instead of the default of `9102`.
      - job_name: 'kubernetes-pods'

        kubernetes_sd_configs:
          - role: pod

        relabel_configs:
          - source_labels: [__meta_kubernetes_pod_annotation_prometheus_io_scrape]
            action: keep
            regex: true
          - source_labels: [__meta_kubernetes_pod_annotation_prometheus_io_path]
            action: replace
            target_label: __metrics_path__
            regex: (.+)
          - source_labels: [__address__, __meta_kubernetes_pod_annotation_prometheus_io_port]
            action: replace
            regex: (.+):(?:\d+);(\d+)
            replacement: ${1}:${2}
            target_label: __address__
          - action: labelmap
            regex: __meta_kubernetes_pod_label_(.+)
          - source_labels: [__meta_kubernetes_namespace]
            action: replace
            target_label: kubernetes_namespace
          - source_labels: [__meta_kubernetes_pod_name]
            action: replace
            target_label: kubernetes_pod_name
```
