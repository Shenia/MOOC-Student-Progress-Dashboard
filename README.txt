*************************************************************************************************************
UBC Arts ISIT 
Work Learn S19: Learning Analytics/Visual Analytics
Project Title: Progress Dashboard for edX MOOC Students - A Proof of Concept (Demo Version)
Supervisor: Sanam Shirazi
Student: Yan Shao (Shenia) Tung
Date: August 27, 2019
*************************************************************************************************************
For use with existing xls files, the programs requires the following software:
Python 3

For full set-up, the program requires the following data services and software:
edX Data Package
Google BigQuery
Tableau Desktop
edX Insights Courseware
Python 3
*************************************************************************************************************
To run with existing xls files, change the path variable in appShared.py and run appShared.py on local 
browser at http://127.0.0.1:2000/
To run full set-up, see Final Documentation
*************************************************************************************************************
This program consists of the following files:
\README.txt
\appShared.py
\CSVs\Video Quizzes Info\current_QV.xlsx
\CSVs\Video Quizzes Info\past_QV.xlsx
\CSVs\Discussion Posts\current_D.xlsx
\CSVs\Discussion Posts\past_D.xlsx
\CSVs\Discussion Views\current_DV.xlsx
\CSVs\Discussion Views\past_DV.xlsx
\CSVs\Discussion Mapping\current_DM.xlsx
\CSVs\Discussion Mapping\past_DM.xlsx

SQL queries are required for some parts of the program. All SQL queries are stored in the following files:
(In demo version, all course id's in SQL files are removed for privacy reasons, thus these files will not run with set up)
\CSVs\Video Quizzes Info\student_video_quiz_current.sql
\CSVs\Video Quizzes Info\student_video_quiz_past.sql
\CSVs\Discussion Posts\posts.sql
\CSVs\Discussion Views\postViews.sql
\CSVs\Discussion Mapping\discussionMapping.sql

This program produces the following output files:
\CSVs\Python Outfiles (raw)\rawcurrent.csv
\CSVs\Python Outfiles (raw)\rawpast.csv

This folder contains a comprehensive report on this project
\Final Documentation Sharable.docx
*************************************************************************************************************