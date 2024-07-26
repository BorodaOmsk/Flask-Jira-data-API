import os
basedir = os.path.abspath(os.path.dirname(__file__))


class Config(object):
    DEBUG = False
    TESTING = False
    CSRF_ENABLED = True



class ProductionConfig(Config):
    DEVELOPMENT = False
    DEBUG = False
    JIRA_USERS = ''
    JIRA_PASSWORD = ''
    JIRA_URL = 'https://<Jira_url>/rest/api/2/'


class StagingConfig(Config):
    DEVELOPMENT = True
    DEBUG = True


class DevelopmentConfig(Config):
    DEVELOPMENT = True
    DEBUG = True
    JIRA_USERS = ''
    JIRA_PASSWORD = ''
    JIRA_URL = 'https://<Jira_url>/rest/api/2/'


class TestingConfig(Config):
    TESTING = True