# IAB207 Rapid Web Development

IAB207 Rapid Web Development - Semester 2 - 2019 - QUT

Create a functioning frontend and backend for a marketplace selling items of our choosings.

Here we have a marketplace *My Tunes* for buying and selling music. Users can create unique login details to start selling their items and buying from others on the marketplace.

*My Tunes* does not integrate any form of payment - this is designed to be left up to the seller and buyer through either phone or email. The buyer can then select a user they wish the sell the item to and the item will be made no longer available to bid on.

### Notable Features
- All input fields are sanitized through the use of custom made flask_wtforms field classes
- All passwords are hashed and stored as a hashkey in the database
- Working search fields which are populated from the available data in the database
 
### Enhancements / Todo
- Current images are stored in local static folder - will need to migrate to file host so that images can be saved and served on heroku deployment
  - Would also like the be able to fomat the images on save - potentially using tinypng api
- Create an admin dashboard to see all users and listings
- Create development and live environments for increased ease of heroku builds
- Set up tests and use Travis CI for build checking before deployments
- Add ability to set the desired bid price rather than it being set to the desired sell price
- Setup whole project to be a boilerplate marketplace for future projects
  
### Technologies
- Python
- Flask
- SQL
- HTML
- CSS
- Bootstrap 4

## Installation

Use the package manager [pip](https://pip.pypa.io/en/stable/) to install all dependencies.

Navigate to /IAB207-ASS.3 (containing *requirements.txt*) and run:

```bash
pip install -r requirements.txt
```

## Creating SQLite Database
To initialise DB, navigate to /IAB207-ASS.3 (contaning *reinit.py*) and run:
```bash
python reinitby.py
```

## Running Application
Navigate to folder containing *app.py*
```bash
flask run
```

## Collaborators
This is a group QUT project collaborated on by 3 members:

 - [Jack Stanyon](https://github.com/stanyonja/) - Styling fixes
 - [Liam Wrigley](https://github.com/liamwrigley/) - Backend / DB / Design / Styling
 - [Quoi McGowan](https://github.com/quoim) - Styling Fixes


## License
[MIT](https://choosealicense.com/licenses/mit/)
