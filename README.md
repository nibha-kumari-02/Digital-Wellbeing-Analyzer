 Digital Wellbeing Analyzer
 Project Overview

Digital Wellbeing Analyzer is a Python-based desktop application that automatically tracks the time spent on different applications on a Windows computer.

It monitors the currently active application, calculates usage time, categorizes applications into different groups, and displays usage statistics through an interactive dashboard.

The main objective of this project is to help users understand their computer usage habits, improve productivity, and maintain a healthy balance between study, work, and entertainment.

🎯 Objectives
Automatically track active application usage.
Monitor user idle time to avoid counting inactive periods.
Categorize applications based on their purpose.
Display total application usage time.
Analyze study, social media, and entertainment time.
Visualize application usage through graphs.
Export usage reports in CSV format.
 Features
1. Automatic Application Tracking
Detects the currently active Windows application.
Retrieves application names and window titles.
Tracks application usage automatically.
2. Idle Time Detection
Detects keyboard and mouse inactivity.
Excludes usage periods when the user is idle for 60 seconds or more.
3. Application Categorization

Applications are classified into five categories:

Category	Examples
Study	VS Code, Python, PyCharm, MS Word
Social Media	WhatsApp, Telegram, Discord
Entertainment	Spotify, VLC, Steam
Browser	Chrome, Edge, Firefox
Other	Applications not listed above
4. Interactive Dashboard

The dashboard displays:

Total Usage Time
Study Time
Social Media Time
Entertainment Time
Currently Active Application
Application Usage Details
5. Usage Analytics
Displays graphical application usage statistics.
Uses Matplotlib bar charts.
Compares time spent across application categories.
6. CSV Report Export
Exports application usage statistics.
Saves reports as wellbeing_report.csv.
Allows users to analyze their usage data separately.
🛠️ Technologies Used
Technology	Purpose
Python	Core programming language
Tkinter	GUI development
NumPy	Numerical calculations
Pandas	Data handling and analysis
Matplotlib	Data visualization
ctypes	Windows API interaction
Windows API	Active application and idle time detection
💻 System Requirements
Operating System: Windows 10 / Windows 11
Python 3.9 or above
Visual Studio Code (recommended)
Git (for GitHub upload)

Note: This application uses Windows-specific APIs through ctypes, so it is designed for Windows operating systems.

📂 Project Structure
text
Digital-Wellbeing-Analyzer/
│
├── digital_wellbeing.py
│
├── README.md
│
├── requirements.txt
│
└── wellbeing_report.csv


Note: The CSV report is generated after exporting data from the application. It does not need to be included initially.

⚙️ Installation and Setup
Step 1: Clone the Repository
bash
git clone https://github.com/nibha-kumari-02/Digital-Wellbeing-Analyzer.git

Step 2: Open the Project Folder
bash
cd Digital-Wellbeing-Analyzer

Step 3: Install Required Libraries
bash
pip install numpy pandas matplotlib

Step 4: Run the Application
bash
python digital_wellbeing.py

📊 How It Works
The application starts and initializes the dashboard.
Windows API detects the currently active application.
The system checks user idle time.
Active application usage is calculated.
Applications are categorized automatically.
The dashboard updates usage statistics every second.
Matplotlib displays graphical analytics.
Users can export their usage report as a CSV file.
🔒 Privacy and Limitations
Application tracking runs locally on the user's computer.
Usage information is maintained in application memory during execution.
The current version does not include cloud storage or user accounts.
Window titles may contain sensitive information; they are displayed locally and are not automatically uploaded.
Usage statistics are not saved persistently unless exported.
Application categorization is based on predefined executable names.
The application is designed specifically for Windows.
🚀 Future Enhancements
Daily and weekly usage reports.
Productivity score calculation.
Application usage reminders.
Screen-time limits and notifications.
Persistent usage history using SQLite.
More detailed graphical analytics.
Personalized productivity recommendations.
👩‍💻 Author

Nibha Kumari

MCA (AI/ML) Student

GitHub: @nibha-kumari-02

⭐ Conclusion

The Digital Wellbeing Analyzer provides a simple and effective way to monitor computer application usage. By tracking active applications, analyzing screen time, and presenting visual reports, it encourages users to develop better digital habits and improve productivity.

If you find this project useful, don't forget to give it a ⭐ on GitHub!
