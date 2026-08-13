from Configu import client
from Models import Resume
import json
import os
from dotenv import load_dotenv
load_dotenv()


sys_msg = f"""You are an expert HR recruiter and resume data extraction specialist.

Your task is to carefully analyze the provided resume and extract relevant candidate information.

Extract only information that is explicitly present in the resume.

Rules:
- Do not guess or fabricate information.
- Do not infer skills, experience, education, or certifications that are not mentioned.
- Preserve the meaning of the original resume.
- Extract each skill as a separate item.
- Extract each education qualification as a separate item.
- Extract each project as a separate item.
- Extract each certification as a separate item.
- Extract each achievement as a separate item.
- If information is missing, use an empty string for string fields and an empty list for list fields.
- Do not evaluate or rank the candidate.
- Return only data matching the provided Resume schema.
- Resume schema:{Resume}"""


def parse_resume(resume_text_input=None):
    if resume_text_input is None:
        return {}

    if resume_text_input:
        user_msg = f"""Extract the candidate information from the following resume.Resume:{resume_text_input}"""
        chat = client.chat.completions.create(
            messages=[
                {
                    "role": "system",
                    "content": sys_msg
                },
                {
                    "role": "user",
                    "content": user_msg
                }
            ],
            model=os.environ.get("MODEL"),
            response_format={
                "type": "json_schema",
                "json_schema": {
                    "name": "Resume",
                    "schema": Resume.model_json_schema()
                }
            }
        )
        return json.loads(chat.choices[0].message.content)

    return {}