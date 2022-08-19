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

   ![](/workshop/images/RedHatOpenShiftDashboard.png)

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

12. To start working we are going to clone the Edge Anomaly Detection project from github.


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
  
   ![](/workshop/images/AnomalyDetectionNotebook.png)

3. The data we will be using (casing1.csv) has 2 columns timestamp and pressure. This data has already been refactored. If you wish to look at the non-refactored data, open file static/data/casing_NotRefactored.csv. The dataset is from a gas pump that is slowly failing overtime. Let's plot this data to see what it looks like. Can we see an anomaly in the visible data?  Run Cells 1-3

    ![](/workshop/images/plotCasingPressurePoints.png)

4. We can see from the above plot that the pressure decreases over time and towards the end we observe some pressure points that have extremely high values. This could be an anomaly but how do we quantify these points? What we can do is perform a linear regression. From the linear regression we can take the percent difference from the regression line and plot that line over our points. Any lines extending beyond a certain distance from our points we can then label as 'an anomaly'
5. Run the remainder of the notebook cells.  We will produce a new plot which will show linear regression and a green line showing the percent difference from the regression line.  When this line is over a certain percentage away from the average linear regression we color it red, to signify that it is an anomaly.  Look at notebooks/anomaly2.png

    ![](/workshop/images/anomaly2.png)

## Creating a Web UI for our algorithm.  

1. We have created a Web UI in which users can choose which dataset they wish to view anomalies for.  The Web UI consists of an HTML page in which users can select different options for plotting such as: Data Source, Regression Group Size, STD Threshold, Plot Scrolling Size, Points per Second.

   ![](/workshop/images/AnomalyDetectionOptions.png)

2. There are 3 sections within the Web UI:  Data Source, Plot Parameters and Actions
3. Data Source - currently you can choose the default casing1.csv which we have prepared.
4. Plot Parameters include: Regression Group Size, STD Threshold, Plot Scrolling Size and Points per Second.
5.      Regression Group Size - number of points used in the calculation of a regression line
6.      STD Threshold - How many standard deviations, from the regression line, do you wish to set before anything above that threshold is listed as an anomaly
7.      Plot Scrolling Size - how many points are plotted in the plot 'window' at any one time
8.      Points per Second - how many pressure points are plotted per second
9. Actions include:  Start Plot and Stop Plot
10.     Start Plot - will start the plotting of the plot
11.     Stop Plot - will stop the plotting of the plot

   ![](/workshop/images/AnomalyDetectionWebUI.png)

12. The Web UI uses an HTML FORM which upon 'submit' posts its options to plot.js which in turn uses services to plot the graph.  In this workshop we will not go into detail as to how we set up the services, templates and static scripts.  Let's go ahead and containerize this application and deploy it on OpenShift.

13. Let's now take our web application and containerize it.

## Packaging the Anomaly Detection Web Application

1. Now that the application code is working, you’re ready to package it as a container image and run it directly in OpenShift as a service that you will be able to call from any other application.

2. We build the application inside OpenShift.  You can access the OpenShift Dedicated dashboard from the application switcher in the top bar of the RHODS dashboard.
   
   ![](/workshop/images/LauncherIcon.png)

3. Open your OpenShift UI and switch to the developer view from the menu on the top left:

   ![](/workshop/images/Switch2DeveloperView.png)

4. Make sure you are in the project that was assigned to you:

   ![](/workshop/images/UserProject1.png)

5. From the +Add menu, click the From Git option:

   ![](/workshop/images/addGitRepo.png)

6. In the Git Repo URL field, enter 

    ```
    https://github.com/Enterprise-Neurosystem/edge-anomaly-detection.git
    ```
   ![](/workshop/images/ImportFromGit.png)

7. Next, change the BUILDER PYTHON to Python 3.8 (UBI7).  Click Edit Import Strategy, then select 3.8 - ubi7 from the drop down list.

   ![](/workshop/images/ImportStrategy.png)

8. If you continue to scroll down, you will see that everything is automatically selected to create a deployment of your application, as well as a route through which you will be able to access it. 

9. Make certain to name your app.  For example:  edge-anomaly-detection

   ![](/workshop/images/GeneralOptionsCreateContainer.png)

10. Now we are ready to press the 'Create' button to create our containerized application.

11. The automated build process will take a few minutes. Some alerts may appear if OpenShift tries to deploy the application while the build is still running, but that’s OK. Then OpenShift will deploy the application (rollout), and in the topology view, you should obtain a screen similar to the following screen capture.

   ![](/workshop/images/TopologyView.png)

12.  We are now ready to view the Anomaly Detection application in a Browser.

## View Application via Browser

13. To view your containerized application in a browser, click the URL icon in the topology view.

   ![](/workshop/images/ClickURL.png)
   
14. Your containerized Anomaly Detection application will now appear in a browser window.  Try the various options (.e.g STD Threshold) that we discussed earlier.

   ![](/workshop/images/AnomalyDetectionApplication.png)
   
15. You are now finished with this part of the workshop.  Next, you will be looking at how we generate Synthetic Data.