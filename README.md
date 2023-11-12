# MadHacks2023

## Inspiration
We went into this project hoping to streamline the enrollment process for UW Madison students. Specifically by allowing students to take classes together easier, and to know what classes they can and have to take.

## What it does
Badger CourseMate offers users the opportunity to more easily choose classes required for their major, and take classes with their friends. It does this by looking at a user's DARS report and highlighting classes depending on if they can take the class, and whether it is required for their major. Badger CourseMate also allows for users to be friends, friends can see what classes and sections their friends have in their carts and can more easily coordinate taking classes together.
 
## How we built it
Badger CourseMate uses an extension that should web scrape the users DARS and Cart with the press of a button, this is then stored in a mongoDB server. This server stores user's login information, friend status's, schedules, and DARS reports. Badge CourseMate also has a website where users can sign up, log in, friend each other and see what classes their friends are taking.

## Challenges we ran into
Chrome extensions are unfamiliar grounds for our team, and presented some complications. Specifically figuring out a way to connect our website to the extension, and for the extension to scrape the webpage. We also tangled with the security features of Chrome Extensions as they blocked our backend from connecting to the extension.

## Accomplishments that we're proud of
Though extensions were a significant hurdle, we made large amounts of progress despite the short time.

## What we learned
We learned how to implement MongoDB, Flask, Chrome Extensions, and Web Scraping into a single app.

## What's next for Badger CourseMate
Badger CourseMate currently only works with CS major classes, next we will expand the system to include every course and major offered by UW Madison. In addition, we will make the application more secure, and make sure the extension can connect to the backend.
