Welcome to your repo for COM2027, Group 4!
=====================================================

Feel free to change this README.

Getting started
---------------

Before you get started, you should update your com2027.yml file with your team members and project details. This will appear at [your static site](https://csee.pages.surrey.ac.uk/com2027/2023-24/Group4).

You have two branches created for you, `trunk` and `release`. The final commit on `release` will be marked.

Commits must be merged into `release` using a merge request, which requires two approvals. Force-pushing is disabled for both branches, as this can destroy your work. Only `trunk` can be merged into `release`.

You may develop directly on `trunk`, although it is recommended that you branch from `trunk` and submit merge requests (or merge directly onto the branch). How you use `trunk` is up to your team.

## INSTRUCTIONS:

## How to run the project with Docker Desktop manually

1) Download Docker Desktop and create account and sign in. 
2) Clone this repository
3) Go to Group4 folder (optionally in a virtual environment)
4) Run command `docker compose up --build`
5) Go to the "Containers" section on Docker Descktop and when the container is shown running similar to what is shown in the screenshot then click the port 8000:8000.
![Screenshot of port](https://gitlab.surrey.ac.uk/csee/com2027/2023-24/Group4/-/blob/trunk/docker-container-port.png?ref_type=heads)
6) You should then see the website in action.

## How to run project without Docker using git in terminal 
1) Clone repo 
2) navigate to `Group4` folder 
3) start virtual environment using `virtualenv` python package and then do `pip install -r requirements.txt`
4) navigate to `bookproject/` and do `python manage.py makemigrations`
6) Then `python manage.py migrate`
7) `python manage.py seed`
8) Lastly, `python manage.py runserver`


## NOTES:
- To use, search for a book (avoid books with pages = 0 as very rare case but do occur, if happens just remove book from "My Library")
- Add book to library, you can then input pages read and you will see XP / progress update
- You can read book (Read book button) , send notes to email **if you sign up with personal email address** and check email to receive notes.
- You can view XP in View Profile
- You can change profile (avatar/bio etc.)
- You can access leaderboards
- You can comment on forums on categories of books (superuser can only create categories/new forum) - **some random forums seeded for display** and this works real time


