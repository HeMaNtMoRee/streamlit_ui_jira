import pandas as pd

def get_initial_tickets():
    """Returns the initial mock Jira tickets as a pandas DataFrame."""
    data = {
        "Key": ["ENG-101", "ENG-102", "DES-201", "QA-301", "ENG-103", "DES-202", "ENG-104", "QA-302"],
        "Summary": [
            "Implement new authentication flow",
            "Fix memory leak in data parser",
            "Create mockups for dashboard",
            "Write E2E tests for login",
            "Update API documentation",
            "Design system component: Button",
            "Optimize database queries",
            "Test new search functionality"
        ],
        "Status": ["In Progress", "To Do", "Done", "In Progress", "To Do", "Done", "Review", "To Do"],
        "Priority": ["Highest", "High", "Medium", "High", "Low", "Medium", "High", "Medium"],
        "Assignee": ["Alice", "Bob", "Charlie", "Alice", "Charlie", "Bob", "Alice", "Charlie"],
        "Project": ["Alpha", "Alpha", "Beta", "Gamma", "Alpha", "Beta", "Gamma", "Gamma"],
        "Sprint": ["Sprint 1", "Sprint 1", "Sprint 2", "Sprint 1", "Backlog", "Sprint 2", "Sprint 3", "Sprint 3"]
    }
    return pd.DataFrame(data)

def get_initial_chat_history():
    """Returns the initial chat history."""
    return [
        {"role": "assistant", "content": "Hi there! I'm your Jira Assistant. I can help you find tickets, update statuses, or summarize project progress. What can I help you with today?"}
    ]
