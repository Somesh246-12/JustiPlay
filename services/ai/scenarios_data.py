# services/ai/scenarios_data.py

SCENARIOS = {
    "Junior Clerk": [  # Beginner
        {
            "id": "b1",
            "title": "The Unpaid Rent",
            "role": "Tenant (Sarah)",
            "context": "You are a tenant. Your landlord suddenly stopped accepting your rent checks without explanation, and you're afraid they are planning to evict you. You have tried to pay three times. You are anxious and confused.",
            "difficulty": "Easy"
        },
        {
            "id": "b2",
            "title": "The Broken Window",
            "role": "Homeowner (Mike)",
            "context": "Your neighbor's kid threw a baseball through your living room window. The neighbor is refusing to pay for the repair, saying 'kids will be kids'. It costs $500 to fix.",
            "difficulty": "Easy"
        },
        {
            "id": "b3",
            "title": "Late Delivery",
            "role": "Small Business Owner (Elena)",
            "context": "You ordered 100 custom t-shirts for an event last week, but they arrived two days after the event. The supplier is refusing a refund. You are angry about the wasted money.",
            "difficulty": "Easy"
        }
    ],
    "Legal Researcher": [ # Intermediate
        {
            "id": "i1",
            "title": "Breach of Employment Contract",
            "role": "Employee (David)",
            "context": "You were promised a $5,000 bonus in your employment contract after one year. It's been 14 months, and your boss says 'money is tight' and won't pay. You have the contract in writing.",
            "difficulty": "Medium"
        },
        {
            "id": "i2",
            "title": "Defective Car Purchase",
            "role": "Car Buyer (Jenny)",
            "context": "You bought a used car from a dealership 'as is', but the transmission failed the next day. The dealer hid this defect. You feel cheated and want your money back.",
            "difficulty": "Medium"
        }
    ],
    "Junior Associate": [ # Advanced
        {
            "id": "a1",
            "title": "Intellectual Property Theft",
            "role": "Software Developer (Raj)",
            "context": "You developed a mobile app as a side project. Your former employer is now claiming they own it because you used a company laptop once to check email. They are threatening to sue.",
            "difficulty": "Hard"
        },
         {
            "id": "a2",
            "title": "Medical Malpractice",
            "role": "Patient (Linda)",
            "context": "You went in for simple knee surgery, but the surgeon operated on the wrong leg. Now you can't walk properly and lost your job. The hospital is offering a small settlement to stay quiet.",
            "difficulty": "Hard"
        }
    ],
    # Fallback for higher levels
    "Senior Partner": [
        {
            "id": "s1",
            "title": "Corporate Merger Dispute",
            "role": "CEO (Mr. Sterling)",
            "context": "Your company is merging with another. You discovered they cooked their books to hide massive debts. You want to back out of the deal, but there's a $10M breakup fee.",
            "difficulty": "Expert"
        }
    ],
    "Legal Mastermind": [
        {
            "id": "m1",
            "title": "Class Action Defense",
            "role": "Factory Owner (Mrs. Vance)",
            "context": "50 residents are suing your factory for groundwater contamination. You followed all regulations at the time, but new science suggests the chemicals were harmful. You are facing bankruptcy.",
            "difficulty": "Legendary"
        }
    ]
}

DRAFTING_TASKS = {
    "Junior Clerk": [
        "Draft a simple Eviction Notice for non-payment of rent.",
        "Write a Demand Letter for a broken window repair.",
        "Draft a Refund Request letter for late delivery of goods."
    ],
    "Legal Researcher": [
        "Draft a Memorandum of Law regarding breach of employment contract.",
        "Write a Complaint for a defective vehicle lawsuit.",
        "Draft a Cease and Desist letter for noise nuisance."
    ],
    "Junior Associate": [
        "Draft a Motion to Dismiss in an Intellectual Property case.",
        "Write a Settlement Agreement for a medical malpractice claim.",
        "Draft a Non-Disclosure Agreement (NDA) for a tech startup."
    ],
    "Senior Partner": [
        "Draft a Merger Agreement clause regarding undisclosed liabilities.",
        "Write an Appellate Brief argument for a complex tort case."
    ],
    "Legal Mastermind": [
        "Draft a Supreme Court Amicus Brief on environmental regulations.",
        "Write a comprehensive Class Action Settlement proposal."
    ]
}

def get_scenarios_for_level(level_name):
    # Mapping to handle progression fallback
    if level_name in SCENARIOS:
        return SCENARIOS[level_name]
    
    # Check lower tiers if exact match not found
    if "Senior" in level_name:
        return SCENARIOS["Senior Partner"]
    elif "Associate" in level_name:
        return SCENARIOS["Junior Associate"]
    elif "Researcher" in level_name:
        return SCENARIOS["Legal Researcher"]
    else:
        return SCENARIOS["Junior Clerk"]

def get_drafting_task_for_level(level_name):
    import random
    tasks = DRAFTING_TASKS.get(level_name, DRAFTING_TASKS["Junior Clerk"])
    # Fallback logic similar to scenarios if needed, but simple get is fine for now if names match
    if level_name not in DRAFTING_TASKS:
         if "Senior" in level_name: tasks = DRAFTING_TASKS["Senior Partner"]
         elif "Associate" in level_name: tasks = DRAFTING_TASKS["Junior Associate"]
         elif "Researcher" in level_name: tasks = DRAFTING_TASKS["Legal Researcher"]
    
    return random.choice(tasks)
