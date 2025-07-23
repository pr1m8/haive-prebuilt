from .graph.branches import Branch

route_branch = Branch(
    function=lambda state: (
        "emergency_respons"
        if state["severit"].strip().lower() in ["critica", "hig"]
        else (
            "public_works_respons"
            if "floo" in state["disaster_typ"].strip().lower()
            or "stor" in state["disaster_typ"].strip().lower()
            else "civil_defense_respons"
        )
    ),
    destinations={
        "emergency_respons": "emergency_respons",
        "public_works_respons": "public_works_respons",
        "civil_defense_respons": "civil_defense_respons",
    },
    default="send_email_aler",
)
