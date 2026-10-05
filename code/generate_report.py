import json
from pathlib import Path

INPUT_PATH = Path("data/requirements.json")
OUTPUT_PATH = Path("analysis_results.md")


def main():
    with open(INPUT_PATH, "r", encoding="utf-8") as f:
        data = json.load(f)

    lines = []

    lines.append("# Comprehensive Risk Analysis")
    lines.append("")
    lines.append(
        "This report contains the stakeholder-centered hazard analysis "
        "generated with LLM assistance and reviewed as part of a "
        "human-in-the-loop workflow."
    )
    lines.append("")

    total_hazards = 0

    for stakeholder_index, stakeholder in enumerate(data["analysis"], start=1):
        lines.append(f"## {stakeholder_index}. {stakeholder['stakeholder']}")
        lines.append("")

        lines.append("### Goals")
        lines.append("")

        for goal in stakeholder["goals"]:
            lines.append(f"- **{goal['goal_id']}**: {goal['goal']}")

        lines.append("")
        lines.append("### Losses, Requirements, Assumptions, and Specifications")
        lines.append("")

        for hazard_index, hazard in enumerate(stakeholder["hazards"], start=1):
            total_hazards += 1

            lines.append(f"#### {hazard['hazard_id']} / " f"{hazard['requirement_id']}")
            lines.append("")

            lines.append(f"**Related Goal:** {hazard['goal_id']}")
            lines.append("")

            lines.append(f"**Loss:** {hazard['loss']}")
            lines.append("")

            lines.append(
                f"**Requirement ({hazard['requirement_id']}):** "
                f"{hazard['requirement']}"
            )
            lines.append("")

            lines.append("**Assumptions (ASM):**")
            lines.append("")

            for asm in hazard["assumptions"]:
                lines.append(f"- **{asm['asm_id']}**: {asm['assumption']}")

            lines.append("")
            lines.append("**Specifications (SPEC):**")
            lines.append("")

            for spec in hazard["specifications"]:
                lines.append(f"- **{spec['spec_id']}**: " f"{spec['specification']}")

            lines.append("")

    OUTPUT_PATH.write_text("\n".join(lines), encoding="utf-8")

    print(f"Generated report for {len(data['analysis'])} stakeholders.")
    print(f"Included {total_hazards} losses/requirements.")
    print(f"Saved to {OUTPUT_PATH}")


if __name__ == "__main__":
    main()
