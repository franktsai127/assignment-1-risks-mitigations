import json
import os
from pathlib import Path

from dotenv import load_dotenv
from openai import OpenAI


load_dotenv()

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

SCENARIO = """
We are developing an ML-enabled dashcam feature to help locate children
reported missing.

The dashcam can search recorded footage for possible appearances of a
missing child using a person-recognition model.

The dashcam does not have direct internet access. It may communicate with
phones, cars, or Wi-Fi hotspots using USB, Bluetooth, or Wi-Fi.

Dashcams differ in battery capacity, processing power, and storage.

Searches are coordinated with authorities and a non-profit child-safety
organization.

Users may have concerns about privacy, mobile-data usage, and device costs.

The person-recognition model is supplied by an external contractor and may
be customized for deployment.

The system may use edge processing, cloud processing, or a combination.
"""


def generate_stakeholders():
    prompt = f"""
You are helping perform stakeholder-centered hazard analysis for an
ML-enabled system.

System scenario:

{SCENARIO}

Identify between 10 and 20 direct and indirect stakeholders who either:

- interact with the system,
- depend on the system,
- operate or maintain the system,
- are affected by decisions made by the system, or
- may experience harm if the system fails or is misused.

For each stakeholder, provide:

1. name
2. type: direct or indirect
3. description
4. why_they_care

Return ONLY valid JSON using this exact structure:

{{
  "stakeholders": [
    {{
      "name": "Stakeholder name",
      "type": "direct",
      "description": "Short description",
      "why_they_care": "Why this stakeholder cares about the system"
    }}
  ]
}}

Do not include markdown or explanatory text outside the JSON.
"""

    response = client.responses.create(
        model="gpt-5-mini",
        input=prompt
    )

    output = response.output_text
    return json.loads(output)


def main():
    stakeholders = generate_stakeholders()

    output_path = Path("data/stakeholders.json")
    output_path.parent.mkdir(parents=True, exist_ok=True)

    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(stakeholders, f, indent=2, ensure_ascii=False)

    print(f"Generated {len(stakeholders['stakeholders'])} stakeholders.")
    print(f"Saved to {output_path}")


if __name__ == "__main__":
    main()