Coded by Daniel Lesniak
This is the time tracker for the cosmetology class.

Run the scanner.py program to open the base UI for the check-in and check-out system. Students may manually input their student number or scan their ID to have it automatically pasted into the box.

The times you check in and the times you check out are logged in your private .json file in the student_logs folder. Your compiled time will show at the top of this file. The master_log.json file pulls the compiled time from each individual file and pastes it with the student number for data consolidation.

A web app has been programmed and can be run locally via the runhtml.py file. It pulls the data from the master_log.json that is uploaded to a GitHub repo and turns it into a table on a visually appealing website.

IMPORTANT!
After every use of the check-in/check-out software, you must push the updated logs to the GitHub repo the webpage pulls from. If you do not the updated data is still saved on your local machine, it just cant be accessed through the web-app
----------------------------------------------------------------------------------------------------------------------------------------------------------------------
Step 1: Open a terminal/command prompt
Navigate to the folder where the student_logs are stored. This is typically inside your project directory.

Step 2: Stage the Student_logs folder
Run the following command in your terminal to stage only the Student_logs folder for commit:

git add Student_logs

This tells Git to track changes in the Student_logs folder.

Step 3: Commit the changes
Now commit the changes by running the following command:

git commit -m "Update student logs"

This commits the changes to your local repository with a message indicating that the logs have been updated.

Step 4: Push the changes to GitHub
To push the changes to the remote repository, run:

git push origin main

This will upload the updated Student_logs folder to the GitHub repository at https://github.com/poptarts-tasty-af/Student-Cosmo-Logs.git.
--------------------------------------------------------------------------------------------------------------------------------------------------------------------

If you need any help with github configuration I am here to help setup the application if needed. Contact me at lesniakdm@s.dcsdk12.org
