from graphviz import Digraph
from pathlib import Path

OUTPUT_DIR = Path("figures")
OUTPUT_DIR.mkdir(exist_ok=True)


def build_original_tree():
    dot = Digraph("fault_tree")
    dot.attr(rankdir="TB")
    dot.attr(label="Fault Tree: False Positive Leads to Harmful Action", labelloc="t")

    dot.node(
        "TOP",
        "TOP EVENT\nAn innocent person is treated as a confirmed sighting\n"
        "or subjected to harmful investigative action",
        shape="box",
    )

    dot.node("AND1", "AND", shape="circle")
    dot.edge("TOP", "AND1")

    dot.node(
        "ML",
        "ML wrong prediction\nPerson who is not the missing child\n"
        "is classified as a candidate match",
        shape="box",
    )

    dot.node("BARRIER", "Verification / confirmation barrier fails", shape="box")

    dot.edge("AND1", "ML")
    dot.edge("AND1", "BARRIER")

    dot.node("OR1", "OR", shape="circle")
    dot.edge("BARRIER", "OR1")

    dot.node(
        "SPEC1",
        "SPEC1 violated\nAutomated result is not clearly labeled\n"
        "as a candidate sighting",
        shape="box",
    )

    dot.node(
        "SPEC2",
        "SPEC2 violated\nSoftware automatically promotes\n"
        "a candidate to confirmed status",
        shape="box",
    )

    dot.node("NO_REVIEW", "Action occurs without effective human review", shape="box")

    dot.node("BAD_REVIEW", "Human review incorrectly confirms the match", shape="box")

    dot.edge("OR1", "SPEC1")
    dot.edge("OR1", "SPEC2")
    dot.edge("OR1", "NO_REVIEW")
    dot.edge("OR1", "BAD_REVIEW")

    # No-review path
    dot.node("AND2", "AND", shape="circle")
    dot.edge("NO_REVIEW", "AND2")

    dot.node("ASM1", "ASM1 violated\nAuthorized reviewer is unavailable", shape="box")

    dot.node(
        "SPEC3",
        "SPEC3 violated\nSoftware permits consequential action\n"
        "without explicit human verification",
        shape="box",
    )

    dot.edge("AND2", "ASM1")
    dot.edge("AND2", "SPEC3")

    # Incorrect-review path
    dot.node("OR2", "OR", shape="circle")
    dot.edge("BAD_REVIEW", "OR2")

    dot.node(
        "ASM2",
        "ASM2 violated\nCandidate evidence is insufficient\n"
        "for reliable human assessment",
        shape="box",
    )

    dot.node(
        "ASM3",
        "ASM3 violated\nInvestigators do not follow the\n"
        "required verification procedure",
        shape="box",
    )

    dot.node(
        "SPEC4",
        "SPEC4 violated\nSoftware does not present sufficient\n"
        "supporting evidence to reviewer",
        shape="box",
    )

    dot.node("HUMAN", "Human reviewer misjudges the candidate", shape="box")

    dot.edge("OR2", "ASM2")
    dot.edge("OR2", "ASM3")
    dot.edge("OR2", "SPEC4")
    dot.edge("OR2", "HUMAN")

    dot.render(OUTPUT_DIR / "fault_tree", format="png", cleanup=True)


def build_mitigated_tree():
    dot = Digraph("fault_tree_mitigated")
    dot.attr(rankdir="TB")
    dot.attr(label="Updated Fault Tree with System-Level Mitigations", labelloc="t")

    dot.node(
        "TOP",
        "TOP EVENT\nAn innocent person is treated as a confirmed sighting\n"
        "or subjected to harmful investigative action",
        shape="box",
    )

    dot.node("AND1", "AND", shape="circle")
    dot.edge("TOP", "AND1")

    dot.node(
        "ML",
        "ML wrong prediction\nPerson who is not the missing child\n"
        "is classified as a candidate match",
        shape="box",
    )

    dot.node("VERIFY", "Enhanced verification safeguards fail", shape="box")

    dot.node("CORROBORATE", "Independent corroboration safeguard fails", shape="box")

    dot.edge("AND1", "ML")
    dot.edge("AND1", "VERIFY")
    dot.edge("AND1", "CORROBORATE")

    # Mitigation 1
    dot.node("AND2", "AND", shape="circle")
    dot.edge("VERIFY", "AND2")

    dot.node("REVIEW1", "Reviewer 1 incorrectly confirms candidate", shape="box")

    dot.node(
        "REVIEW2",
        "Independent Reviewer 2 also\nincorrectly confirms candidate",
        shape="box",
    )

    dot.edge("AND2", "REVIEW1")
    dot.edge("AND2", "REVIEW2")

    # Mitigation 2
    dot.node("OR1", "OR", shape="circle")
    dot.edge("CORROBORATE", "OR1")

    dot.node(
        "BYPASS",
        "Software incorrectly permits action\nwithout required corroborating evidence",
        shape="box",
    )

    dot.node(
        "FALSE_EVIDENCE",
        "Independent corroborating evidence\nis itself incorrect or misleading",
        shape="box",
    )

    dot.edge("OR1", "BYPASS")
    dot.edge("OR1", "FALSE_EVIDENCE")

    dot.render(OUTPUT_DIR / "fault_tree_mitigated", format="png", cleanup=True)


def main():
    build_original_tree()
    build_mitigated_tree()

    print("Generated:")
    print("figures/fault_tree.png")
    print("figures/fault_tree_mitigated.png")


if __name__ == "__main__":
    main()
