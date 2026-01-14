import os
import re
import csv
import logging

# Configure logging
logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s - %(levelname)s - %(message)s',
                    handlers=[
                        logging.FileHandler("conversion.log"),
                        logging.StreamHandler()
                    ])

def convert_markdown_to_csv(roles_dir, output_csv):
    logging.info(f"Starting markdown to CSV conversion from directory: {roles_dir}")
    
    all_headings = set()
    role_data = []

    # First pass to collect all unique headings
    for filename in os.listdir(roles_dir):
        if filename.endswith(".md"):
            filepath = os.path.join(roles_dir, filename)
            try:
                with open(filepath, 'r', encoding='utf-8') as f:
                    content = f.read()
                    headings = re.findall(r"##\s*(.*)", content)
                    for heading in headings:
                        all_headings.add(heading.strip())
            except Exception as e:
                logging.error(f"Error reading or parsing headings from {filepath}: {e}")

    sorted_headings = sorted(list(all_headings))
    csv_headers = ['Role Name'] + sorted_headings

    # Second pass to extract data for each role
    for filename in os.listdir(roles_dir):
        if filename.endswith(".md"):
            filepath = os.path.join(roles_dir, filename)
            role_name = os.path.splitext(filename)[0].replace('-', ' ').title()
            current_role_data = {'Role Name': role_name}
            
            # Initialize all heading columns for the current role
            for heading in sorted_headings:
                current_role_data[heading] = ''

            try:
                with open(filepath, 'r', encoding='utf-8') as f:
                    content = f.read()
                    
                    # Split content by '##' headings
                    parts = re.split(r"(##\s*.*)", content)
                    
                    current_heading = None
                    for part in parts:
                        if part.startswith("##"):
                            current_heading = part.replace("##", "").strip()
                        elif current_heading and current_heading in sorted_headings:
                            current_role_data[current_heading] += part.strip() + "\n"
                            
                role_data.append(current_role_data)
                logging.info(f"Successfully processed role: {role_name} from {filepath}")

            except Exception as e:
                logging.error(f"Error processing content for {role_name} from {filepath}: {e}")
    
    # Write to CSV
    try:
        with open(output_csv, 'w', newline='', encoding='utf-8') as csvfile:
            writer = csv.DictWriter(csvfile, fieldnames=csv_headers)
            writer.writeheader()
            for row in role_data:
                # Ensure all heading keys are present in the row before writing
                for header in sorted_headings:
                    if header not in row:
                        row[header] = ''
                writer.writerow(row)
        logging.info(f"Successfully created CSV file: {output_csv}")
    except Exception as e:
        logging.error(f"Error writing to CSV file {output_csv}: {e}")

if __name__ == "__main__":
    roles_directory = "/Users/jens.wedin/Documents/Visual Studio/generate-role-descriptions/role_descriptions"
    output_csv_file = "/Users/jens.wedin/Documents/Visual Studio/generate-role-descriptions/roles_structured.csv"
    
    convert_markdown_to_csv(roles_directory, output_csv_file)
