from smartcityportal.wsgi import application

# Vercel serverless function handler
def handler(event, context):
    """
    Vercel serverless function that wraps Django WSGI app
    """
    return application(event, context)

# Keep app export for compatibility
app = application
