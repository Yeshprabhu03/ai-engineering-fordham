https://www.fordham.edu/information-technology/it-services/ramcentral360/appointment-campaigns

# Appointment Campaigns

**For Advisors**

## Overview

A campaign is a great way to organize groups of students and responsibilities. Once a campaign is created, you can quickly take actions that apply to all students within a campaign, such as assigning a task or creating an appointment campaign.

## Create a Campaign

See: [Detailed instructions to create a campaign](https://scribehow.com/shared/Create_Testing_Campaign_Appointment_in_Salesforce_Marketing_Cloud__2I5VaKteSiqrOuksOsrGDQ)

- Navigate to the “Student Success Hub” application. This might be the app shown by default, but if it is not, use the ‘App Launcher’ (the 9 dots at the top-left of the page) to select it.
- Use the dropdown list next to the App Name to navigate to the
**Campaigns**object. - You will see a list view of campaigns. Click the
**New**button in the right-hand corner to start creating a new campaign- Note: The default view is “Recently Viewed” list, but this can be changed by pinning one of the other titles listed in the dropdown menu located next the the “Recently Viewed” title.

- Enter the following information in the “New Campaign: Appointment” screen:
- Campaign Name – limit of 69 characters
- Active – check the box
- Parent Campaign – optional – if you want to create a series of campaigns and hold them in one parent campaign, you are able to do this, but it’s not necessary
- Status – default is ‘Planned’, but should switch to ‘In Progress’ when you are ready to use the campaign
- Ready for Marketing Cloud - Leave blank at this stage
- Start Date – enter the start date of your campaign
- End Date – enter the end date of your campaign
- Note: These dates will be used to track if students have scheduled a meeting as part of this campaign

- Schedule for Deletion? – if you don’t need to keep this campaign for re-use at a later date, then check this box – the campaign will automatically be deleted 6 months after the creation of the campaign record
- Select the college, which will determine the template to use
- Enter the campaign's message subject and content

- After entering the above information, click
**save**- Note: Upon Save, the campaign will automatically be renamed as follows:
**Term**(F22, W22, S22, U22, F23, etc.) +**Your Salesforce Alias**(a short name to identify you) + {**Campaign Name**that you entered initially}**Example: F22_mdavis_My First Campaign**


When you are ready to send the campaign, click Schedule Campaign at the top of the screen.

Within one hour, this will send the campaign message to all students in the campaign and mark them as ‘sent’


## Add students to a Campaign

Once a campaign has been created, students can be added to it as “Campaign Members.” This can be done in three different ways:

**Add from the campaign**

- Within the campaign, locate the dropdown arrow next to the title “Campaign Members.” From here, select “Add Contacts.”
- Enter and select the names of individuals you would like to add to the campaign using the search box.
- At the prompt when adding to a Campaign, you can find and select the appropriate campaign. You should set the “Member Status” to “Not Sent” initially.
- Select “Submit”
- After you’ve added the appropriate students to your ‘Campaign Members’, you will see the number of members in the ‘Campaign Members’ component within your Campaign. From here, you can click the ‘View All’ button to see a list of your students/campaign members.

**Student Enrollment Search**

- Click the app launcher (9 dots in top left of menu bar)
- Select
**Student Success Hub** - Select
**Student Enrollment Search**from the drop-down menu - Enter search criteria and click
**Submit** - Select students to add to the campaign and click
**Add to Campaign** - *If there are more than 50 students, you can advance to the next page and add another 50 students. Repeat as many times as needed
- Choose
**Existing Campaign** - Select your appointment campaign

Click **Submit**

**Add from List view**

- To add contacts in a list view, navigate to the
**Contacts**object from the Student Success Hub menu. - Select the check box next to the individuals you would like added to your campaign.
- Within a contact list view, on the top right click
**Add to Campaign** - At the prompt when adding to a Campaign, you can find and select the appropriate campaign.
- Leave “Member Status” set to “Not Sent” initially
- Click
**Submit** - You will see the number of members in the ‘Campaign Members’ component within your Campaign. From here, you can click the ‘View All’ button to see a list of your students/campaign members.

**Add from a report**

- To use a report for adding contacts to a campaign, navigate to the
**Reports**object using the Student Success Hub menu. Select and Run a report. - In the top right corner, select the down arrow drop-down next to the Edit button to see and click
**Add to Campaign**- Note
**: You cannot select which students to add – all students in the report will be added to the Campaign. You can then use the Campaign Member tools to delete those not needed.**

- Note
- At the prompt when adding to a Campaign, you can find and select the appropriate campaign.
- Leave “Member Status” set to “Not Sent” initially
- Click
**Submit** - You will see the number of members in the ‘Campaign Members’ component within your Campaign. From here, you can click the ‘View All’ button to see a list of your students/campaign members.

## Assign a task

Now that you have the Campaign created and the appropriate Contacts/Students added to your Campaign, you may now proceed to create a task to assign to all the students within this campaign.

- Navigate to the
**Campaigns**object in the Student Success Hub. - Locate and select the desired Campaign you’ve created and populated.
- Click on the
**Create Student Task**button at the top-right of the campaign. - You will be prompted to enter information regarding the task (as shown below). Fill out the details of the task – a ‘due date’ is not required, but you may enter one by moving the toggle switch to “Yes.”
- Once you’ve finished entering the information for the task, click
**Submit** - Click
**Finish**to end the process. - For each student in the list, a single task should be created on the Advisee Record and assigned to the student for completion

## Send Appointment Campaign

First, create a Campaign as described above, then you can follow these steps to send or re-send an Appointment Campaign to the students

- Navigate to the
**Campaigns**object in the Student Success Hub. - Locate and select the desired Campaign you’ve created and populated.
- At the top-right of the screen, click
**Schedule Campaign**. - Click
**Finish**to complete the process.

- Within one hour, this will send the campaign message to all students in the campaign and mark them as ‘sent’

- When a student books an appointment with you based on this campaign, the student’s Member Status will be updated from “Sent” to “Complete.”
**Note**: you can monitor the status of the campaign by viewing the pie chart on the Campaign (the darker portion shows the number of students with “Complete” status and the lighter portion shows the number of students with “Sent” status)

- If you want to send another note or reminder to those students who have not booked an appointment with you, click the
**Appointment Campaign**button again and craft a follow-up or new message to them. The action will only send emails to those in the Campaign Membership who have a Status that is NOT equal to “Complete”

## Clone a Campaign

You may need to clone a campaign to launch a new appointment campaign to the same list of students with new dates.

- Navigate to the
**Campaigns**object in the Student Success Hub - Locate and select the desired Campaign you’ve created and populated
- At the top-right of the screen, click
**Clone Campaign and Members** - On the left, select
**CampaignMember** - On the bottom, click
**Copy Selected Objects** - At the top of the screen, click
**Edit** - Rename the campaign name
- Note: Leave the first term & username (ex: F22_jsmith_)
- Select new start and end dates
- Click
**Save** - Reset the contact status
- On the right, under Campaign Members, click
**View All** - Select all
- On the upper right, click
**Update Status** - Select
**Not Sent** - Click
**Save**