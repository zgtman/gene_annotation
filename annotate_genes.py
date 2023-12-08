import csv
import xlsxwriter

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

if __name__ == "__main__":
    input_file_path = "genes.txt"
    gene_info_file_path = "/Users/broz/Documents/python/anotace_genes/gene_info.csv"  # Replace with the actual path
    output_file_path = "genes_annotated.xlsx"

    enrich_input_file(input_file_path, gene_info_file_path, output_file_path)






    # gene_info_file_path = "/Users/broz/Documents/python/anotace_genes/gene_info.csv"  # Replace with the actual path


