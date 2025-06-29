import requests
from bs4 import BeautifulSoup
import csv
import tkinter as tk
from tkinter import messagebox, filedialog

# Function to scrape product data
def scrape_books():
    base_url = "http://books.toscrape.com/catalogue/page-{}.html"
    books = []

    for page in range(1, 6):  # Scrape first 5 pages
        url = base_url.format(page)
        response = requests.get(url)
        soup = BeautifulSoup(response.content, 'html.parser')
        articles = soup.find_all('article', class_='product_pod')

        for article in articles:
            title = article.h3.a['title']
            price = article.find('p', class_='price_color').text.strip()
            rating = article.p['class'][1]
            books.append({'Title': title, 'Price': price, 'Rating': rating})

    return books

# Function to save to CSV
def save_to_csv(data):
    file_path = filedialog.asksaveasfilename(defaultextension='.csv', filetypes=[("CSV files", "*.csv")])
    if file_path:
        with open(file_path, 'w', newline='', encoding='utf-8') as f:
            writer = csv.DictWriter(f, fieldnames=['Title', 'Price', 'Rating'])
            writer.writeheader()
            writer.writerows(data)
        messagebox.showinfo("Success", f"Data saved to {file_path}")

# GUI functions
def run_scraper():
    messagebox.showinfo("Scraping", "Scraping data... Please wait.")
    data = scrape_books()
    save_to_csv(data)

# UI Setup
root = tk.Tk()
root.title("Book Scraper")
root.geometry("300x150")

label = tk.Label(root, text="Scrape product info from books.toscrape.com", wraplength=250)
label.pack(pady=10)

scrape_button = tk.Button(root, text="Start Scraping", command=run_scraper)
scrape_button.pack(pady=10)

root.mainloop()