import json
import os
import re

def find_similar_roles(current_role, all_roles, max_similar=5):
    similar_roles = []
    current_industry = set(current_role['industry'])
    current_medium = set(current_role['medium'])
    current_skills = set(current_role.get('skills', []))

    for role in all_roles:
        if role['id'] == current_role['id']:
            continue

        score = 0
        score += len(current_industry.intersection(set(role['industry']))) * 2
        score += len(current_medium.intersection(set(role['medium'])))
        score += len(current_skills.intersection(set(role.get('skills', [])))) * 3
        
        if current_role['orgLevel'] == role['orgLevel']:
            score += 1

        if score > 2: # Increased threshold for better matches
            similar_roles.append({'role': role, 'score': score})
    
    similar_roles.sort(key=lambda x: x['score'], reverse=True)
    
    return [item['role'] for item in similar_roles[:max_similar]]

def generate_role_descriptions(roles_data):
    output_dir = 'role_descriptions'
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    for role in roles_data:
        filename = f"{role['title'].replace(' ', '-').replace('/', '-').lower()}.md"
        filepath = os.path.join(output_dir, filename)

        # Preserve existing detailed description
        description = f"\n{role['description']}\n" # Default from JSON
        try:
            with open(filepath, 'r', encoding='utf-8') as f:
                content = f.read()
                # Use regex to find the description between "## Description" and the next section
                match = re.search(r'## Description\n(.*?)\n## ', content, re.DOTALL)
                if match:
                    description = f"\n{match.group(1).strip()}\n"
        except FileNotFoundError:
            pass # File doesn't exist yet, use default description

        org_level = ", ".join(role['orgLevel']) if isinstance(role['orgLevel'], list) else role['orgLevel']
        medium = ", ".join(role['medium'])
        industry = ", ".join(role['industry'])
        responsibilities = "\n".join([f"- {resp}" for resp in role['responsibilities']])
        skills = "\n".join([f"- {skill}" for skill in role.get('skills', [])])

        similar_roles = find_similar_roles(role, roles_data)
        
        similar_roles_md = ""
        if similar_roles:
            similar_roles_md += "\n## Similar to other roles\n"
            for similar_role in similar_roles:
                similar_filename = f"{similar_role['title'].replace(' ', '-').replace('/', '-').lower()}.md"
                similar_roles_md += f"- [{similar_role['title']}]({similar_filename})\n"

        markdown_content = f"""# {role['title']}
## Description
{description.strip()}

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
{similar_roles_md}"""
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(markdown_content)
        print(f"Updated {filename}")

# Load the roles.json data
roles_json_path = "/Users/jens.wedin/Documents/Visual Studio/generate-role-descriptions/roles.json"
with open(roles_json_path, 'r', encoding='utf-8') as f:
    roles = json.load(f)

# Generate the markdown files
generate_role_descriptions(roles)
