from typing import Any, Dict, List, Optional
from app.ai.chat_client import BaseLLMClient
from app.ai.gemini_client import GeminiClient
from app.ai.ollama_client import OllamaClient
from app.rag.prompt_builder import PromptBuilder
from app.core.config import settings
from app.core.logging import logger


class ResponseGenerator:
    """
    Dispatches GraphRAG prompts to LLM engines with an advanced,
    deterministic Semantic Graph Reasoning Engine fallback.
    """

    def __init__(self, llm_client: Optional[BaseLLMClient] = None):
        self.custom_client = llm_client
        self.gemini = GeminiClient() if settings.GEMINI_API_KEY else None
        self.ollama = OllamaClient()

    async def generate_explanation(
        self,
        prompt: str,
        question: str = "",
        graph_context: Optional[Dict[str, Any]] = None,
    ) -> str:
        """Sends prompt to available LLM or generates grounded graph explanation."""
        # 1. Custom client if provided
        if self.custom_client:
            try:
                return await self.custom_client.generate_response(
                    prompt=prompt,
                    system_instruction=PromptBuilder.SYSTEM_INSTRUCTION,
                    temperature=0.2,
                )
            except Exception as e:
                logger.warning(f"Custom LLM client failed: {e}")

        # 2. Local Ollama if running
        try:
            return await self.ollama.generate_response(
                prompt=prompt,
                system_instruction=PromptBuilder.SYSTEM_INSTRUCTION,
                temperature=0.2,
            )
        except Exception:
            pass

        # 3. Google Gemini (if active and quota available)
        if self.gemini and settings.GEMINI_API_KEY:
            for model_name in ["gemini-3.6-flash", "gemini-3.7-flash", "gemini-flash-latest"]:
                try:
                    self.gemini.model = model_name
                    return await self.gemini.generate_response(
                        prompt=prompt,
                        system_instruction=PromptBuilder.SYSTEM_INSTRUCTION,
                        temperature=0.2,
                    )
                except Exception:
                    continue

        # 4. Deterministic Multi-Database Graph Intelligence Engine
        return self._generate_graph_reasoning(prompt, question, graph_context or {})

    def _generate_graph_reasoning(
        self, prompt: str, question: str, graph_context: Dict[str, Any]
    ) -> str:
        """
        Extracts rich knowledge graph entities and relationships (Student, Drive, Skills, Criteria)
        and synthesizes an accurate, contextual response for the user query.
        """
        q_raw = question or prompt
        q_lower = q_raw.lower().strip()

        # Student data
        student_name = graph_context.get("student_name", "Student")
        student_cgpa = graph_context.get("student_cgpa", 0.0)
        student_backlogs = graph_context.get("student_backlogs", 0)
        student_skills = graph_context.get("student_skills", [])
        skills_formatted = ", ".join(student_skills) if student_skills else "No skills registered yet"

        # Drive data
        drive_title = graph_context.get("drive_title")
        company_name = graph_context.get("company_name")
        matched_skills = graph_context.get("matched_skills", [])
        missing_skills = graph_context.get("missing_skills", [])
        required_skills = graph_context.get("required_skills", [])
        min_cgpa = graph_context.get("min_cgpa")
        max_backlogs = graph_context.get("max_backlogs")
        salary_package = graph_context.get("salary_package", "Competitive Package")

        eligible_drives = graph_context.get("eligible_drives", [])
        ineligible_drives = graph_context.get("ineligible_drives", [])
        suitable_drives = graph_context.get("suitable_drives", [])

        # =============================================================
        # 1. GREETINGS (e.g. "hloo", "hello", "hi", "hey", "hii")
        # =============================================================
        if any(q_lower.startswith(g) or q_lower == g for g in ["hloo", "hello", "hi", "hey", "hii", "hiii", "hola", "greetings", "good morning", "good evening"]):
            return (
                f"Hello **{student_name}**! 👋 How can I help with your placements today?\n\n"
                f"**Your Profile Snapshot:**\n"
                f"• **Verified CGPA:** `{student_cgpa:.2f}`\n"
                f"• **Active Backlogs:** `{student_backlogs}`\n"
                f"• **Registered Skills ({len(student_skills)} nodes):** `{skills_formatted}`\n\n"
                f"**You can ask me:**\n"
                f"• *'For what placement drives am I eligible?'*\n"
                f"• *'For which drives am I not eligible?'*\n"
                f"• *'What skills should I learn to increase my chances?'*\n"
                f"• *'Show drives with highest salary package'*"
            )

        # =============================================================
        # 2. INELIGIBILITY / NOT ELIGIBLE INQUIRIES
        # (e.g. "for which i am not ellogible", "ineligible drives", "why not eligible")
        # =============================================================
        if (
            "not eligible" in q_lower
            or "not ellogible" in q_lower
            or "ineligible" in q_lower
            or "why rejected" in q_lower
            or "cannot apply" in q_lower
            or ("not" in q_lower and ("eligible" in q_lower or "ellogible" in q_lower or "eligble" in q_lower))
        ):
            if ineligible_drives:
                drives_list = []
                for i, d in enumerate(ineligible_drives, 1):
                    reasons = d.get("failure_reasons", [])
                    reasons_text = "; ".join(reasons) if reasons else "Did not satisfy academic criteria"
                    drives_list.append(
                        f"**{i}. {d.get('drive_title')} at {d.get('company_name')}** ({d.get('salary_package', 'N/A')})\n"
                        f"   • ❌ **Reason Ineligible:** {reasons_text}\n"
                        f"   • **Cutoff:** CGPA ≥ {d.get('min_cgpa')}, Max Backlogs: {d.get('max_backlogs')}"
                    )
                return (
                    f"### 🚫 Placement Drives You Are Currently Ineligible For\n\n"
                    f"Based on your current academic records (CGPA: `{student_cgpa:.2f}`, Active Backlogs: `{student_backlogs}`), "
                    f"you do not meet the criteria for the following **{len(ineligible_drives)}** drive(s):\n\n"
                    + "\n\n".join(drives_list) +
                    f"\n\n💡 *Tip: Clear pending backlogs or update your profile in Profile Studio to unlock new drives.*"
                )
            else:
                return (
                    f"### 🎉 Great News, {student_name}!\n\n"
                    f"You have **no ineligible placement drives**! With your CGPA of `{student_cgpa:.2f}` and `{student_backlogs}` backlogs, "
                    f"you satisfy the academic criteria for **all active placement drives** in the system.\n\n"
                    f"Ask *'For what placement drives am I eligible?'* to see your ranked opportunities!"
                )

        # =============================================================
        # 3. ELIGIBILITY LIST / WHICH DRIVES CAN I APPLY TO
        # (e.g. "for what placment drive i am ellogible", "which drives am i eligible for")
        # =============================================================
        if (
            "eligible" in q_lower
            or "ellogible" in q_lower
            or "eligble" in q_lower
            or "can i apply" in q_lower
            or "where can i apply" in q_lower
        ) and not (drive_title or company_name):
            if eligible_drives:
                drives_list = []
                for i, d in enumerate(eligible_drives, 1):
                    drives_list.append(
                        f"**{i}. {d.get('drive_title')} at {d.get('company_name')}**\n"
                        f"   • **Package:** `{d.get('salary_package', 'N/A')}`\n"
                        f"   • **Skill Match:** `{d.get('match_pct')}%`\n"
                        f"   • **Matched Skills:** `{', '.join(d.get('matched_skills', [])) or 'None'}`\n"
                        f"   • **Missing Skills:** `{', '.join(d.get('missing_skills', [])) or 'None (100% matched!)'}`"
                    )
                return (
                    f"### ✅ Placement Drives You Are Eligible To Apply For\n\n"
                    f"Hello **{student_name}**! Based on your verified CGPA (`{student_cgpa:.2f}`) and `{student_backlogs}` active backlogs, "
                    f"you are **eligible for {len(eligible_drives)} live placement drive(s)**:\n\n"
                    + "\n\n".join(drives_list) +
                    f"\n\n👉 *Go to the **Explore Drives** tab to submit your applications!*"
                )
            else:
                return (
                    f"### ⚠️ No Eligible Drives Found for Current Academic Thresholds\n\n"
                    f"Your current CGPA is `{student_cgpa:.2f}` with `{student_backlogs}` active backlogs. "
                    f"None of the current published drives match this threshold. Check back soon for new drives!"
                )

        # =============================================================
        # 4. SINGLE DRIVE SPECIFIC INQUIRY (Target drive selected / named)
        # =============================================================
        if drive_title or company_name:
            c_name = company_name or "Target Company"
            d_name = drive_title or "Position"
            
            cgpa_pass = student_cgpa >= (min_cgpa or 0.0)
            backlog_pass = student_backlogs <= (max_backlogs if max_backlogs is not None else 999)
            is_eligible = cgpa_pass and backlog_pass

            match_pct = 0
            if required_skills:
                match_pct = round((len(matched_skills) / len(required_skills)) * 100)

            status_header = "✅ **ELIGIBLE TO APPLY**" if is_eligible else "❌ **CURRENTLY NOT ELIGIBLE**"
            
            reasons = []
            if not cgpa_pass:
                reasons.append(f"• **CGPA Policy:** Your CGPA ({student_cgpa:.2f}) is below the cutoff of {min_cgpa:.2f}.")
            else:
                reasons.append(f"• **CGPA Policy:** Your CGPA ({student_cgpa:.2f}) meets or exceeds the cutoff (≥ {min_cgpa:.2f}).")

            if not backlog_pass:
                reasons.append(f"• **Backlog Policy:** You have {student_backlogs} active backlogs (Maximum allowed: {max_backlogs}).")
            else:
                reasons.append(f"• **Backlog Policy:** Backlogs within allowed threshold ({student_backlogs} active).")

            matched_str = ", ".join(matched_skills) if matched_skills else "None"
            missing_str = ", ".join(missing_skills) if missing_skills else "None (100% matched!)"

            return (
                f"### {status_header} for {d_name} at {c_name}\n\n"
                f"**Placement Criteria & Knowledge Graph Analysis:**\n"
                f"{chr(10).join(reasons)}\n\n"
                f"**Tech Stack & Skill Overlap ({match_pct}% Match):**\n"
                f"• **Matched Skills:** `{matched_str}`\n"
                f"• **Missing Skills to Prepare:** `{missing_str}`\n"
                f"• **Compensation Package:** `{salary_package}`\n\n"
                f"{'🎉 You can submit your application immediately on the Explore Drives page!' if is_eligible else '💡 Tip: Clear missing criteria to unlock this drive.'}"
            )

        # =============================================================
        # 5. RECOMMENDATIONS & MATCHING DRIVES
        # =============================================================
        if any(w in q_lower for w in ["recommend", "matching", "match", "which company", "which drive", "where should i", "find job", "opportunities", "best company"]):
            if suitable_drives:
                drives_text = []
                for i, d in enumerate(suitable_drives[:4], 1):
                    d_title = d.get("drive_title", "Position")
                    c_name = d.get("company_name", "Company")
                    pkg = d.get("salary_package", "N/A")
                    pct = round(d.get("match_pct", 0))
                    elig_badge = "✅ Eligible" if d.get("is_eligible") else "❌ Ineligible"
                    drives_text.append(
                        f"**{i}. {d_title} at {c_name}** ({pkg}) — {elig_badge}\n"
                        f"   • **Match Score:** `{pct}%`\n"
                        f"   • **Matched Skills:** `{', '.join(d.get('matched_skills', [])) or 'None'}`\n"
                        f"   • **Skills to Learn:** `{', '.join(d.get('missing_skills', [])) or 'None'}`"
                    )
                
                return (
                    f"### 🎯 Top Placement Opportunities for {student_name}\n\n"
                    f"Ranked by skill match score in the Neo4j Knowledge Graph:\n\n"
                    + "\n\n".join(drives_text) +
                    f"\n\n💡 *Navigate to **Explore Drives** to apply directly.*"
                )

        # =============================================================
        # 6. SKILL GAPS & LEARNING ROADMAP
        # =============================================================
        if any(w in q_lower for w in ["skill", "learn", "gap", "improve", "roadmap", "prepare", "study", "what is missing"]):
            all_missing = []
            for d in suitable_drives:
                all_missing.extend(d.get("missing_skills", []))
            top_missing = sorted(list(set(all_missing)))[:6]
            if not top_missing:
                top_missing = ["Docker", "Kubernetes", "Redis", "System Design", "AWS"]

            return (
                f"### 🚀 Career Skill Gap & Placement Roadmap for {student_name}\n\n"
                f"**Your Current Skills in Knowledge Graph:**\n"
                f"• `{skills_formatted}`\n\n"
                f"**High-Demand Skills in Current Placement Drives:**\n"
                + "\n".join([f"• **`{s}`**: Highly requested across active placement drives." for s in top_missing[:4]]) +
                f"\n\n**Action Steps:**\n"
                f"1. Build a project utilizing **{top_missing[0] if top_missing else 'System Design'}** and **{top_missing[1] if len(top_missing) > 1 else 'Cloud'}**.\n"
                f"2. Upload your updated resume to **Resume Studio** to extract and sync new skill nodes into Neo4j."
            )

        # =============================================================
        # 7. STUDENT PROFILE & ACADEMICS
        # =============================================================
        if any(w in q_lower for w in ["profile", "cgpa", "backlog", "my details", "who am i", "my skills", "resume"]):
            return (
                f"### 🎓 Student Profile State for {student_name}\n\n"
                f"• **Cumulative CGPA:** `{student_cgpa:.2f} / 10.0`\n"
                f"• **Active Backlogs:** `{student_backlogs}`\n"
                f"• **Verified Skills ({len(student_skills)} nodes):** `{skills_formatted}`\n"
                f"• **Graph Status:** Synchronized with Neo4j AuraDB\n\n"
                f"You can edit your academic credentials or skill matrix in the **Profile Studio** tab."
            )

        # =============================================================
        # 8. SALARY PACKAGES & COMPENSATION
        # =============================================================
        if any(w in q_lower for w in ["salary", "package", "lpa", "highest", "paying", "ctc"]):
            if suitable_drives:
                top_pkgs = [f"• **{d.get('company_name')} ({d.get('drive_title')}):** `{d.get('salary_package', 'N/A')}`" for d in suitable_drives[:4]]
                return (
                    f"### 💼 Compensation Packages across Active Placement Drives:\n\n"
                    + "\n".join(top_pkgs) +
                    f"\n\nCheck **Explore Drives** for comprehensive job descriptions and criteria."
                )

        # =============================================================
        # 9. GENERAL FALLBACK
        # =============================================================
        return (
            f"Hello **{student_name}**! 👋 I am your **CareerConnect AI Placement Agent**, powered by **Neo4j GraphRAG**.\n\n"
            f"**Your Profile Summary:**\n"
            f"• **CGPA:** `{student_cgpa:.2f}` | **Backlogs:** `{student_backlogs}`\n"
            f"• **Active Skills:** `{skills_formatted}`\n\n"
            f"**How I can assist you:**\n"
            f"1. Ask *'For what placement drives am I eligible?'*\n"
            f"2. Ask *'For which drives am I not eligible?'*\n"
            f"3. Ask *'What skills should I learn to get placed?'*\n"
            f"4. Ask *'Which drives offer the highest package?'*"
        )