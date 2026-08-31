from django.db import migrations

def seed_certificates(apps, schema_editor):
    Certificate = apps.get_model('certificates', 'Certificate')
    # Remove any existing certificates to satisfy "Add ONLY these 4 verified certificates"
    Certificate.objects.all().delete()

    certificates = [
        {
            "name": "GEN AI STUDY JAM 2024 – Basics of Google Cloud Courses",
            "issuer": "Google Developer Groups On Campus – VVIET, Mysore",
            "issue_date": "2024-11-22",
            "credential_url": "/media/certificates/DocScanner 31-Aug-2026 10-47 AM.pdf",
            "description": "October 11, 2024 – November 22, 2024"
        },
        {
            "name": "Generative AI Landscape",
            "issuer": "Infosys Springboard",
            "issue_date": "2025-05-07",
            "credential_url": "/media/certificates/thangi cetificate 1.pdf",
            "description": ""
        },
        {
            "name": "Prompt Engineering",
            "issuer": "Infosys Springboard",
            "issue_date": "2025-05-07",
            "credential_url": "/media/certificates/certificate 2.pdf",
            "description": ""
        },
        {
            "name": "Data Science",
            "issuer": "Infosys Springboard",
            "issue_date": "2026-08-30",
            "credential_url": "/media/certificates/60cce879-321d-4b1a-b44f-56cfc3d8d5ed(1).pdf",
            "description": ""
        }
    ]

    for cert in certificates:
        Certificate.objects.create(**cert)

def unseed_certificates(apps, schema_editor):
    Certificate = apps.get_model('certificates', 'Certificate')
    Certificate.objects.all().delete()

class Migration(migrations.Migration):
    dependencies = [
        ('certificates', '0001_initial'),
    ]

    operations = [
        migrations.RunPython(seed_certificates, unseed_certificates),
    ]
