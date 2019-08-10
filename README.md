# Reference Project

Hello Students,

This is a project that I have made for you to reference. This project contains some extra stuff that has not been covered in class yet, but I have left comments explaining what the code does in detail. This project is a more advanced version of the todo list that we have done.

The following project includes:-

1. User Authentication
2. Post Creation
3. Error Validation
4. Admin Panel
5. Authenticated Page

This app, while it does have some frontend styling, is only used for position the elements, the main focus here is writing the python code.
I've used flexbox to position the elements.

If you're interested in understanding the CSS of this project then please do this
exercise [Flexbox Froggy](https://flexboxfroggy.com/)

It should take you at max 30 mintues to understand how flexbox works using this exercise.

## Running the project

Create a virtual environment and activate it

```python
virtualenv reference_project
source reference_project/Scripts/activate
```

You've learn't that you can install packages using the pip command. However in the case of having to install multiple packages at once, you can run the following command.

```python
pip install -r requirements.txt
```

This commands installs all the packages put in the requirements.txt

To create your own requirements.txt for your own packages then use

```python
pip freeze > requirements.txt
```

Note: Only do pip freeze inside a virtual environments. If you use it with the global python install. It will list all the packages that installed globally.

Once everything is installed run mysql using XAMPP and connect to the database. I have used the database 'todo' in this project
Create the tables using this sql code

```sql
create table user(
    id int primary key auto_increment,
    name varchar(20),
    hash varchar(40),
    isAdmin boolean
);

```

isAdmin is a boolean to check if the user is an admin or not

```sql
create table post(
    id int primary key auto_increment,
    title varchar(50),
    description varchar(200),
    userId int,
    foreign key (userId) references user(id) on delete cascade
);
```

You may notice there is delete cascade in the foreign key. this is because if you do not use delete cascade and if you try to delete
a record from user that already has a post it will not let you delete is as there are posts that have the foreign key of that user.
so if you add delete cascade when you delete a user, it will delete the user along with all the posts that are associcated with the user.

To understand the source code please start reading the comments from the base.html file

Warning: In the jinja template comments i have given a space between { and %. This is because jinja is trying to render it as a syntax and doesn't see it as a comment. Make sure there is no space in the code.
