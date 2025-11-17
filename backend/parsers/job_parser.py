from typing import Dict, Any, List
import re

DEFAULT_SKILL_DIFFICULTY = 0.0
DEFAULT_EDU_DIFFICULTY = -0.25
DEFAULT_EXP_DIFFICULTY = 0.25
DEFAULT_OTHER_DIFFICULTY = 0.0

COMMON_SKILLS = [
	"python", "java", "javascript", "sql", "c++", "c#", "go", "rust",
	"machine learning", "deep learning", "nlp", "computer vision",
	"aws", "azure", "gcp", "docker", "kubernetes",
	"pandas", "numpy", "scikit-learn", "tensorflow", "pytorch",
	"react", "node", "django", "flask", "fastapi",
]


def _extract_requirements_from_text(text: str) -> List[Dict[str, Any]]:
	items: List[Dict[str, Any]] = []
	lower = text.lower()

	# Skills
	for skill in COMMON_SKILLS:
		if skill in lower:
			items.append({"kind": "skill", "value": skill, "difficulty": DEFAULT_SKILL_DIFFICULTY})

	# Education
	if re.search(r"\b(bachelor|bs|ba|master|ms|phd|doctorate)\b", lower):
		edu = re.search(r"\b(bachelor|bs|ba|master|ms|phd|doctorate)\b", lower).group(1)
		items.append({"kind": "education", "value": edu, "difficulty": DEFAULT_EDU_DIFFICULTY})

	# Experience years
	yrs = re.findall(r"(\d+)\+?\s+years?", lower)
	if yrs:
		max_yrs = max(int(y) for y in yrs)
		items.append({"kind": "experience", "value": f"{max_yrs}+ years", "difficulty": DEFAULT_EXP_DIFFICULTY + (max_yrs - 2) * 0.1})

	# Generic bullet points as "other" items
	for line in text.splitlines():
		if re.match(r"^\s*[-*•]\s+", line):
			val = re.sub(r"^\s*[-*•]\s+", "", line).strip()
			if len(val) > 5:
				items.append({"kind": "other", "value": val, "difficulty": DEFAULT_OTHER_DIFFICULTY})

	return items


def parse_job_payload(payload: Dict[str, Any]) -> Dict[str, Any]:
	title = (payload.get("title") or "").strip() or None
	company = (payload.get("company") or "").strip() or None
	location = (payload.get("location") or "").strip() or None
	description = (payload.get("description") or "").strip() or None
	raw_text = (payload.get("raw_text") or "").strip()

	text = "\n".join([t for t in [title, company, location, description, raw_text] if t])
	requirements = _extract_requirements_from_text(text)
	return {
		"title": title,
		"company": company,
		"location": location,
		"description": description or raw_text or None,
		"requirements": requirements,
	}


