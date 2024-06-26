import random
import string
import argparse
import os
from sqlalchemy import create_engine, Column, Integer, String, Text
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from faker import Faker


# Define the User class
Base = declarative_base()
fake = Faker()
basedir = os.path.abspath(os.path.dirname(__file__))

class User(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True)
    username = Column(String(80), unique=True, nullable=False)
    email = Column(String(120), unique=True, nullable=False)
    title = Column(String(100), nullable=False)
    bio = Column(Text, nullable=False)
    avatar = Column(String(255), nullable=True)
    
    def __repr__(self):
        return f'<User {self.username}>'

# Create a SQLite database connection
engine = create_engine('sqlite:///' + os.path.join(basedir, 'app.db'), echo=True)
Base.metadata.create_all(engine)

Session = sessionmaker(bind=engine)
session = Session()

# List of possible job titles
job_titles = [
    'Software Developer', 'Data Scientist', 'Project Manager', 
    'Graphic Designer', 'Marketing Manager', 'Product Manager', 
    'Sales Representative', 'Customer Support Specialist', 
    'HR Specialist', 'Business Analyst', 'Operations Manager', 
    'Accountant', 'Financial Analyst', 'Research Scientist', 
    'Technical Writer', 'Network Engineer', 'System Administrator', 
    'UX Designer', 'Content Strategist', 'Quality Assurance Engineer'
]

# Function to generate a random username
def generate_username():
    return fake.name()

# Function to generate a random email
def generate_email():
    return fake.email()

def generate_job_title():
    return random.choice(job_titles)

def generate_bio():
    # Generate a paragraph of random text and repeat until desired length is achieved
    paragraphs = [fake.paragraph(nb_sentences=8) for _ in range(50)]
    bio_text = ' '.join(paragraphs)
    words = bio_text.split()
    # Trim to be between 300 to 800 words
    bio_length = random.randint(300, 800)
    return ' '.join(words[:bio_length])

def generate_avatar():
    return fake.image_url()

# Function to clear the database
def clear_database():
    session.query(User).delete()
    session.commit()
    print("Database cleared.")

# Argument parsing
parser = argparse.ArgumentParser(description="Insert or clear users in the database.")
parser.add_argument('--clear', action='store_true', help='Clear all users from the database.')
args = parser.parse_args()

# Clear the database if --clear argument is provided
if args.clear:
    clear_database()

else:
# Generate and insert 50 users
    for _ in range(50):
        username = generate_username()
        email = generate_email()
        jobTitle = generate_job_title()
        bio = generate_bio()
        avatar = generate_avatar()
        user = User(username=username, email=email, title=jobTitle, bio=bio, avatar=avatar)
        session.add(user)

    # Commit the transaction
    session.commit()

    # Close the session
    session.close()

    print("Inserted 50 users into the database.")