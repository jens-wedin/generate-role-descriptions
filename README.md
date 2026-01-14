# Role Description Generator

This project contains a Python script to generate Markdown files for different job roles based on a JSON input file. The generated Markdown files provide a structured description for each role, including details about the organizational level, medium, industry, responsibilities, and skills.

## Project Structure

- `roles.json`: A JSON file containing an array of role objects. Each object defines a specific role with its attributes.
- `generate_role_descriptions.py`: A Python script that reads the `roles.json` file and generates a Markdown file for each role.
- `role-descriptions/`: The directory where the generated Markdown files are saved.

## How to Use

1.  **Populate `roles.json`**: Make sure the `roles.json` file is populated with the role data you want to use. Each role should be a JSON object with the following structure:
    ```json
    {
      "id": "role-id",
      "title": "Role Title",
      "orgLevel": "IC",
      "medium": ["Digital"],
      "industry": ["Tech"],
      "description": "A brief description of the role.",
      "responsibilities": [
        "Responsibility 1",
        "Responsibility 2"
      ],
      "skills": [
        "Skill 1",
        "Skill 2"
      ]
    }
    ```

2.  **Run the script**: Execute the Python script from your terminal:
    ```bash
    python generate_role_descriptions.py
    ```

3.  **Find the output**: The script will generate a Markdown file for each role in the `role-descriptions` directory. The filename will be a sanitized version of the role's title (e.g., `role-title.md`).

## Generated File Structure

Each generated Markdown file will have the following structure:

```markdown
# [Role Title]

## Description
[Description]

## Org Level
[Org Level]

## Medium
[Medium]

## Industry
[Industry]

## Responsibilities
- [Responsibility 1]
- [Responsibility 2]

## Skills
- [Skill 1]
- [Skill 2]

## Similar to other roles
- [Similar Role 1](./similar-role-1.md)
- [Similar Role 2](./similar-role-2.md)
```
