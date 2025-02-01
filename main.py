import streamlit as st  # Required for building the web app
import requests  # Required for making HTTP requests to fetch web pages
from bs4 import BeautifulSoup  # Required for parsing HTML content
import pandas as pd  # Required for handling data and saving it as CSV
from io import BytesIO  # Required for downloading the CSV file

# Streamlit UI
st.title("Web Scraper for E-commerce Websites")
st.write("### Welcome to E-commerce Web Scraper")
st.write("### HI! Please choose any category from the Web Scraper test website to gather data. This tool helps you learn more about automation for any website! 🚀")

# User input for URL
url = st.text_input("Enter the URL of the webpage to scrape")

if st.button("Scrape Data"):
    try:
        r = requests.get(url)  # Make a GET request to fetch the webpage content
        soup = BeautifulSoup(r.text, "lxml")  # Parse the webpage content using BeautifulSoup

        # Extract names of products
        product_names = [i.text for i in soup.find_all('a', class_="title")]
        
        # Extract product prices
        prices = [i.text for i in soup.find_all("h4", class_="price float-end card-title pull-right")]
        
        # Extract product ratings
        ratings = [i.text for i in soup.find_all("p", class_="review-count float-end")]

        # Create a DataFrame using the extracted data
        df = pd.DataFrame({"Names": product_names, "Prices": prices, "Ratings": ratings})
        
        # Display the data in a table
        st.write("### Extracted Data")
        st.dataframe(df)
        
        # Convert DataFrame to CSV in-memory
        csv_buffer = BytesIO()
        df.to_csv(csv_buffer, index=False)
        csv_buffer.seek(0)
        
        # Download button for CSV file
        st.download_button(
            label="Download CSV File",
            data=csv_buffer,
            file_name="product_details.csv",
            mime="text/csv"
        )
    except Exception as e:
        st.error(f"An error occurred: {e}")
