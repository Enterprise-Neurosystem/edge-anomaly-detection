# Edge Anomaly Detection - Workshop Instructions
<details>
<summary>Table of Contents</summary>
<p>

* [Log into RHODS](#logging-into-rhods)
* [Git Clone the Edge Anomaly Detection Project](#git-clone-the-edge-anomaly-detection-project)
* [Run the Anomaly Detection notebook](#run-anomaly-detection-notebook)
* [Package the application](#select-slice)
* [View Application via browser](#stream-sensor-data)

</p>
</details>

## Log into RHODS

1. Go to the [OpenShift console](https://console-openshift-console.apps.ieee.8goc.p1.openshiftapps.com/) and click on **WorkshopAttendees** and log in with your credentials.

    ![](/workshop/images/workshop_attendees.png)

2. Upon successful login, you will see the Red Hat OpenShift Dedicated environment.  This is a kubernetes platform from which you can create containerized applications.  Part of this environment is the Red Hat OpenShift Data Science platform.  It is accessed by selecting the launcher icon in the upper right corner.

   ![](/workshop/images/launchericon.png)

3. Click on **Log in with OpenShift** and then click on **WorkshopAttendees** and log in with your credentials.

    ![](/workshop/images/openshift_login.png)

4. Click on **Allow selected permissions** to authorize access. 

    ![](/workshop/images/authorize_access.png)

5. Once in the RHODS dashboard, click on the **Launch Application** hyperlink in the JupyterHub tile.

    ![](/workshop/images/rhods_jupyterhub.png)

6. Again, click on **WorkshopAttendees** and log in with your credentials and click on **Allow selected permissions**

7. Choose **Standard Data Science** as the notebook image and select a **small** notebook size.

    ![](/workshop/images/jupyterhub_nb.png)

8. Click on "Start Server"

## Git Clone the Edge Anomaly Detection Project 
1. Click on the Git icon on the left of your JupyterHub notebook. 

2. Click on the **Clone a Repository** button.

    ![](/workshop/images/git_clone.png)

3. Paste the following URL and click **Clone**.
 
    ```
    https://github.com/Enterprise-Neurosystem/edge-synthetic-data-generator.git
    ```
## Generate Sensor Data

1. Now that we've cloned the project, let's generate synthetic sensor data from a notebook. 

2. Open the notebook named `12_generate_sensor_data.ipynb` from the File Explorer tab. 

    ![](/workshop/images/generate_sensor_data.png)

3.  Run cells 1-6 by selecting each one and clicking the run button. 

    ![](/workshop/images/run_cells.png)

## Select Slice

1. Once you run the first 6 cells and reach the section titled **Selecting your slice**, enter in your slice number in the following cell. For example, if your slice number is 13, your code should resemble the following:

    ![](/workshop/images/select_slice.png)

2. After inputting your slice number, run the cell to plot the sensor data for that slice:

    ![](/workshop/images/slice_13_plot.png)

## Stream Sensor Data
Now that you've selected a slice of synthetic data, it's time for you to stream your data via Apache Kafka to the sensor failure prediction model for ingestion. 

1. First, attach a fake timestamp to each instance of synthetic data, making it time series data, by running the first four cells in this section. 

    ![](/workshop/images/streaming_sensor_data.png)

2. Now that you've transformed your data into time series data, define the Kafka cluster credentials by running the following cell:
  
    ![](/workshop/images/kafka_connect.png)

3. Finally, stream your data by running the remaining two cells, which (1) connects to the Kafka cluster based on the credentials you defined in the previous step, (2) initializes a KafkaProducer object, (3) streams your data to the sensor failure prediction model.

    ![](/workshop/images/produce_data.png)









