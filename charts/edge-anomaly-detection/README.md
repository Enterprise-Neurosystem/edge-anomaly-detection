# Edge Anomaly Detection Helm Chart

[Helm](https://helm.sh) chart to support the deployment of the Edge Anomaly Detection to Kubernetes.

## Installing the Chart

This chart supports specifying parameters in order to customize the behavior for the environment. See the [values.yaml](values.yaml) file for the list of available parameters.

The following parameters are required:

* Location containing the image
* Hostname(s) exposing the application via an _Ingress_

To install the chart, execute the following command while also providing the required parameters:

```shell
helm upgrade -i edge-anomaly-detection --set image=<IMAGE_LOCATION> --set ingress.hosts[0].host=<HOSTNAME>
```

Access the application at the hostname provided.
