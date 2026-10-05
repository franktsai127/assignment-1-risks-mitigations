import json
import os
from pathlib import Path

from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))


def load_hazards():
    path = Path("data/hazards.json")

    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)["analysis"]


def analyze_requirement(stakeholder, hazard):
    prompt = f"""
You are performing requirements and safety analysis for an ML-enabled
dashcam system that helps locate missing children.

Stakeholder:
{stakeholder}

Loss:
{hazard["loss"]}

Requirement:
{hazard["requirement"]}

Analyze this requirement by identifying environmental assumptions (ASM)
and software specifications (SPEC).

Definitions:

ASM:
An environmental assumption describes something about the real-world
environment that the software depends on being true.

Examples:
- Investigators review received candidate sightings within a reasonable time.
- Network connectivity becomes available often enough for delayed reports
  to eventually reach investigators.
- Reference images provided for a missing-child case correspond to the
  correct child.

ASM must describe phenomena in the environment, or assumptions connecting
environment phenomena to information observable by the software.

SPEC:
A software specification describes behavior or responsibilities of the
software at the interface between the machine and the environment.

Examples:
- The software labels automated detections as candidate sightings rather
  than confirmed sightings.
- The software records timestamps and available location metadata for each
  candidate sighting.
- The software restricts access to search results to authenticated,
  authorized accounts.

SPEC should describe what the software must do to help establish the
requirement, given the environmental assumptions.

Important rules:

1. Do not rewrite the requirement.
2. Do not put software behavior in ASM.
3. Do not put uncontrollable environmental behavior in SPEC.
4. Keep each ASM and SPEC concrete and testable.
5. Generate between 2 and 4 ASMs.
6. Generate between 2 and 4 SPECs.
7. Avoid vague statements such as:
   - "The environment behaves correctly."
   - "The system should be secure."
   - "The model should be accurate."
8. Include ML-related behavior in SPEC when relevant, but do not assume
   the ML model is always correct.

Return ONLY valid JSON using this exact structure:

{{
  "assumptions": [
    {{
      "asm_id": "ASM1",
      "assumption": "Environmental assumption"
    }}
  ],
  "specifications": [
    {{
      "spec_id": "SPEC1",
      "specification": "Software specification"
    }}
  ]
}}

Do not include markdown or explanatory text outside the JSON.
"""

    response = client.responses.create(model="gpt-5-mini", input=prompt)

    return json.loads(response.output_text)


def main():
    analyses = load_hazards()

    results = []
    total_requirements = 0

    for stakeholder_index, stakeholder_analysis in enumerate(analyses, start=1):
        stakeholder = stakeholder_analysis["stakeholder"]

        print(
            f"[{stakeholder_index}/{len(analyses)}] "
            f"Analyzing requirements for {stakeholder}..."
        )

        stakeholder_result = {
            "stakeholder": stakeholder,
            "goals": stakeholder_analysis["goals"],
            "hazards": [],
        }

        for hazard in stakeholder_analysis["hazards"]:
            total_requirements += 1

            requirement_analysis = analyze_requirement(stakeholder, hazard)

            enriched_hazard = {
                **hazard,
                "assumptions": requirement_analysis["assumptions"],
                "specifications": requirement_analysis["specifications"],
            }

            stakeholder_result["hazards"].append(enriched_hazard)

        results.append(stakeholder_result)

    output = {"analysis": results}

    output_path = Path("data/requirements.json")

    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(output, f, indent=2, ensure_ascii=False)

    total_asms = sum(
        len(h["assumptions"]) for stakeholder in results for h in stakeholder["hazards"]
    )

    total_specs = sum(
        len(h["specifications"])
        for stakeholder in results
        for h in stakeholder["hazards"]
    )

    print()
    print(f"Analyzed {total_requirements} requirements.")
    print(f"Generated {total_asms} assumptions.")
    print(f"Generated {total_specs} specifications.")
    print(f"Saved to {output_path}")


if __name__ == "__main__":
    main()
