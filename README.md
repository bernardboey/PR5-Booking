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

* Public / Member / Administrator Access Levels
* Information about PR5 and the website (_public_)
* Calendar displaying confirmed and pending bookings (JavaScript integration using [FullCalendar](https://fullcalendar.io/)) (_public_)
  * Members can drag and select timings to book a slot (_member_)
* Make a booking (making use of Django's ModelForms) (_member_)
* Dashboard to view upcoming bookings at a glance (_member_)
* View my bookings (categorised as upcoming/pending/rejected/past) (_member_)
* Approve booking requests from members (_admin_)
* Profile page to view booking statistics (_member_)
  * View profiles of members to see their booking statistics and history (_admin_)
* Login functionality (with password change and reset) (_member_)
* Email notifications (whenever a booking gets approved/rejected by an admin) (_member_)

This project is clearly distinctive from other projects as we have not worked on any booking-related functionality before.
This project is also sufficiently complex, 
The web application uses three models in Django (User, Booking, and Approval) spread across two apps (users and bookings).
I implemented the frontend with support from the Bootstrap framework, with mobile-responsiveness in mind.
In addition, JavaScript was used to enable Bootstrap modals, as well as to integrate the calendar functionality with my website.

## Files



## Usage

For the purposes of submission, the Email Backend has been changed to the console so that setting up SMTP is not necessary.
This means that emails will be displayed in the console instead.

1. Download the distribution code
2. In your terminal, cd into the pr5-booking directory.
3. Run python manage.py makemigrations bookings to make migrations for the bookings app. 
4. Run python manage.py makemigrations users to make migrations for the users app.
5. Run python manage.py migrate to apply migrations to your database.
6. Run python manage.py runserver to begin the website.
7. Login as superuser and create a member account via `[domain]/accounts/create/`. 
   The password set link will be sent via email (but in this case displayed in the console)
8. You now have a member account and admin account to test with.