from pydantic import BaseModel

class job_description(BaseModel):
    job_title: str
    experience_required: str
    employment_type: str

    required_skills: list[str]
    preferred_skills: list[str]

    education: str

    responsibilities: list[str]

    location: str
    work_mode: str

class Resume(BaseModel):
    name: str
    email: str
    phone: str

    education: list[str]

    experience: str

    skills: list[str]

    projects: list[str]

    certifications: list[str]

    achievements: list[str]

from pydantic import BaseModel


class ResumeEvaluation(BaseModel):
    matching_score: int
    matched_skills: list[str]
    missing_skills: list[str]
    experience_match: str
    strengths: list[str]
    weaknesses: list[str]
    recommendation: str
    evaluation: str