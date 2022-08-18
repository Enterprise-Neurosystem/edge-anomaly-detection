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

2. Upon successful login, you will see the Red Hat OpenShift Dedicated environment.  This is a kubernetes platform from which you can create containerized applications.  Part of this environment is the Red Hat OpenShift Data Science platform.  It is accessed by **clicking** the **launcher** icon in the upper right corner.

   ![](/workshop/images/launchericon.png)

3. Upon clicking the **Launcher Icon** you will see another login screen.  Click the **Log in with OpenShift** icon.

   ![](/workshop/images/loginwithopenshift.png)

4. Click on **WorkshopAttendees** and log in with your credentials.

    ![](/workshop/images/workshop_attendees.png)

5. Click on **Allow selected permissions** to authorize access. 

    ![](/workshop/images/authorize_access.png)

6. Once in the RHODS dashboard, click on the **Launch Application** hyperlink in the JupyterHub tile.

    ![](/workshop/images/redhatopenshiftdatascienceplatform.png)

7. Again, click on **WorkshopAttendees** and log in with your credentials and click on **Allow selected permissions**

   ![](/workshop/images/workshop_attendees.png)

8. When you first gain access to JupyterHub, a configuration screen gives you the opportunity to select a notebook image and configure the deployment size and environment variables for your data science project.

    ![](/workshop/images/Notebookserveroptions.png)

9. Choose **Tensorflow** Notebook image, **Small** Container size.  You will not be entering **Environment Variables**.  Once you have chosen these options click the **Start Server** button.  Once the server starts you will be taken into a Jupyter Hub IDE (Integrated Development Environment).  It is in this environment that we can look at our sensor data and determine how to visualize and detect anomalies.

10. Welcome to Jupyter Lab!   After starting your server, three sections appear in JupyterLab's launcher window:  Notebook, Console and Other.  On the left side of the navigation paine, locate the explorer panel.  This panel is where you can create and manager your project directories.
    ![](/workshop/images/JupyterNotebookIDE.png)

11. To start working we are going to clone the Edge Anomaly Detection project from github.


## Git Clone the Edge Anomaly Detection Project 
1. Click on the Git icon on the left of your JupyterHub notebook. 

2. Click on the **Clone a Repository** button.

    ![](/workshop/images/git_clone.png)

3. Paste the following URL and click **Clone**.
 
    ```
    https://github.com/Enterprise-Neurosystem/edge-anomaly-detection.git
    ```
4. After you have cloned your repository, it will appear as a 'directory' under the **Name** pane.

   ![](/workshop/images/namePane.png)

## Run the Anomaly Detection Notebook

1. Now that we've cloned the project, let's take a look at some anomaly data.  Open the notebook named `notebooks\AnomalyDetectionNotebook.ipynb` from the File Explorer tab.
  
2. ![](/workshop/images/AnomalyDetectionNotebook.png)

3. The data we will be using (casing1.csv) has 2 columns timestamp and pressure. This data has already been refactored. If you wish to look at the non-refactored data, open file static/data/casing_NotRefactored.csv. The dataset is from a gas pump that is slowly failing overtime. Let's plot this data to see what it looks like. Can we see an anomaly in the visible data?  Run Cells 1-3

    ![](/workshop/images/plotCasingPressurePoints.png)

4. We can see from the above plot that the pressure decreases over time and towards the end we observe some pressure points that have extremely high values. This could be an anomaly but how do we quantify these points? What we can do is perform a linear regression. From the linear regression we can take the percent difference from the regression line and plot that line over our points. Any lines extending beyond a certain distance from our points we can then label as 'an anomaly'
5. Run the remainder of the notebook cells.  We will produce a new plot which will show linear regression and a green line showing the percent difference from the regression line.  When this line is over a certain percentage away from the average linear regression we color it red, to signify that it is an anomaly.  Look at notebooks/anomaly2.png

    ![](/workshop/images/anomaly2.png)

## Creating a Web UI for our algorithm.  

1. We have created a Web UI in which users can choose which dataset they wish to view anomalies for.  










