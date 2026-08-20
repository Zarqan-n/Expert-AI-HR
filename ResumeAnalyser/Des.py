import os
import json
from ResumeAnalyser.Configu import client
from ResumeAnalyser.Models import job_description
from dotenv import load_dotenv
load_dotenv()

# Convert Description to json

desc = """Job description
We are looking for a highly motivated and talented Junior AI Engineer to join our team in India. The ideal candidate will have a strong foundation in artificial intelligence and machine learning, with excellent problem-solving skills and the ability to work collaboratively in a fast-paced environment.
Roles and Responsibility
Design, develop, and deploy AI models and algorithms to solve complex problems.
Collaborate with cross-functional teams to identify business needs and develop solutions.
Develop and maintain large-scale data pipelines and architectures.
Conduct research and stay updated on the latest advancements in AI and machine learning.
Participate in code reviews and contribute to improving overall code quality.
Work closely with senior engineers to design and implement new features.
Job Requirements
Strong understanding of machine learning fundamentals, including supervised and unsupervised learning.
Experience with deep learning frameworks such as TensorFlow or PyTorch.
Proficiency in programming languages such as Python, C++, or Java.
Excellent problem-solving skills and attention to detail.
Ability to work effectively in a team environment and communicate complex ideas clearly.
Strong analytical and critical thinking skills, with the ability to interpret complex data sets.


Disclaimer: This job description has been sourced from a public domain and may have been modified by Naukri.com to improve clarity for our users. We encourage job seekers to verify all details directly with the employer via their official channels before applying.
Role: Search Engineer
Industry Type: IT Services & Consulting
Department: Engineering - Software & QA
Employment Type: Full Time, Permanent
Role Category: Software Development
Education
UG: Any Graduate
PG: LLM in Law
Key Skills
pythongitdevopsmicrosoft azureawsdocker"""


def parse_descripton(desc_text=None):
    if desc_text is None:
        desc_text = desc

    if desc_text:
        chat_completion = client.chat.completions.create(
            messages=[
                {
                    "role": "system",
                    "content": """You are an experienced HR recruiter and recruitment analyst.

Your task is to carefully analyze the given job description and extract the required information into the provided schema.

Rules:
- Extract only information that is explicitly mentioned.
- Do not guess or fabricate missing details.
- If a field is not available, return an empty string for string fields and an empty list for list fields.
- Keep skills, preferred skills, and responsibilities as separate list items.
- Preserve the original meaning while keeping the output concise.
- Return only the structured output matching the schema.
"""
                },
                {
                    "role": "user",
                    "content": f"""Extract the following information from this job description:

- Job Title
- Experience Required
- Employment Type
- Required Skills
- Preferred Skills
- Education
- Responsibilities
- Location
- Work Mode
- Description:{desc_text}"""
                }
            ],
            model=os.environ.get("MODEL"),
            response_format={
                "type": "json_schema",
                "json_schema": {
                    "name": "job_description",
                    "schema": job_description.model_json_schema()
                }
            }
        )

        return json.loads(chat_completion.choices[0].message.content)

    return {}