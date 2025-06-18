def handle_dispatch(issue_type, urgency_level):
    if urgency_level in ["high", "critical"]:
        tech = get_technician(issue_type)
        return f"{tech} dispatched for urgent {issue_type} issue."
    return "Logged for review."
def get_technician(issue_type):
    techs = {
        "plumbing": "Plumber John",
        "gas": "Gas Specialist",
        "cleanliness": "Cleaning Crew",
        "noise": "Security",
        "general": "Manager"
    }
    return techs.get(issue_type, "Technician")