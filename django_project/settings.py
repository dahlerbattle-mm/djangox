from pathlib import Path
import socket
# from dotenv import load_dotenv
import environ

env = environ.Env()
environ.Env.read_env()

# # Load the .env file
# load_dotenv()

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/dev/howto/deployment/checklist/

# https://docs.djangoproject.com/en/dev/ref/settings/#secret-key
# SECURITY WARNING: keep the secret key used in production secret!
# SECRET_KEY = "django-insecure-0peo@#x9jur3!h$ryje!$879xww8y1y66jx!%*#ymhg&jkozs2"
SECRET_KEY = env("SECRET_KEY")

# https://docs.djangoproject.com/en/dev/ref/settings/#debug
# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

# https://docs.djangoproject.com/en/dev/ref/settings/#allowed-hosts
ALLOWED_HOSTS = ["localhost", "0.0.0.0", "127.0.0.1", "*"]


# Application definition
# https://docs.djangoproject.com/en/dev/ref/settings/#installed-apps
INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "whitenoise.runserver_nostatic",
    "django.contrib.staticfiles",
    "django.contrib.sites",
    'django.contrib.humanize',
    # Third-party
    "allauth",
    "allauth.account",
    "crispy_forms",
    "crispy_bootstrap5",
    "debug_toolbar",
    # Local
    "accounts",
    "pages",
    "dashboards",
    "settings",
    "integrations",
    "chat",
    "models",
    "dataroom",
    "subscription",
    "entities",
]

# https://docs.djangoproject.com/en/dev/ref/settings/#middleware
MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "whitenoise.middleware.WhiteNoiseMiddleware",  # WhiteNoise
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "debug_toolbar.middleware.DebugToolbarMiddleware",  # Django Debug Toolbar
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
    "allauth.account.middleware.AccountMiddleware",  # django-allauth
]

CSRF_TRUSTED_ORIGINS = [
    "https://officially-fast-condor.ngrok-free.app/*"
]

# https://docs.djangoproject.com/en/dev/ref/settings/#root-urlconf
ROOT_URLCONF = "django_project.urls"

# https://docs.djangoproject.com/en/dev/ref/settings/#wsgi-application
WSGI_APPLICATION = "django_project.wsgi.application"

# https://docs.djangoproject.com/en/dev/ref/settings/#templates
TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [BASE_DIR / "templates"],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ],
        },
    },
]

# For Docker/PostgreSQL usage uncomment this and comment the DATABASES config above
DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql",
        "NAME": "postgres",
        "USER": "postgres",
        "PASSWORD": "postgres",
        "HOST": "db",  # set in docker-compose.yml
        "PORT": 5432,  # default postgres port
    }
}

# Password validation
# https://docs.djangoproject.com/en/dev/ref/settings/#auth-password-validators
AUTH_PASSWORD_VALIDATORS = [
    {
        "NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.MinimumLengthValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.CommonPasswordValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.NumericPasswordValidator",
    },
]


# Internationalization
# https://docs.djangoproject.com/en/dev/topics/i18n/
# https://docs.djangoproject.com/en/dev/ref/settings/#language-code
LANGUAGE_CODE = "en-us"

# https://docs.djangoproject.com/en/dev/ref/settings/#time-zone
TIME_ZONE = "UTC"

# https://docs.djangoproject.com/en/dev/ref/settings/#std:setting-USE_I18N
USE_I18N = True

# https://docs.djangoproject.com/en/dev/ref/settings/#use-tz
USE_TZ = True

# https://docs.djangoproject.com/en/dev/ref/settings/#locale-paths
LOCALE_PATHS = [BASE_DIR / 'locale']

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/5.0/howto/static-files/

# https://docs.djangoproject.com/en/dev/ref/settings/#static-root
STATIC_ROOT = BASE_DIR / "staticfiles"

# https://docs.djangoproject.com/en/dev/ref/settings/#static-url
STATIC_URL = "/static/"

# https://docs.djangoproject.com/en/dev/ref/contrib/staticfiles/#std:setting-STATICFILES_DIRS
STATICFILES_DIRS = [BASE_DIR / "static"]

# https://whitenoise.readthedocs.io/en/latest/django.html
STORAGES = {
    "default": {
        "BACKEND": "django.core.files.storage.FileSystemStorage",
    },
    "staticfiles": {
        "BACKEND": "whitenoise.storage.CompressedManifestStaticFilesStorage",
    },
}

# Default primary key field type
# https://docs.djangoproject.com/en/stable/ref/settings/#default-auto-field
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# django-crispy-forms
# https://django-crispy-forms.readthedocs.io/en/latest/install.html#template-packs
CRISPY_ALLOWED_TEMPLATE_PACKS = 'bootstrap5'
CRISPY_TEMPLATE_PACK = "bootstrap5"

# https://docs.djangoproject.com/en/dev/ref/settings/#email-backend
EMAIL_BACKEND = "django.core.mail.backends.console.EmailBackend"

# https://docs.djangoproject.com/en/dev/ref/settings/#default-from-email
DEFAULT_FROM_EMAIL = "root@localhost"

# django-debug-toolbar
# https://django-debug-toolbar.readthedocs.io/en/latest/installation.html
# https://docs.djangoproject.com/en/dev/ref/settings/#internal-ips
hostname, _, ips = socket.gethostbyname_ex(socket.gethostname())
INTERNAL_IPS = [ip[:-1] + "1" for ip in ips]

# https://docs.djangoproject.com/en/dev/topics/auth/customizing/#substituting-a-custom-user-model
AUTH_USER_MODEL = "accounts.CustomUser"

# django-allauth config
# https://docs.djangoproject.com/en/dev/ref/settings/#site-id
SITE_ID = 1

# https://docs.djangoproject.com/en/dev/ref/settings/#login-redirect-url
LOGIN_REDIRECT_URL = "home"

# https://django-allauth.readthedocs.io/en/latest/views.html#logout-account-logout
ACCOUNT_LOGOUT_REDIRECT_URL = "home"

# https://django-allauth.readthedocs.io/en/latest/installation.html?highlight=backends
AUTHENTICATION_BACKENDS = (
    "django.contrib.auth.backends.ModelBackend",
    "allauth.account.auth_backends.AuthenticationBackend",
)
# https://django-allauth.readthedocs.io/en/latest/configuration.html
ACCOUNT_SESSION_REMEMBER = True
ACCOUNT_SIGNUP_PASSWORD_ENTER_TWICE = False
ACCOUNT_USERNAME_REQUIRED = False
ACCOUNT_AUTHENTICATION_METHOD = "email"
ACCOUNT_EMAIL_REQUIRED = True
ACCOUNT_UNIQUE_EMAIL = True

### This includes all details needed to receive OAuth authorization from customers ###
### TODO: Should this be included here or should I just link directly to the env folder when used? ###

#quickbooks information
QUICKBOOKS_REALM_ID = env('QUICKBOOKS_REALM_ID')
QUICKBOOKS_CLIENT_ID = env('QUICKBOOKS_CLIENT_ID')
QUICKBOOKS_CLIENT_SECRET = env('QUICKBOOKS_CLIENT_SECRET')
QUICKBOOKS_REDIRECT_URI = "https://officially-fast-condor.ngrok-free.app/integrations/callback/quickbooks/"

#hubspot information
HUBSPOT_APP_ID = env('HUBSPOT_APP_ID')
HUBSPOT_CLIENT_ID = env('HUBSPOT_CLIENT_ID')
HUBSPOT_CLIENT_SECRET = env('HUBSPOT_CLIENT_SECRET')
HUBSPOT_REDIRECT_URI = "https://officially-fast-condor.ngrok-free.app/integrations/callback/hubspot/"

#stripe information
STRIPE_APP_ID = env('STRIPE_APP_ID')
STRIPE_CLIENT_ID = env('STRIPE_CLIENT_ID')
STRIPE_CLIENT_SECRET = env('STRIPE_CLIENT_SECRET')
STRIPE_REDIRECT_URI = "https://officially-fast-condor.ngrok-free.app/integrations/callback/stripe/"

#jira information
JIRA_APP_ID = env('JIRA_APP_ID')
JIRA_CLIENT_ID = env('JIRA_CLIENT_ID')
JIRA_CLIENT_SECRET = env('JIRA_CLIENT_SECRET')
JIRA_REDIRECT_URI = "https://officially-fast-condor.ngrok-free.app/integrations/callback/jira/"

#datadog information
DATADOG_APP_ID = env('DATADOG_APP_ID')
DATADOG_CLIENT_ID = env('DATADOG_CLIENT_ID')
DATADOG_CLIENT_SECRET = env('DATADOG_CLIENT_SECRET')
DATADOG_REDIRECT_URI = "https://officially-fast-condor.ngrok-free.app/integrations/callback/datadog/"


### This provides all integrations in the integrations app ###
### TODO: Should this be here or in a file in the integrations app? ###
INTEGRATION_SERVICES = [
        {'name': 'QuickBooks', 'connect_url': 'quickbooks_connect', 'logo_url': 'images/integrations_logos/quickbooks_logo.png', 'oauth_base_url': 'https://appcenter.intuit.com/connect/oauth2', "response_type": "code"},
        {'name': 'HubSpot', 'connect_url': 'hubspot_connect', 'logo_url': 'images/integrations_logos/hubspot_logo.svg.png', 'oauth_base_url': 'https://app.hubspot.com/oauth/authorize', "response_type": "code"},
        {'name': 'Stripe', 'connect_url': 'stripe_connect', 'logo_url': 'images/integrations_logos/stripe_logo.svg.png', 'oauth_base_url': 'https://connect.stripe.com/oauth/authorize', "response_type": "code"},
        {'name': 'Jira', 'connect_url': 'jira_connect', 'logo_url': 'images/integrations_logos/jira_logo.svg.png', 'oauth_base_url': 'https://auth.atlassian.com/authorize', "response_type": "code"},
        {'name': 'Datadog', 'connect_url': 'datadog_connect', 'logo_url': 'images/integrations_logos/datadog_logo.png', 'oauth_base_url': 'https://app.datadoghq.com/oauth2/v1/authorize', "response_type": "code"},
        {'name': 'Salesforce', 'connect_url': 'integrations', 'logo_url': 'images/integrations_logos/salesforce_logo.svg.png', 'oauth_base_url': 'https://hostname/services/oauth2/authorize', "response_type": "code"},
        {'name': 'Xero', 'connect_url': 'integrations', 'logo_url': 'images/integrations_logos/xero_logo.com.png', 'oauth_base_url': 'https://login.xero.com/identity/connect/authorize', "response_type": "code"},
        {'name': 'Mailchimp', 'connect_url': 'integrations', 'logo_url': 'images/integrations_logos/mailchimp_logo.png', 'oauth_base_url': 'https://login.mailchimp.com/oauth2/authorize', "response_type": "code"},
        {'name': 'Zoho', 'connect_url': 'integrations', 'logo_url': 'images/integrations_logos/zoho_logo.png', 'oauth_base_url': 'https://accounts.zoho.com/oauth/v2/auth', "response_type": "code"},
        {'name': 'ActiveCampaign', 'connect_url': 'integrations', 'logo_url': 'images/integrations_logos/active_campaign_logo.svg.png', 'oauth_base_url': 'https://api.example.com/oauth2/authorize', "response_type": "code"},
        {'name': 'Freshbooks', 'connect_url': 'integrations', 'logo_url': 'images/integrations_logos/freshbooks_logo.png', 'oauth_base_url': 'https://api.freshbooks.com/auth/oauth/token', "response_type": "code"},
        {'name': 'Sage', 'connect_url': 'integrations', 'logo_url': 'images/integrations_logos/sage_logo.svg.png', 'oauth_base_url': 'https://www.sageone.com/oauth2/auth/central?filter=apiv3.1', "response_type": "code"},
        {'name': 'Monday.com', 'connect_url': 'mondaydotcom_connect', 'logo_url': 'images/integrations_logos/monday.com_logo.svg.png', 'oauth_base_url': 'https://auth.monday.com/oauth2/authorize', "response_type": "code"},
        {'name': 'Pendo', 'connect_url': 'integrations', 'logo_url': 'images/integrations_logos/pendo_logo.png', 'oauth_base_url': 'https://app.pendo.io/api/v1/page', "response_type": "code"},
        {'name': 'BambooHR', 'connect_url': 'integrations', 'logo_url': 'images/integrations_logos/bamboohr_logo.png', 'oauth_base_url': 'https://api.bamboohr.com/api/gateway.php', "response_type": "code"},
        {'name': 'Gusto', 'connect_url': 'integrations', 'logo_url': 'images/integrations_logos/gusto_logo.png', 'oauth_base_url': 'https://api.bamboohr.com/api/gateway.php', "response_type": "code"},
    ]

### This provides all of the information needed for the dashboard pages. ###
### NOTE: Will likely change. ####
### TODO: Should this be included in settings.py or in a seperate file structure in the dashboard app? ###
EXPENSES_CATEGORIES = [
        {'name': 'Total Expenses', 'value': 0, 'growth_rate': 0},
        {'name': 'COGS', 'value': 0, 'growth_rate': 0},
        {'name': 'G&A', 'value': 0, 'growth_rate': 0},
        {'name': 'S&M', 'value': 0, 'growth_rate': 0},
        {'name': 'R&D', 'value': 0, 'growth_rate': 0},
        {'name': 'Payroll', 'value': 0, 'growth_rate': 0},
        {'name': 'Non-Operating Expenses', 'value': 0, 'growth_rate': 0},
        {'name': 'Payroll per FTE', 'value': 0, 'growth_rate': 0},
        {'name': 'Expenses per FTE', 'value': 0, 'growth_rate': 0},
    ]   

REVENUE_CATEGORIES = [
        {'name': 'Total Revenue', 'value': 0, 'growth_rate': 0},
        {'name': 'ARPA', 'value': 0, 'growth_rate': 0},
        {'name': 'Customer Concentration', 'value': 0, 'growth_rate': 0},
        {'name': 'New Customer Revenue', 'value': 0, 'growth_rate': 0},
        {'name': 'Existing Customer Revenue', 'value': 0, 'growth_rate': 0},
        {'name': 'Revenue per Employee', 'value': 0, 'growth_rate': 0},
        {'name': 'Revenue from Lower Figure Product/Service', 'value': 0, 'growth_rate': 0},
        {'name': 'Revenue from Middle Figure Product/Service', 'value': 0, 'growth_rate': 0},
        {'name': 'Revenue from Upper Figure Product/Service', 'value': 0, 'growth_rate': 0},
    ]

FINANCIAL_CATEGORIES = [
        {'name': 'Gross Profit', 'value': 0, 'growth_rate': 0},
        {'name': 'Gross Profit Margin', 'value': 0, 'growth_rate': 0},
        {'name': 'Net Profit', 'value': 0, 'growth_rate': 0},
        {'name': 'Net Profit Margin', 'value': 0, 'growth_rate': 0},
        {'name': 'EBITDA', 'value': 0, 'growth_rate': 0},
        {'name': 'EBITDA Margin', 'value': 0, 'growth_rate': 0},
        {'name': 'Rule of 40', 'value': 0, 'growth_rate': 0},
        {'name': 'Net Working Capital', 'value': 0, 'growth_rate': 0},
        {'name': 'Debt to Equity', 'value': 0, 'growth_rate': 0},
    ]

PIPELINE_CATEGORIES = [
        {'name': 'Conversion Rate', 'value': 0, 'growth_rate': 0},
        {'name': 'Sales Velocity', 'value': 0, 'growth_rate': 0},
        {'name': 'Average Deal Size', 'value': 0, 'growth_rate': 0},
        {'name': 'Weighted Pipeline', 'value': 0, 'growth_rate': 0},
        {'name': 'Prospects', 'value': 0, 'growth_rate': 0},
        {'name': 'Marketing Qualified Leads', 'value': 0, 'growth_rate': 0},
        {'name': 'Sales Qualified Leads', 'value': 0, 'growth_rate': 0},
        {'name': 'Closed-Won', 'value': 0, 'growth_rate': 0},
        {'name': 'Closed-Lost', 'value': 0, 'growth_rate': 0},
    ]

PRODUCT_CATEGORIES = [
        {'name': 'NPS/CSAT', 'value': 0, 'growth_rate': 0},
        {'name': 'Monthly Active Users', 'value': 0, 'growth_rate': 0},
        {'name': 'Site Visits', 'value': 0, 'growth_rate': 0},
        {'name': 'Velocity', 'value': 0, 'growth_rate': 0},
        {'name': 'Burndown Progress', 'value': 0, 'growth_rate': 0},
        {'name': 'R&D Expenses', 'value': 0, 'growth_rate': 0},
        {'name': 'Work in Progress', 'value': 0, 'growth_rate': 0},
        {'name': 'Backlog', 'value': 0, 'growth_rate': 0},
        {'name': 'Lead Time', 'value': 0, 'growth_rate': 0},
    ]

SAAS_METRICS_CATEGORIES = [
        {'name': 'MRR', 'value': 0, 'growth_rate': 0},
        {'name': 'LTV/CAC', 'value': 0, 'growth_rate': 0},
        {'name': 'Revenue Churn Rate', 'value': 0, 'growth_rate': 0},
        {'name': 'Customer Lifetime Value', 'value': 0, 'growth_rate': 0},
        {'name': 'Customer Aquisition Costs', 'value': 0, 'growth_rate': 0},
        {'name': 'CAC Payback (Mos.)', 'value': 0, 'growth_rate': 0},
    ]

SERVICES_CATEGORIES = [
        {'name': 'NPS/CSAT', 'value': 0, 'growth_rate': 0},
        {'name': 'Completed Contracts', 'value': 0, 'growth_rate': 0},
        {'name': 'Contracts in Progress', 'value': 0, 'growth_rate': 0},
        {'name': 'Backlog', 'value': 0, 'growth_rate': 0},
        {'name': 'Employee Utilization', 'value': 0, 'growth_rate': 0},
        {'name': 'Billable Hours', 'value': 0, 'growth_rate': 0},
    ]

CASHFLOW_CATEGORIES = [
        {'name': 'Net Runway (mos.)', 'value': 0, 'growth_rate': 0},
        {'name': 'Gross Runway (mos.)', 'value': 0, 'growth_rate': 0},
        {'name': 'Net Burn Rate', 'value': 0, 'growth_rate': 0},
        {'name': 'Gross Burn Rate', 'value': 0, 'growth_rate': 0},
        {'name': 'Cash Available', 'value': 0, 'growth_rate': 0},
        {'name': 'Quick Ratio', 'value': 0, 'growth_rate': 0},
        {'name': 'AR Days', 'value': 0, 'growth_rate': 0},
        {'name': 'AP Days', 'value': 0, 'growth_rate': 0},
        {'name': 'Inventory Days', 'value': 0, 'growth_rate': 0},
    ]

SUMMARY_CATEGORIES = [
        {'name': 'Revenue', 'value': 0, 'growth_rate': 0},
        {'name': 'Revenue Best Performer', 'value': 0, 'growth_rate': 0},
        {'name': 'Revenue Worst Performer', 'value': 0, 'growth_rate': 0},

        {'name': 'Expenses', 'value': 0, 'growth_rate': 0},
        {'name': 'Expenses Best Performer', 'value': 0, 'growth_rate': 0},
        {'name': 'Expenses Worst Performer', 'value': 0, 'growth_rate': 0},

        {'name': 'Gross Income Margin', 'value': 0, 'growth_rate': 0},
        {'name': 'Financials Best Performer', 'value': 0, 'growth_rate': 0},
        {'name': 'Financials Worst Performer', 'value': 0, 'growth_rate': 0},

        {'name': 'Net Runway (mos.)', 'value': 0, 'growth_rate': 0},
        {'name': 'Cashflow Best Performer', 'value': 0, 'growth_rate': 0},
        {'name': 'Cashflow Worst Performer', 'value': 0, 'growth_rate': 0},

        {'name': 'Conversion Rate', 'value': 0, 'growth_rate': 0},
        {'name': 'Pipeline Best Performer', 'value': 0, 'growth_rate': 0},
        {'name': 'Pipeline Worst Performer', 'value': 0, 'growth_rate': 0},

        {'name': 'Revenue Churn Rate', 'value': 0, 'growth_rate': 0},
        {'name': 'SaaS Metrics Best Performer', 'value': 0, 'growth_rate': 0},
        {'name': 'SaaS Metrics Worst Performer', 'value': 0, 'growth_rate': 0},

        {'name': 'NPS/CSAT', 'value': 0, 'growth_rate': 0},
        {'name': 'Product Development Best Performer', 'value': 0, 'growth_rate': 0},
        {'name': 'Product Worst Performer', 'value': 0, 'growth_rate': 0},

        {'name': 'NPS/CSAT', 'value': 0, 'growth_rate': 0},
        {'name': 'Services Best Performer', 'value': 0, 'growth_rate': 0},
        {'name': 'Services Worst Performer', 'value': 0, 'growth_rate': 0},

        {'name': 'Employee Satisfaction', 'value': 0, 'growth_rate': 0},
        {'name': 'HR Best Performer', 'value': 0, 'growth_rate': 0},
        {'name': 'HR Worst Performer', 'value': 0, 'growth_rate': 0},
]

HR_CATEGORIES = [
        {'name': 'Employee Satisfaction', 'value': 0, 'growth_rate': 0},
        {'name': 'Employee Turnover', 'value': 0, 'growth_rate': 0},
        {'name': 'Payroll as % of Revenue', 'value': 0, 'growth_rate': 0},
        {'name': 'Job Acceptance Rate', 'value': 0, 'growth_rate': 0},
        {'name': 'Open Jobs', 'value': 0, 'growth_rate': 0},
        {'name': 'Fill Time', 'value': 0, 'growth_rate': 0},
        {'name': 'Revenue per FTE', 'value': 0, 'growth_rate': 0},
        {'name': 'Expense per FTE', 'value': 0, 'growth_rate': 0},
        {'name': 'Training Expenses', 'value': 0, 'growth_rate': 0},
    ]