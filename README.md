<h1 align="center"> Bible Reading Monitoring App </h1> <br>

<p align="center">
  <img src="https://github.com/jenniferatalya/BibleMonitoringApp/assets/96117065/99b14fc2-cd47-4841-82e3-64a06bf6acf5" width="700px"><br>
  <a href="http://bacaalkitab.web.id/" target="_blank"><img src="https://github.com/jenniferatalya/BibleMonitoringApp/assets/96117065/8f1fca74-9ebc-434d-95db-44a41a8f4d37" width="300px"></a>
</p>

## Introduction
<p align="justify">
In the current digital era, many Bible study groups utilize instant messaging applications such as WhatsApp to share Bible verses and discuss their readings. However, monitoring the reading progress of each group member often becomes a challenging and time-consuming task. This issue is also faced by the Bible study groups at GRII Solo and Yogyakarta. To address this challenge, a web-based application equipped with data analytics features and Machine Learning (ML)-based CRUD (Create, Read, Update, and Delete) functionality has been designed and developed to track members' reading progress and enhance monitoring across multiple Bible study groups. Furthermore, with the support of ML and Regular Expression (RegEx), this application can automatically summarize instant messaging reports of members' readings and provide a clearer overview through data analytics features. This application enables Bible study group leaders to easily record members who have completed their Bible readings and monitor the reading progress of each member. With a dashboard presenting the reading progress of each member, it is expected to facilitate leaders in identifying members who are lagging behind and understanding the development of each group under their supervision. Additionally, the web application allows group leaders to manage members, groups, churches, devotions, and administrators. It is hoped that this application can make a positive contribution to strengthening the Bible study group community, particularly at GRII Solo and Yogyakarta.
</p>


## Main Features

A few of the things you can do with this web application:

* Automatic Recapitulation

<p>
  <img width="600" alt="Screenshot 2024-06-12 at 13 34 55" src="https://github.com/jenniferatalya/BibleMonitoringApp/assets/96117065/54572352-84aa-4d39-b4a2-28e30d3073bb">

</p>
  
* Data Analytics (Dashboard)
<p>
  <img width="600" alt="Screenshot 2024-05-17 at 17 39 04" src="https://github.com/jenniferatalya/BibleMonitoringApp/assets/96117065/9900a4f2-693a-4e14-8003-ac862f153898">
</p>

* Data Management (CRUD)
<p>
  <img width="1000" alt="Screenshot 2024-05-17 at 17 39 04" src="https://github.com/jenniferatalya/BibleMonitoringApp/assets/96117065/35462e09-e55e-401e-99b5-e0a30a106324">
</p>

## Built With
<div>
  <a href="https://www.python.org/" target="_blank"><img src="https://github.com/jenniferatalya/BibleMonitoringApp/assets/96117065/368a6ae9-59aa-4137-874b-5f615f1c3d77" width="90px"></a> &nbsp;&nbsp;
  <a href="https://scikit-learn.org/stable/" target="_blank"><img src="https://github.com/jenniferatalya/BibleMonitoringApp/assets/96117065/9b14503e-a29f-4adb-b988-75db5649b04f" width="200px"></a> &nbsp;&nbsp;
  <a href="https://www.mysql.com/" target="_blank"><img src="https://github.com/jenniferatalya/BibleMonitoringApp/assets/96117065/5e8f4608-6c34-401a-9a66-bff55b4349fb" width="200px"></a> &nbsp;
</div><br><br>
<div>
  <a href="https://html.com/" target="_blank"><img src="https://github.com/jenniferatalya/BibleMonitoringApp/assets/96117065/804edd5a-6c36-4be6-b847-355be039a6c4" width="100px"></a> &nbsp;&nbsp;
  <a href="" target="_blank"><img src="https://github.com/jenniferatalya/BibleMonitoringApp/assets/96117065/0d8683cb-dd4f-4d03-9bde-b1724a025ab7" width="71px"></a> &nbsp;&nbsp;
  <a href="https://www.javascript.com/" target="_blank"><img src="https://github.com/jenniferatalya/BibleMonitoringApp/assets/96117065/bf521020-c25e-47f2-8079-7e5fe089da80" width="93px"></a> &nbsp;&nbsp;
  <a href="https://www.chartjs.org/" target="_blank"><img src="https://github.com/jenniferatalya/BibleMonitoringApp/assets/96117065/a1d9a8eb-24b6-419f-9935-1e6486d57027" width="100px"></a> &nbsp;
</div>

## Getting Started

1. **Clone the Repository**
  ```sh
  git clone https://github.com/jenniferatalya/BibleMonitoringApp.git
  ```

2. **Create Virtual Environment With Python 3.11.5 (recommended)**
  ```sh
  conda create -n yourenvname python=3.11.5
  conda activate yourenvname
  ```

3. **Install Requirements**
  ```sh
  pip install -r requirements.txt
  ```

4. **Turn On MySQL From XAMPP or WampServer**

   Before starting the project, ensure that MySQL is active on your local server. If you're using XAMPP or WampServer, follow these steps to enable MySQL:

   <img width="450" alt="Screenshot 2024-06-12 at 14 27 02" src="https://github.com/jenniferatalya/BibleMonitoringApp/assets/96117065/b5953020-97dc-4e62-8cad-dc9c4accb9f0">

5. **Import the Database**
   * Open your preferred database management tool (this could be phpMyAdmin).
   * Look for an option to import a database. In most tools, you'll find this under a menu labeled "Import" or "Import/Export".
   * Select the database file you want to import. This file should be in a format supported by your database management tool (usually SQL or a compatible format).

6. **Configure Local Database**

   Before starting the project, change the username to your mysql username, the default username should be root

    <img width="584" alt="Screenshot 2024-06-12 at 14 30 10" src="https://github.com/jenniferatalya/BibleMonitoringApp/assets/96117065/9a6c9a5e-5a43-4849-a470-886cb727861d">

7. **Run The Project**

   Follow these steps to run the project:

   - Navigate to the project directory in your terminal:
     ```sh
     cd BibleMonitoringApp
     ```

   - Make sure your virtual environment is activated, then execute the following command:
     ```sh
     python main.py
     ```

   The project will automatically open in your default browser at http://localhost:8080.


## Contributors

<a href="https://github.com/jenniferatalya" target="_blank"><img src="https://github.com/jenniferatalya/BibleMonitoringApp/assets/96117065/bc8ba3ec-ecb4-400a-91d9-67d94cbf78e9" width="100px"></a> &nbsp;
<a href="https://github.com/renatavalencia" target="_blank"><img src="https://github.com/jenniferatalya/BibleMonitoringApp/assets/96117065/615fc9b5-8892-418d-b236-fea146bd654f" width="100px"></a>

## Contact

Jennifer Atalya - jenniferdjohari@gmail.com <br>
Renata Valencia - rntvlnc@gmail.com
