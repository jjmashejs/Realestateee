import re
KEYWORDS = {
    r"(leak|burst|flood)": ("plumbing", "critical"),
    r"(no water|low pressure)": ("plumbing", "high"),
    r"(noise|loud)": ("noise", "medium"),
    r"(clean|trash|dirty)": ("cleanliness", "low"),
    r"(gas smell)": ("gas", "critical")
}
def classify_issue(text):
    text = text.lower()
    for pattern, (issue, urgency) in KEYWORDS.items():
        if re.search(pattern, text):
            return issue, urgency
    return "general", "low"