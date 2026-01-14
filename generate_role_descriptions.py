import json
import os

def generate_role_descriptions(roles_data):
    for role in roles_data:
        # Sanitize title for filename
        filename = f"{role['title'].replace(' ', '-').replace('/', '-').lower()}.md"
        filepath = os.path.join(os.getcwd(), filename) # Save in current directory

        org_level = ", ".join(role['orgLevel']) if isinstance(role['orgLevel'], list) else role['orgLevel']
        medium = ", ".join(role['medium'])
        industry = ", ".join(role['industry'])
        responsibilities = "\n".join([f"- {resp}" for resp in role['responsibilities']])
        skills = "\n".join([f"- {skill}" for skill in role['skills']])

        markdown_content = f"""# {role['title']}

## Description
{role['description']}

## Org Level
{org_level}

## Medium
{medium}

## Industry
{industry}

## Responsibilities
{responsibilities}

## Skills
{skills}
"""
        with open(filepath, 'w') as f:
            f.write(markdown_content)
        print(f"Created {filename}")

# Load the roles.json data
roles_json_path = "/Users/jens.wedin/Documents/Visual Studio/generate-role-descriptions/roles.json"
with open(roles_json_path, 'r') as f:
    roles = json.load(f)

# Generate the markdown files
generate_role_descriptions(roles)
