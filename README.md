# PR5 Booking

A booking system for the Jamming Studio PR5.

## Motivation

I decided to build something that could potentially have a practical application in my daily life.
PR5 (Practice Room 5) is the jamming studio in my College, and due to historical reasons, the booking is not managed
by the centralised College booking system, but by a committee of students.
Currently, there is no booking system set up for the room, and the committee uses a mixture of Google Forms,
Spreadsheets and Calendar to manage requests for booking from students.
This is time-consuming for the committee, and the user experience for students is not great.

## Project Description

PR5 Booking is a website where students can book the jamming studio (PR5) in my College,
and administrators can approve/reject the booking requests. Here are the available features:

* Public / User / Administrator Access Levels
* Information about PR5 and the website (_public_)
* Calendar displaying confirmed and pending bookings (JavaScript integration using [FullCalendar](https://fullcalendar.io/)) (_public_)
  * Users can drag and select timings to book a slot (_user_)
* Make a booking (making use of Django's ModelForms) (_user_)
* Dashboard to view upcoming bookings at a glance (_user_)
* View my bookings (categorised as upcoming/pending/rejected/past) (_user_)
* Approve booking requests from users (_admin_)
* Profile page to view booking statistics (_user_)
  * View profiles of users to see their booking statistics and history (_admin_)
* Login functionality (with password change and reset) (_user_)
* Email notifications (whenever a booking gets approved/rejected by an admin) (_user_)

This project is clearly distinctive from other projects as we have not worked on any booking-related functionality before.
This project is also sufficiently complex, 
The web application uses three models in Django (User, Booking, and Approval) spread across two apps (users and bookings).
I implemented the frontend with support from the Bootstrap framework, with mobile-responsiveness in mind.
In addition, JavaScript was used to enable Bootstrap modals, as well as to integrate the calendar functionality with my website.

## Web Pages

### Home

Nothing interesting here, just information about PR5 and how to get an account to be able to book the room.

### Dashboard

The dashboard contains information about upcoming bookings. There are 3 panels, which display the number of 1) approved upcoming bookings, 2) pending bookings, and 3) rejected bookings.

Additionally, it presents the user with the 3 next upcoming bookings, as well as a button to view all upcoming bookings.

For admins, there is an additional panel that states the number of bookings that require approval.

### Calendar

Makes use of the [FullCalendar](https://fullcalendar.io) library to implement a selectable calendar similar to Google Calendar.

For non-users, they will be able to see upcoming confirmed and pending bookings on the calendar, but will not be able to select timeslots and book.
Users are allowed to bring friends into the room for jamming.
Therefore, this web page allows friends of users to be able to verify that the booking timing, without needing an account.

For users, in addition to the above functionality, they will be able to drag and select a timeslot to make a booking.
Users are not allowed to select timeslots that conflict with existing events. This is implemented via a FullCalendar setting.
Upon selecting a valid timeslot, the user is prompted for confirmation via a Bootstrap modal
(that displays the selected date and timings) and then redirected to the booking page, with the dates and timeslots already filled in (passed as GET parameters).
This allows for easy booking, as it is pretty much similar to creating an event on Google Calendar.
Users can only select timeslots that start and end on the same day, because I do not want users to be able to book across different days.

Pending bookings are displayed on the calendar as well so that there will not be a situation where there are multiple conflicting booking requests waiting for approval.
This ensures a more seamless booking experience which will not be affected by any potential delays between when the booking is made and when the administrator sees it and approves it.
Only if the administrator rejects the booking, will the slot be freed up for other users to book.

### Make a Booking

This page is not accessible via the navbar (although it is accessible via the url), as it is better for the user to select the booking by checking the calendar for conflicting timeslots.
In addition, the booking date and timings are pre-filled after the user selects a timeslot from the calendar.

The form is implemented via the ModelForm for the Booking model, and asks the user for additional details for the booking.
Validation is implemented to check that the user correctly filled up the form (e.g. filled up at least one equipment, booking does not clash with another timeslot)

I designed the Booking model such that there is no start and end date - there is only one booking date, and there is a start and end time.
This physically prevents the user from selecting a timeslot that spans multiple days.

### My Bookings

This page displays the user's bookings grouped by the following categories:

* **Upcoming Bookings**
  
  These are upcoming bookings that have been approved. Users can delete upcoming bookings via a popup Bootstrap modal form.
  Once the date and time passes, the booking will be considered a past booking instead.
  The bookings are sorted in ascending order of the date of the booking, so that users can see the next upcoming booking first.

* **Pending Bookings**
  
  These are bookings for future dates that have not yet been approved or rejected.
  If a booking lapses (the timeslot passes) without any approval/rejection,
  it will no longer be considered a pending booking, and will be a past booking.
  Users can delete pending bookings via a popup Bootstrap modal form.
  The bookings are sorted in ascending order of the date of the booking.

* **Rejected Bookings**
  
  These are bookings for future dates that have been rejected. Users cannot delete such bookings.
  Once the date and time passes, the booking will be considered a past booking instead.
  I designed it this way as I believe that the user is mainly interested in bookings that are for future dates, so bookings that are in the past, can be lumped together under "Past Bookings".
  The bookings are sorted in ascending order of the date of the booking.

* **Past Bookings**
  
  These are all bookings for past dates, no matter whether they have been approved or rejected or neither.
  They can be distinguished as the booking will state whether it was approved or rejected (or if neither, there will be no text for approval/rejection).
  Users cannot delete such bookings.
  The bookings are sorted in ascending order of the date of the booking, so that users can see the most recent past booking first.

### All Bookings

Only administrators can access this page. It displays all user bookings grouped by the following categories:

* **Unapproved Bookings**
  
  These are upcoming bookings that are pending. Administrators can select to approve or reject the bookings via a popup Bootstrap modal form.
  Once the date and time passes without any approval/rejection, the booking will be considered a past booking instead.
  When approving/rejecting, the administrator can add 1) comments to be displayed to the user (e.g. reason for rejection),
  and 2) comments to be displayed to other administrators (e.g. notes on why approval/rejection was granted).
  The bookings are sorted in ascending order of the date of the booking, so that administrators can see the next upcoming booking first.

* **Approved Bookings**
  
  These are upcoming bookings that have been approved. Administrators can choose to reject an already approved booking via a popup Bootstrap modal form.
  Once the date and time passes, the booking will be considered a past booking instead.
  The bookings are sorted in ascending order of the date of the booking.

* **Rejected Bookings**
  
  These are bookings for future dates that have been rejected. Administrators can choose to approve an already rejected booking via a popup Bootstrap modal form.
  Once the date and time passes, the booking will be considered a past booking instead.
  The bookings are sorted in ascending order of the date of the booking.

* **Past Bookings**
  
  These are all bookings for past dates, no matter whether they have been approved or rejected or neither.
  They can be distinguished as the booking will state whether it was approved or rejected (or if neither, there will be no text for approval/rejection).
  The bookings are sorted in ascending order of the date of the booking, so that administrators can see the most recent past booking first.
  
### My Profile

Users can view their own profile, which contains statistics about their past bookings.

### Other Users' Profiles

Administrators can view other users' profiles by clicking on their name on the "All Bookings" page (the name of the user requesting the booking will be displayed as a hyperlink to their profile).
Their profiles contain statistics about past bookings, as well as a history of their bookings, sorted in descending order of the date of the booking.

### Change Password

Users can change their password, implemented via the built-in Django Change Password Form and View.

### Create Account

Superusers can access this page to create a new user account. This is more restrictive to prevent administrators from creating accounts as they wish.
This page is intended to be used in person - the new user will need to undergo a workshop to be familiarised with the room,
and the superuser will then ask them to fill up the form on the spot (the navbars of this page are hidden for this reason so that the new user cannot click to go elsewhere).
Upon submission, the new user will receive an email that contains a link to set their password.
This was designed this way so that superusers can also create accounts on behalf of new users without them being in-person, if ever required.

## Files

* [bookings](./bookings)
  * [templates](./bookings/templates)
    * [bookings](./bookings/templates/bookings)
      * [all_bookings](./bookings/templates/bookings/all_bookings)
        
        Contains the HTML templates for the pages that display all booking requests to the administrators for approval/rejection ("All Bookings").
      * [booking_reviewed](./bookings/templates/bookings/booking_reviewed)
        
        Contains the templates for the email that is sent when a booking is approved/rejected.
      * [user_bookings](./bookings/templates/bookings/user_bookings)
        
        Contains the HTML templates for the pages that display the user's bookings to them ("My Bookings").
      * [bookings_layout.html](./bookings/templates/bookings/bookings_layout.html)
        
        Template that implements the layout of bookings being presented to the user.
        Contains Bootstrap modals that allow the user to delete the booking (only allowed when booking is approved or pending)
        as well administrators to approve/reject the booking.
      * [calendar.html](./bookings/templates/bookings/calendar.html)
        
        Template for the "Calendar" page. Makes use of the [FullCalendar](https://fullcalendar.io) library to implement a selectable calendar.
        The booking data is fed into the Calendar object via an API route (see [views.py](./bookings/views.py)).
      * [dashboard.html](./bookings/templates/bookings/dashboard.html)
        
        Template for the "Dashboard" page.
      * [make_booking.html](./bookings/templates/bookings/make_booking.html)
    
        Template for the "Make a Booking" page. Makes use of the ModelForm as in [forms.py](./bookings/forms.py).
  * [models.py](./bookings/models.py)
    
    Contains the Booking model and Approval model.
  * [forms.py](./bookings/forms.py)
    
    Contains the forms for creating a Booking/Approval instance. These forms are used in the templates above.
  * [views.py](./bookings/views.py)
  
    Contains the many views that are present for the booking portion of the website (e.g. make booking, view bookings, dashboard, etc.).
* [static](./static)
  * [fullcalendar](./static/fullcalendar)
    
    Folder containing the FullCalendar library, taken from [this website](https://fullcalendar.io/docs/getting-started).
  * [favicon.png](./static/favicon.png)
    
    Favicon I created for the website.
  * [pr5_room.jpg](./static/pr5_room.jpg)
    
    Image of PR5 taken from [this website](https://arts.yale-nus.edu.sg/band-room/).
  * [styles.css](./static/styles.css)
    
    Additional CSS styling.
* [templates](./templates) (Templates)
  * [base.html](./templates/base.html)
    
    Base template that all other templates inherit from. Contains HTML for navbar.
  * [form-group.html](./templates/form-group.html)
    
    Template for creating Bootstrap form groups, which can be easily re-used by other pages that require forms.
    Extends on Django's default ModelForm and provides Boostrap styling for form errors etc.
  * [home.html](./templates/home.html)
    
    Home page template.
* [users](./users)
  
  Contains the custom user model and forms, as well as the profile and create account views. Some code adapted from the Django package codebase (`django.contrib.auth`).
  * [templates](./users/templates)
    
    Contains templates for all the account related functions - Login, Create Account, Password Change, Password Reset. Some code adapted from the Django package codebase (`django.contrib.admin.templates`).
    Also contains templates for the profile pages.
  * [templatetags](./users/templatetags)
    * [form_extras.py](./users/templatetags/form_extras.py)
      
      Contains useful template tags to be used for form inputs.

## Usage

For the purposes of submission, the Email Backend has been changed to the console so that setting up SMTP is not necessary.
This means that emails will be displayed in the console instead.

1. Download the distribution code
2. In your terminal, cd into the pr5-booking directory.
3. Run `python manage.py makemigrations` bookings to make migrations for the bookings app. 
4. Run `python manage.py makemigrations` users to make migrations for the users app.
5. Run `python manage.py migrate` to apply migrations to your database.
6. Run `python manage.py createsuperuser` to create a superuser.
7. Run `python manage.py runserver` to begin the website.
8. Login as superuser and create a user account via `[domain]/accounts/create/` (or accessible by logging in > Profile > Create Account). 
   The password set link is normally sent via email, but in this case will be displayed in the console.
9. You now have a user account and admin account to test with.

## Notes

For the screen recording, I decided to use the SMTP Email Backend so that the email functionality can be demonstrated.
This differs from the distribution code here.