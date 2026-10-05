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


def load_stakeholders():
    path = Path("data/stakeholders.json")

    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)["stakeholders"]


def analyze_stakeholder(stakeholder):
    prompt = f"""
You are performing stakeholder-centered hazard analysis for an ML-enabled
dashcam system.

System scenario:

{SCENARIO}

Stakeholder:

Name: {stakeholder["name"]}
Type: {stakeholder["type"]}
Description: {stakeholder["description"]}
Why they care: {stakeholder["why_they_care"]}

For this stakeholder, identify:

1. Important goals or values they care about.
2. Plausible losses or harms that could occur if the system fails,
   behaves incorrectly, or is misused.
3. A system requirement corresponding to each loss.

Focus on concrete harms to this stakeholder.

Generate between 3 and 5 loss/requirement pairs.

Requirements MUST describe only desired phenomena or outcomes in the
environment ("world").

A requirement must NOT specify how the software, dashcam, model, API,
database, or other system component implements the behavior.

Do NOT include implementation details such as:
- encryption algorithms
- confidence thresholds
- queues
- retry logic
- databases
- APIs
- authentication mechanisms
- automatic deletion
- software notifications
- model architecture

Bad requirement:
"The dashcam must encrypt images with AES-256 and upload them within
10 minutes."

Good requirement:
"Unauthorized parties do not gain access to identifying images or
location information."

Bad requirement:
"The model must only report matches above 0.90 confidence."

Good requirement:
"People who are not the missing child are not treated as confirmed
sightings solely because of an automated prediction."

Specifications describing how software achieves these requirements will
be generated in a later analysis step.

Avoid vague requirements such as:
- "The system should be secure."
- "The model should be accurate."
- "The system should work correctly."

Instead, write concrete requirements such as:
- "Authorized investigators should receive relevant sightings within
  an acceptable time window."
- "People who do not match the missing child should not be reported
  to investigators as confirmed sightings."

Return ONLY valid JSON in this exact structure:

{{
  "stakeholder": "{stakeholder["name"]}",
  "goals": [
    {{
      "goal_id": "G1",
      "goal": "Goal or value"
    }}
  ],
  "hazards": [
    {{
      "hazard_id": "H1",
      "goal_id": "G1",
      "loss": "Concrete loss or harm",
      "requirement_id": "REQ1",
      "requirement": "Requirement intended to prevent or reduce the loss"
    }}
  ]
}}

Do not include markdown or explanatory text outside the JSON.
"""

    response = client.responses.create(model="gpt-5-mini", input=prompt)

    return json.loads(response.output_text)


def main():
    stakeholders = load_stakeholders()

    results = []

    for i, stakeholder in enumerate(stakeholders, start=1):
        print(f"[{i}/{len(stakeholders)}] " f"Analyzing {stakeholder['name']}...")

        result = analyze_stakeholder(stakeholder)
        results.append(result)

    output = {"analysis": results}

    output_path = Path("data/hazards.json")
    output_path.parent.mkdir(parents=True, exist_ok=True)

    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(output, f, indent=2, ensure_ascii=False)

    total_hazards = sum(len(item["hazards"]) for item in results)

    print()
    print(f"Analyzed {len(results)} stakeholders.")
    print(f"Generated {total_hazards} losses/requirements.")
    print(f"Saved to {output_path}")


if __name__ == "__main__":
    main()
