from jira import JIRA

JiraUrl = 'https://quanoskazka.atlassian.net/'

class JiraConnector:

    def __init__(self, JiraUrl):
        self.JiraUrl = JiraUrl

    #jira = JIRA(JiraUrl)
    auth_jira = JIRA(JiraUrl, auth=('magnit_322@rambler.ru', 'Quant240420'))

    def get_task(self, key):
        try:
            issue = self.auth_jira.issue(key)
            return issue
        except Exception:
            return False

    def get_projects(self):
        return self.auth_jira.projects()

    def createTask(self, project, summary, user):
        try:
            new_issue = self.auth_jira.create_issue(project=project, summary=summary,
                                      description='Look into this one', issuetype={'name': 'Task'})
            return True
        except Exception:
            return False

    def createBag(self, project, summary, user):
        try:
            new_issue = self.auth_jira.create_issue(project=project, summary=summary,
                                      description='Look into this one', issuetype={'name': 'Bug'})
            return True
        except Exception:
            return False

    def getIssues(self, project):
        try:
            issues_in_proj = self.auth_jira.search_issues('project='+project)
            return issues_in_proj
        except Exception:
            return False
