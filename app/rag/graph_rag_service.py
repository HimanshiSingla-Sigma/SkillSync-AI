import re
from typing import Any, Dict, List, Optional
from app.rag.graph_retriever import GraphRetriever
from app.rag.context_builder import ContextBuilder
from app.rag.prompt_builder import PromptBuilder
from app.rag.response_generator import ResponseGenerator
from app.services.eligibility_service import EligibilityService
from app.repositories.student_repository import StudentRepository
from app.repositories.drive_repository import DriveRepository
from app.ai.faq_service import FAQService
from app.schemas.chat_schema import ChatMessageResponse
from app.core.logging import logger

STOPWORDS = {
    "a", "an", "the", "for", "and", "or", "but", "in", "on", "at", "to", "of", "with", "by", "from",
    "is", "are", "was", "were", "be", "been", "being", "have", "has", "had", "do", "does", "did",
    "can", "could", "should", "would", "will", "shall", "may", "might", "must",
    "i", "me", "my", "myself", "we", "our", "ours", "ourselves", "you", "your", "yours",
    "he", "him", "his", "she", "her", "hers", "it", "its", "they", "them", "their", "theirs",
    "what", "which", "who", "whom", "this", "that", "these", "those", "am", "how", "why", "when", "where",
    "all", "any", "both", "each", "few", "more", "most", "other", "some", "such",
    "no", "nor", "not", "only", "own", "same", "so", "than", "too", "very", "just",
    "eligible", "eligibility", "ellogible", "eligble", "ineligible",
    "drive", "drives", "placement", "placment", "job", "jobs", "company", "companies",
    "internship", "internships", "intern", "hiring", "recruitment", "opportunity", "opportunities",
    "hello", "hloo", "hey", "hi", "hii", "hiii", "good", "morning", "afternoon", "evening", "night",
    "thanks", "thank", "please", "tell", "give", "show", "list", "find", "check", "apply", "applied",
}


class GraphRAGService:
    """
    Main GraphRAG Orchestration Engine:
    User Query -> Dual-Database Retrieval (MongoDB + Neo4j) -> Deterministic Injection -> Context Synthesis -> LLM Response
    """

    def __init__(
        self,
        retriever: Optional[GraphRetriever] = None,
        generator: Optional[ResponseGenerator] = None,
        eligibility_service: Optional[EligibilityService] = None,
        student_repo: Optional[StudentRepository] = None,
        drive_repo: Optional[DriveRepository] = None,
    ):
        self.retriever = retriever or GraphRetriever()
        self.generator = generator or ResponseGenerator()
        self.eligibility_service = eligibility_service or EligibilityService()
        self.student_repo = student_repo or StudentRepository()
        self.drive_repo = drive_repo or DriveRepository()

    async def process_student_query(
        self,
        student_id: str,
        question: str,
        drive_id: Optional[str] = None,
    ) -> ChatMessageResponse:
        logger.info(f"GraphRAG processing query for student '{student_id}': \"{question}\"")
        clean_q = question.strip().lower()

        # 1. Direct FAQ Match Check
        for faq in FAQService.get_faqs():
            faq_q = faq["question"].strip().lower()
            if (
                faq_q in clean_q
                or (len(clean_q) > 15 and clean_q in faq_q)
                or any(
                    phrase in clean_q
                    for phrase in [
                        "difference between eligibility and match",
                        "how is my eligibility calculated",
                        "how is eligibility calculated",
                        "update missing skills",
                    ]
                )
            ):
                student_doc = await self.student_repo.find_by_id(student_id)
                student_skills = student_doc.skills if student_doc else []
                return ChatMessageResponse(
                    question=question,
                    answer=faq["answer"],
                    retrieved_graph_context={"faq_match": faq["question"], "student_skills": student_skills},
                    suggested_skills_to_learn=[],
                    recommended_drives=[],
                )

        # 2. Extract Verified Student Profile (MongoDB + Neo4j)
        student_mongo = await self.student_repo.find_by_id(student_id)
        student_name = student_mongo.full_name if student_mongo else "Student"
        student_cgpa = student_mongo.profile.cgpa if student_mongo and student_mongo.profile else 0.0
        student_backlogs = student_mongo.profile.backlogs if student_mongo and student_mongo.profile else 0
        student_programme = student_mongo.profile.programme if student_mongo and student_mongo.profile else "Computer Science"
        student_skills = student_mongo.skills if student_mongo else []

        # 3. Target Drive Discovery (Only when specific drive requested or company named)
        target_drive_id = drive_id if drive_id and drive_id.strip() else None
        
        if not target_drive_id:
            # Extract non-stopword tokens of length >= 3
            tokens = [
                w for w in re.findall(r"[a-zA-Z0-9]+", question.lower())
                if len(w) >= 3 and w not in STOPWORDS
            ]
            if tokens:
                all_mongo_drives = await self.drive_repo.list_all(limit=50)
                for token in tokens:
                    for md in all_mongo_drives:
                        c_name_lower = md.company_name.lower()
                        title_lower = md.title.lower()
                        # Match whole word or meaningful stem in company name
                        if token in c_name_lower.split() or (len(token) >= 4 and token in c_name_lower):
                            target_drive_id = str(md.id)
                            break
                        # Match distinctive words in title (e.g. "backend", "fullstack", "intern")
                        if token in title_lower.split() and token not in ["developer", "engineer", "associate", "software"]:
                            target_drive_id = str(md.id)
                            break
                    if target_drive_id:
                        break

        # 4. Context Assembly & Dual-Database Analysis
        graph_context: Dict[str, Any] = {}
        suggested_skills: List[str] = []
        recommended_drives: List[str] = []

        if target_drive_id:
            # Single Drive Specific Inquiry
            graph_context = await self.retriever.retrieve_student_drive_graph_context(
                student_id=student_id, drive_id=target_drive_id
            ) or {}
            
            drive_mongo = await self.drive_repo.find_by_id(target_drive_id)
            if drive_mongo:
                graph_context["drive_title"] = graph_context.get("drive_title") or drive_mongo.title
                graph_context["company_name"] = graph_context.get("company_name") or drive_mongo.company_name
                graph_context["salary_package"] = drive_mongo.salary_package
                graph_context["min_cgpa"] = drive_mongo.eligibility_criteria.min_cgpa
                graph_context["max_backlogs"] = drive_mongo.eligibility_criteria.max_backlogs
                graph_context["required_skills"] = drive_mongo.required_skills
                graph_context["mandatory_skills"] = drive_mongo.eligibility_criteria.mandatory_skills

            graph_context["student_name"] = student_name
            graph_context["student_cgpa"] = student_cgpa
            graph_context["student_backlogs"] = student_backlogs
            graph_context["student_programme"] = student_programme
            graph_context["student_skills"] = student_skills

            req_skills = graph_context.get("required_skills", [])
            matched = [s for s in req_skills if s in student_skills]
            missing = [s for s in req_skills if s not in student_skills]
            graph_context["matched_skills"] = matched
            graph_context["missing_skills"] = missing

            eligibility_snapshot = None
            try:
                el_eval = await self.eligibility_service.check_eligibility(student_id, target_drive_id)
                eligibility_snapshot = el_eval.model_dump()
            except Exception as e:
                logger.warning(f"Could not compute eligibility snapshot: {e}")

            context_str = ContextBuilder.build_student_drive_context(
                graph_data=graph_context,
                deterministic_eligibility=eligibility_snapshot,
            )
            prompt = PromptBuilder.build_eligibility_explanation_prompt(question, context_str)
            suggested_skills = missing

        else:
            # Multi-Drive Knowledge Graph Evaluation across ALL active drives
            all_published_drives = await self.drive_repo.list_all(status="PUBLISHED", limit=20)
            if not all_published_drives:
                all_published_drives = await self.drive_repo.list_all(limit=20)

            evaluated_drives = []
            eligible_drives = []
            ineligible_drives = []

            for d in all_published_drives:
                req_skills = d.required_skills or []
                mand_skills = d.eligibility_criteria.mandatory_skills or []
                matched = [s for s in req_skills if s in student_skills]
                missing = [s for s in req_skills if s not in student_skills]
                missing_mand = [s for s in mand_skills if s not in student_skills]
                pct = (len(matched) / len(req_skills) * 100) if req_skills else 100.0

                cgpa_pass = student_cgpa >= d.eligibility_criteria.min_cgpa
                backlog_pass = student_backlogs <= d.eligibility_criteria.max_backlogs
                mand_pass = len(missing_mand) == 0

                is_eligible = cgpa_pass and backlog_pass and mand_pass
                failure_reasons = []
                if not cgpa_pass:
                    failure_reasons.append(f"CGPA {student_cgpa:.2f} is below cutoff {d.eligibility_criteria.min_cgpa:.2f}")
                if not backlog_pass:
                    failure_reasons.append(f"Active backlogs ({student_backlogs}) exceed max allowed ({d.eligibility_criteria.max_backlogs})")
                if not mand_pass:
                    failure_reasons.append(f"Missing mandatory skills: {', '.join(missing_mand)}")

                drive_entry = {
                    "drive_id": str(d.id),
                    "drive_title": d.title,
                    "company_name": d.company_name,
                    "salary_package": d.salary_package,
                    "min_cgpa": d.eligibility_criteria.min_cgpa,
                    "max_backlogs": d.eligibility_criteria.max_backlogs,
                    "match_pct": round(pct, 1),
                    "matched_skills": matched,
                    "missing_skills": missing,
                    "is_eligible": is_eligible,
                    "failure_reasons": failure_reasons,
                }

                evaluated_drives.append(drive_entry)
                if is_eligible:
                    eligible_drives.append(drive_entry)
                else:
                    ineligible_drives.append(drive_entry)

            # Sort suitable drives by match percentage
            suitable_drives = sorted(evaluated_drives, key=lambda x: x["match_pct"], reverse=True)

            graph_context = {
                "student_name": student_name,
                "student_cgpa": student_cgpa,
                "student_backlogs": student_backlogs,
                "student_skills": student_skills,
                "student_programme": student_programme,
                "suitable_drives": suitable_drives,
                "eligible_drives": eligible_drives,
                "ineligible_drives": ineligible_drives,
            }

            student_profile = {
                "full_name": student_name,
                "cgpa": student_cgpa,
                "backlogs": student_backlogs,
                "programme": student_programme,
                "skills": student_skills,
            }
            context_str = ContextBuilder.build_recommendations_context(student_profile, suitable_drives)
            prompt = PromptBuilder.build_career_advice_prompt(question, context_str)

            for d in eligible_drives if eligible_drives else suitable_drives:
                recommended_drives.append(f"{d.get('drive_title')} at {d.get('company_name')} ({d.get('salary_package', 'N/A')})")
                suggested_skills.extend(d.get("missing_skills", []))
            suggested_skills = sorted(list(set(suggested_skills)))[:6]

        # 5. Response Generation with Dynamic Graph Context
        llm_answer = await self.generator.generate_explanation(
            prompt=prompt,
            question=question,
            graph_context=graph_context,
        )

        return ChatMessageResponse(
            question=question,
            answer=llm_answer,
            retrieved_graph_context=graph_context,
            suggested_skills_to_learn=suggested_skills,
            recommended_drives=recommended_drives,
        )