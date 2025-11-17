from __future__ import annotations

from pathlib import Path
from typing import Dict, List, Optional

import pandas as pd

DATA_FILE = Path(__file__).resolve().parents[2] / "linkedin_job_posts_insights.xlsx"


def _clean(value: Optional[str]) -> Optional[str]:
	if value is None:
		return None
	if isinstance(value, float) and pd.isna(value):
		return None
	value = str(value).strip()
	return value if value else None


def load_linkedin_records(limit: Optional[int] = None) -> List[Dict]:
	if not DATA_FILE.exists():
		return []

	df = pd.read_excel(DATA_FILE)
	records: List[Dict] = []

	for idx, row in df.iterrows():
		if limit is not None and len(records) >= limit:
			break

		title = _clean(row.get("job_title"))
		company = _clean(row.get("company_name"))
		location = _clean(row.get("location"))
		job_function = _clean(row.get("job_function"))
		employment_type = _clean(row.get("employment_type"))
		industry = _clean(row.get("industry"))
		hiring_status = _clean(row.get("hiring_status"))
		seniority_level = _clean(row.get("seniority_level"))
		date_val = row.get("date")
		date_str = None
		if pd.notna(date_val):
			try:
				date_str = pd.to_datetime(date_val).strftime("%Y-%m-%d")
			except Exception:
				date_str = str(date_val)

		desc_parts = []
		if job_function:
			desc_parts.append(f"Function: {job_function}")
		if industry:
			desc_parts.append(f"Industry: {industry}")
		if employment_type:
			desc_parts.append(f"Type: {employment_type}")
		if hiring_status:
			desc_parts.append(f"Status: {hiring_status}")
		if date_str:
			desc_parts.append(f"Posted: {date_str}")

		requirements = []
		if job_function:
			requirements.append({"kind": "skill", "value": job_function})
		if seniority_level:
			requirements.append({"kind": "experience", "value": seniority_level})
		if employment_type:
			requirements.append({"kind": "other", "value": f"Employment: {employment_type}"})
		if industry:
			requirements.append({"kind": "other", "value": f"Industry: {industry}"})
		if hiring_status:
			requirements.append({"kind": "other", "value": f"Hiring: {hiring_status}"})

		records.append(
			{
				"title": title or "Untitled",
				"company": company,
				"location": location,
				"description": " • ".join(desc_parts) if desc_parts else None,
				"requirements": requirements,
			}
		)

	return records

