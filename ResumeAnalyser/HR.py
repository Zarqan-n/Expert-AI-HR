from ResumeAnalyser.Resume import parse_resume
from ResumeAnalyser.Des import parse_descripton
from ResumeAnalyser.Configu import client
from ResumeAnalyser.Models import ResumeEvaluation
import json
import os
import time
from dotenv import load_dotenv
load_dotenv()


def evaluate_resume(resume_text: str, desc_text: str):
    resume = parse_resume(resume_text)
    desc = parse_descripton(desc_text)

    system_msg = f"""You are an expert HR recruiter and candidate evaluation specialist.

Your task is to evaluate a candidate's resume against a given job description.

Compare the candidate strictly against the requirements in the job description.

Evaluation rules:

- Calculate a matching score from 0 to 100.
- Consider required skills more important than preferred skills.
- Compare the candidate's actual experience with the required experience.
- Identify skills that match the job requirements.
- Identify required skills that are missing from the resume.
- Identify the candidate's major strengths for this particular job.
- Identify weaknesses or gaps relevant to this particular job.
- Do not assume that a candidate has a skill or experience that is not explicitly present in the resume.
- Do not give credit for a skill simply because it is related to another skill.
- Do not consider personal characteristics such as gender, age, religion, race, nationality, marital status, or other protected characteristics.
- Base the evaluation only on job-related qualifications and information present in the provided data.
- Give a concise explanation for the score.
- The recommendation should be based only on the candidate's qualifications and job requirements.
- Return only the structured output matching the ResumeEvaluation schema.
"""

    chat_completion = client.chat.completions.create(
        messages=[
            {
                "role": "system",
                "content": system_msg
            },
            {
                "role": "user",
                "content": f"Job description:{desc} and Resume: {resume}"
            }
        ],
        model=os.environ.get("MODEL"),
        response_format={
            "type": "json_schema",
            "json_schema": {
                "name": "ResumeEvaluation",
                "schema": ResumeEvaluation.model_json_schema()
            }
        }
    )

    return json.loads(chat_completion.choices[0].message.content)