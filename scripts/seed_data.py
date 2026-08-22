"""Script to seed realistic development data into MongoDB and synchronize with Neo4j."""

import asyncio
from app.core.database import init_databases, close_databases
from app.core.logging import logger
from app.schemas.student_schema import StudentRegisterRequest
from app.schemas.company_schema import CompanyRegisterRequest
from app.schemas.drive_schema import DriveCreateRequest, DriveEligibilityCriteriaSchema
from app.services.student_service import StudentService
from app.services.company_service import CompanyService
from app.services.drive_service import DriveService


async def seed_all_data():
    """Seeds demo students, companies, and placement drives."""
    logger.info("Starting database seeding process...")
    await init_databases()

    student_svc = StudentService()
    company_svc = CompanyService()
    drive_svc = DriveService()

    # 1. Seed Students
    student1_req = StudentRegisterRequest(
        email="rahul.sharma@example.com",
        password="Password123!",
        full_name="Rahul Sharma",
        cgpa=8.75,
        backlogs=0,
        programme="B.Tech Computer Science",
        branch="Computer Science",
        graduation_year=2025,
        skills=["python", "fastapi", "docker", "sql", "git", "mongodb"],
    )
    student2_req = StudentRegisterRequest(
        email="priya.patel@example.com",
        password="Password123!",
        full_name="Priya Patel",
        cgpa=6.80,
        backlogs=1,
        programme="B.Tech Information Technology",
        branch="Information Technology",
        graduation_year=2025,
        skills=["java", "spring boot", "mysql", "html", "css"],
    )

    try:
        s1 = await student_svc.register(student1_req)
        logger.info(f"Seeded student 1: {s1['student'].email}")
    except Exception as e:
        logger.warning(f"Student 1 seeding notice: {e}")

    try:
        s2 = await student_svc.register(student2_req)
        logger.info(f"Seeded student 2: {s2['student'].email}")
    except Exception as e:
        logger.warning(f"Student 2 seeding notice: {e}")

    # 2. Seed Recruiter Company
    company_req = CompanyRegisterRequest(
        name="Nexora Technologies",
        email="recruiter@nexora.io",
        password="Password123!",
        industry="Enterprise Software & Cloud AI",
        website="https://nexora.io",
        description="Pioneering enterprise AI workflows and cloud architectures.",
        location="Bengaluru, India",
    )

    try:
        c1 = await company_svc.register(company_req)
        company_id = c1["company"].id
        logger.info(f"Seeded company: {c1['company'].name} (ID: {company_id})")

        # 3. Seed Placement Drive
        drive_req = DriveCreateRequest(
            title="Associate Backend Engineer (Python/FastAPI)",
            role_type="Full-Time",
            salary_package="14.5 LPA",
            location="Bengaluru / Hybrid",
            job_description="We are seeking talented graduate engineers proficient in Python, FastAPI, Docker, and MongoDB to build scalable microservices.",
            required_skills=["python", "fastapi", "docker", "mongodb", "aws", "neo4j"],
            eligibility_criteria=DriveEligibilityCriteriaSchema(
                min_cgpa=7.50,
                max_backlogs=0,
                allowed_programmes=["B.Tech Computer Science", "B.Tech Information Technology"],
                allowed_graduation_years=[2025],
                mandatory_skills=["python", "fastapi"],
            ),
        )

        d1 = await drive_svc.create_drive(company_id, drive_req)
        logger.info(f"Seeded placement drive: '{d1.title}' (ID: {d1.id})")

    except Exception as e:
        logger.warning(f"Company/Drive seeding notice: {e}")

    await close_databases()
    logger.info("Database seeding successfully concluded.")


if __name__ == "__main__":
    asyncio.run(seed_all_data())