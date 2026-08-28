from rest_framework.views import APIView
from rest_framework.response import Response
from django.db import connection

class HealthCheckView(APIView):
    """
    Endpoint for monitoring API and database health.
    """
    def get(self, request):
        db_status = "ok"
        try:
            with connection.cursor() as cursor:
                cursor.execute("SELECT 1")
                row = cursor.fetchone()
                if row[0] != 1:
                    db_status = "error"
        except Exception:
            db_status = "error"
            
        return Response({
            "status": "ok",
            "database": db_status
        })
