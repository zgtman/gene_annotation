#!/usr/bin/env python3

import tkinter as tk
from tkinter import filedialog
import csv
import xlsxwriter
import os
from PIL import Image, ImageTk  # Ensure you have the Pillow library installed

class Tooltip:
    def __init__(self, widget, text):
        self.widget = widget
        self.text = text
        self.tooltip = None
        self.widget.bind("<Enter>", self.display_tooltip)
        self.widget.bind("<Leave>", self.hide_tooltip)

    def display_tooltip(self, event):
        x, y, _, _ = self.widget.bbox("insert")
        x += self.widget.winfo_rootx() + 25
        y += self.widget.winfo_rooty() + 20

        # Create a toplevel window
        self.tooltip = tk.Toplevel(self.widget)
        self.tooltip.wm_overrideredirect(True)
        self.tooltip.wm_geometry(f"+{x}+{y}")

        # Display the tooltip text
        label = tk.Label(self.tooltip, text=self.text, justify='left', background='#ffffe0', relief='solid', borderwidth=1, wraplength=200)
        label.pack(ipadx=1)

    def hide_tooltip(self, _):
        if self.tooltip:
            self.tooltip.destroy()
            self.tooltip = None


def enrich_input_file(input_file_path, gene_info_file_path, output_file_path):
    gene_info = {}

    # Read gene info file and create a dictionary
    with open(gene_info_file_path, 'r') as gene_info_file:
        gene_info_reader = csv.DictReader(gene_info_file)
        for row in gene_info_reader:
            gene_info[row['gene_symbol']] = row

    # Read input file and annotate genes
    with open(input_file_path, 'r') as input_file, xlsxwriter.Workbook(output_file_path) as workbook:
        worksheet = workbook.add_worksheet()

        # Write header row
        header = ["Gene Symbol"] + list(gene_info[list(gene_info.keys())[0]].keys())
        for col_num, header_value in enumerate(header):
            worksheet.write(0, col_num, header_value)

        row_num = 1  # Start from the second row
        for gene_symbol in input_file:
            gene_symbol = gene_symbol.strip()

            if gene_symbol in gene_info:
                gene_data = gene_info[gene_symbol]
                output_row = [gene_symbol] + list(gene_data.values())

                # Write data to Excel
                for col_num, cell_value in enumerate(output_row):
                    worksheet.write(row_num, col_num, cell_value)

                row_num += 1

def select_input_file():
    input_file_path = filedialog.askopenfilename(filetypes=[("Text files", "*.txt")])
    if input_file_path:
        input_file_var.set(input_file_path)

def run_enrichment():
    input_file_path = input_file_var.get()

    # Extract directory from input file path
    input_directory = os.path.dirname(input_file_path)

    gene_info_file_path = "~/repos/gene_annotation/gene_info.csv"  # Replace with the actual path

    # Create the output file path in the same directory as the input file
    output_file_path = os.path.join(input_directory, "output.xlsx")

    enrich_input_file(input_file_path, gene_info_file_path, output_file_path)
    result_label.config(text="Gene enrichment completed. Output saved to output.xlsx in the same directory as the input file.")

# Create the main application window
app = tk.Tk()
app.title("Gene Enrichment Tool")

# Variable to store the input file path
input_file_var = tk.StringVar()

# Create GUI components
input_label = tk.Label(app, text="Select Input File:")
Tooltip(input_label, "Select a text file containing gene names, one per line.")
input_entry = tk.Entry(app, textvariable=input_file_var, state="readonly", width=40)
input_button = tk.Button(app, text="Browse", command=select_input_file)
run_button = tk.Button(app, text="Run Enrichment", command=run_enrichment)
result_label = tk.Label(app, text="")

# Load and display the logo
logo_path = "~/repos/gene_annotation/bioxsys.png"  # Replace with the actual path to your logo 
if os.path.exists(logo_path):
    logo_image = Image.open(logo_path)
    logo_image = logo_image.resize((int(logo_image.width * 0.1), int(logo_image.height * 0.1)))  # Resize to 10%
    logo_photo = ImageTk.PhotoImage(logo_image)
    logo_label = tk.Label(app, image=logo_photo)
    logo_label.image = logo_photo  # Keep a reference to prevent garbage collection
    logo_label.grid(row=0, column=3, padx=10, pady=10, rowspan=2)  # Adjust the row and column as needed

# Arrange GUI components
input_label.grid(row=0, column=0, padx=10, pady=10)
input_entry.grid(row=0, column=1, padx=10, pady=10)
input_button.grid(row=0, column=2, padx=10, pady=10)
run_button.grid(row=1, column=0, columnspan=3, pady=10)
result_label.grid(row=2, column=0, columnspan=3)

# Start the application loop
app.mainloop()
