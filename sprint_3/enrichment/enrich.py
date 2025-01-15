import pandas as pd
import numpy as np
from sqlalchemy import create_engine, Column, Integer, String, Float
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import logging
from typing import List, Dict
import os
from dotenv import load_dotenv
import random

# Load environment variables
load_dotenv()

# Set up logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# Set up database connection
DB_USER = os.getenv('DB_USER', 'postgres')
DB_PASSWORD = os.getenv('DB_PASSWORD', 'postgres')
DB_HOST = os.getenv('DB_HOST', 'localhost')
DB_PORT = os.getenv('DB_PORT', '5432')
DB_NAME = os.getenv('DB_NAME', 'preproddb')

DATABASE_URL = f"postgresql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"

# Set up SQLAlchemy
Base = declarative_base()
engine = create_engine(DATABASE_URL)
Session = sessionmaker(bind=engine)

class Student(Base):
    __tablename__ = 'students'
    
    id = Column(Integer, primary_key=True)
    name = Column(String)
    age = Column(Integer)
    gender = Column(String)
    major = Column(String)
    gpa = Column(Float)

def create_tables():
    """Create tables in the PostgreSQL database"""
    Base.metadata.create_all(engine)
    logging.info("Database tables created (if they didn't exist already).")

def populate_sample_data():
    """Populate the students table with sample data"""
    session = Session()

    # Check if the table is already populated
    if session.query(Student).first():
        logging.info("Table already contains data. Skipping sample data population.")
        session.close()
        return

    # Sample data
    names = ["Alice Smith", "Bob Johnson", "Charlie Brown", "Diana Ross", "Ethan Hunt", 
             "Fiona Apple", "George Michael", "Hannah Montana", "Ian McKellen", "Julia Roberts"]
    majors = ["Computer Science", "Engineering", "Physics", "Mathematics", "Chemistry", 
              "Biology", "Psychology", "Economics", "History"]

    # Generate sample students
    sample_students = []
    for i in range(50):  # Generate 50 sample students
        student = Student(
            name=random.choice(names),
            age=random.randint(18, 25),
            gender=random.choice(["Male", "Female"]),
            major=random.choice(majors),
            gpa=round(random.uniform(2.0, 4.0), 2)
        )
        sample_students.append(student)

    # Add sample data to the database
    session.add_all(sample_students)
    session.commit()
    session.close()

    logging.info("Sample data populated successfully.")

def load_data() -> pd.DataFrame:
    """Load data from PostgreSQL database."""
    try:
        with engine.connect() as connection:
            df = pd.read_sql_table('students', connection)
        logging.info(f"Data loaded successfully. Shape: {df.shape}")
        return df
    except Exception as e:
        logging.error(f"Error loading data: {str(e)}")
        raise

def validate_data(df: pd.DataFrame) -> pd.DataFrame:
    """Validate and clean the data."""
    # Remove rows with missing values
    df.dropna(inplace=True)
    
    # Ensure age is within a reasonable range
    df = df[(df['age'] >= 17) & (df['age'] <= 30)]
    
    # Ensure GPA is within valid range
    df = df[(df['gpa'] >= 0) & (df['gpa'] <= 4.0)]
    
    logging.info("Data validation completed.")
    return df

def transform_data(df: pd.DataFrame) -> pd.DataFrame:
    """Transform the data."""
    # Calculate age group
    df['age_group'] = pd.cut(df['age'], bins=[0, 20, 22, 25, 30], labels=['18-20', '21-22', '23-25', '26-30'])
    
    # Calculate GPA category
    df['gpa_category'] = pd.cut(df['gpa'], bins=[0, 2.0, 3.0, 3.5, 4.0], 
                                labels=['Poor', 'Average', 'Good', 'Excellent'])
    
    # Create a numeric encoding for gender
    df['gender_code'] = df['gender'].map({'Male': 0, 'Female': 1})
    
    logging.info("Data transformation completed.")
    return df

def enrich_data(df: pd.DataFrame) -> pd.DataFrame:
    """Enrich the data with additional information."""
    # Add department information
    department_map = {
        'Computer Science': 'School of Computing',
        'Engineering': 'School of Engineering',
        'Physics': 'School of Sciences',
        'Mathematics': 'School of Sciences',
        'Chemistry': 'School of Sciences',
        'Biology': 'School of Sciences',
        'Psychology': 'School of Social Sciences',
        'Economics': 'School of Business',
        'History': 'School of Humanities'
    }
    df['department'] = df['major'].map(department_map)
    
    # Add estimated starting salary (fictional data)
    salary_map = {
        'Computer Science': 75000,
        'Engineering': 70000,
        'Physics': 65000,
        'Mathematics': 62000,
        'Chemistry': 63000,
        'Biology': 61000,
        'Psychology': 55000,
        'Economics': 68000,
        'History': 52000
    }
    df['estimated_salary'] = df['major'].map(salary_map)
    
    logging.info("Data enrichment completed.")
    return df

def save_data(df: pd.DataFrame) -> None:
    """Save processed data back to the database."""
    try:
        with engine.connect() as connection:
            df.to_sql('processed_students', connection, if_exists='replace', index=False)
        logging.info("Processed data saved to database.")
    except Exception as e:
        logging.error(f"Error saving data: {str(e)}")
        raise

def main():
    try:
        # Ensure tables exist
        create_tables()
        
        # Populate sample data if the table is empty
        populate_sample_data()
        
        # Load data
        df = load_data()
        
        if df.empty:
            logging.warning("No data found in the database after population attempt. Please check your database connection and permissions.")
            return
        
        # Process data
        df = validate_data(df)
        df = transform_data(df)
        df = enrich_data(df)
        
        # Save processed data
        save_data(df)
        
        # Print summary statistics
        print(df.describe())
        print("\nSample of processed data:")
        print(df.head())
        
    except Exception as e:
        logging.error(f"An error occurred: {str(e)}")

if __name__ == "__main__":
    main()