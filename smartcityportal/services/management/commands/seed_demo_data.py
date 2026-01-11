from django.core.management.base import BaseCommand
from django.db import transaction
from services.models import ServiceCategory, CityService
from issues.models import IssueCategory

SERVICE_CATEGORIES = {
    "Transport": "Public transport and mobility support.",
    "Utilities": "Water, electricity, streetlights and essential utilities.",
    "Public Safety": "Emergency services and citizen safety support.",
    "Health": "Hospitals, ambulance, public health services.",
    "Education": "Libraries and education-related services.",
    "Waste & Sanitation": "Garbage, sanitation, drainage services.",
    "Municipal Services": "Citizen services, certificates, tax and civic admin.",
}

ISSUE_CATEGORIES = [
    "Road Damage",
    "Water Leakage",
    "Streetlight Not Working",
    "Waste Overflow",
    "Drainage Blockage",
    "Public Safety",
    "Electricity Issue",
    "Traffic Congestion",
    "Noise Pollution",
    "Illegal Construction",
    "Tree Cutting",
    "Animal Menace",
    "Other",
]

SERVICES_DATA = {
    "Transport": [
        {
            "name": "Railway Enquiry (General)",
            "description": "Train schedule enquiry, platform info, and station guidance.",
            "contact_info": "Dial: 139 | Helpdesk: railway@smartcityportal.local"
        },
        {
            "name": "Railway Station Help Desk",
            "description": "Assistance for passengers, lost & found guidance, station facilities.",
            "contact_info": "Phone: 139"
        },
        {
            "name": "IRCTC Ticket Support (Guidance)",
            "description": "Help for booking issues, cancellation guidance, and travel info (guidance only).",
            "contact_info": "Support: irctc-help@smartcityportal.local"
        },
        {
            "name": "Airport Help Desk",
            "description": "Flight info, terminal guidance, lost & found assistance.",
            "contact_info": "Phone: 1800-222-333 | Email: airport@smartcityportal.local"
        },
        {
            "name": "Airline Customer Support (Guidance)",
            "description": "General guidance for flight rescheduling and baggage queries.",
            "contact_info": "Email: airline-help@smartcityportal.local"
        },
        {
            "name": "Bus Depot / RTC Enquiry",
            "description": "Bus routes, timings, and ticketing support.",
            "contact_info": "Phone: 1800-444-555"
        },
        {
            "name": "Metro Services",
            "description": "Metro route info, smart card recharge guidance, station assistance.",
            "contact_info": "Phone: 1800-666-777"
        },
        {
            "name": "Auto/Taxi Stand Info",
            "description": "Guidance on designated pick-up points and fare complaints routing.",
            "contact_info": "Phone: 1800-101-202"
        },
    ],
    "Utilities": [
        {
            "name": "Electricity Complaint Center",
            "description": "Report power outage, meter issues, and billing disputes.",
            "contact_info": "Dial: 1912"
        },
        {
            "name": "Water Supply Office",
            "description": "Water supply complaints, new connection guidance, billing queries.",
            "contact_info": "Phone: 1800-123-456"
        },
        {
            "name": "Street Light Maintenance",
            "description": "Report streetlights not working, flickering, damaged poles.",
            "contact_info": "Phone: 1800-333-121"
        },
        {
            "name": "Drainage & Sewer Helpline",
            "description": "Report blocked drains, overflow, stagnant water issues.",
            "contact_info": "Phone: 1800-777-141"
        },
        {
            "name": "Gas Pipeline Emergency (Guidance)",
            "description": "Gas leakage guidance and emergency contact routing.",
            "contact_info": "Emergency: 1906"
        },
    ],
    "Public Safety": [
        {
            "name": "Police Emergency",
            "description": "Emergency police assistance.",
            "contact_info": "Dial: 100"
        },
        {
            "name": "Women Safety Helpline",
            "description": "Women safety support and emergency reporting.",
            "contact_info": "Dial: 1091"
        },
        {
            "name": "Cyber Crime Helpline (Guidance)",
            "description": "Report cyber fraud and online scams (guidance).",
            "contact_info": "Dial: 1930"
        },
        {
            "name": "Fire & Emergency",
            "description": "Fire emergencies and rescue operations.",
            "contact_info": "Dial: 101"
        },
        {
            "name": "Disaster Management Helpline",
            "description": "Flood/storm alerts and emergency guidance.",
            "contact_info": "Phone: 1077"
        },
    ],
    "Health": [
        {
            "name": "Ambulance Service",
            "description": "Emergency ambulance dispatch.",
            "contact_info": "Dial: 108"
        },
        {
            "name": "Government Hospital Helpdesk",
            "description": "OPD timings, emergency ward guidance, appointments.",
            "contact_info": "Phone: 1800-888-999"
        },
        {
            "name": "Blood Bank Enquiry (Guidance)",
            "description": "Blood availability enquiry and donation guidance.",
            "contact_info": "Phone: 104"
        },
    ],
    "Education": [
        {
            "name": "Public Library",
            "description": "Membership, reading rooms, book lending and digital access.",
            "contact_info": "Phone: 1800-111-222"
        },
        {
            "name": "Public Examination Helpdesk (Guidance)",
            "description": "General guidance for exam forms, certificates and queries.",
            "contact_info": "Email: exams@smartcityportal.local"
        },
    ],
    "Waste & Sanitation": [
        {
            "name": "Garbage Collection",
            "description": "Missed pickup complaints and schedule guidance.",
            "contact_info": "Phone: 1800-555-131"
        },
        {
            "name": "Waste Overflow Reporting",
            "description": "Report illegal dumping and overflow at public bins.",
            "contact_info": "Phone: 1800-555-131"
        },
        {
            "name": "Public Toilet Maintenance",
            "description": "Report unclean public toilets and maintenance needs.",
            "contact_info": "Phone: 1800-909-808"
        },
    ],
    "Municipal Services": [
        {
            "name": "Citizen Service Center",
            "description": "General help for civic services and guidance.",
            "contact_info": "Phone: 1800-000-161"
        },
        {
            "name": "Property Tax Helpdesk",
            "description": "Property tax payment, receipts, corrections, and help.",
            "contact_info": "Phone: 1800-222-171"
        },
        {
            "name": "Birth/Death Certificate Helpdesk (Guidance)",
            "description": "Guidance for applying and tracking certificates.",
            "contact_info": "Email: certificates@smartcityportal.local"
        },
        {
            "name": "Road Maintenance Office",
            "description": "Report major road damage and maintenance requests routing.",
            "contact_info": "Phone: 1800-700-700"
        },
        {
            "name": "Parks & Recreation Office",
            "description": "Park timings, maintenance issues, public facility complaints.",
            "contact_info": "Phone: 1800-999-151"
        },
    ],
}

class Command(BaseCommand):
    help = "Seeds demo data for categories and services. Uses get_or_create to preserve existing records."

    @transaction.atomic
    def handle(self, *args, **options):
        categories_created = 0
        categories_skipped = 0
        services_created = 0
        services_skipped = 0
        issues_created = 0
        issues_skipped = 0

        self.stdout.write(self.style.WARNING("Starting demo data seeding (get_or_create mode)..."))
        self.stdout.write("")

        # Service Categories
        self.stdout.write("Processing Service Categories...")
        for name, description in SERVICE_CATEGORIES.items():
            obj, created = ServiceCategory.objects.get_or_create(
                name=name,
                defaults={"description": description}
            )
            if created:
                categories_created += 1
                self.stdout.write(self.style.SUCCESS(f"  ✓ Created: {name}"))
            else:
                categories_skipped += 1
                self.stdout.write(f"  - Skipped (exists): {name}")

        self.stdout.write("")

        # City Services
        self.stdout.write("Processing City Services...")
        for cat_name, services in SERVICES_DATA.items():
            try:
                category = ServiceCategory.objects.get(name=cat_name)
            except ServiceCategory.DoesNotExist:
                self.stdout.write(
                    self.style.ERROR(f"  ✗ Category not found: {cat_name}. Skipping its services.")
                )
                continue

            for svc in services:
                obj, created = CityService.objects.get_or_create(
                    category=category,
                    name=svc["name"],
                    defaults={
                        "description": svc["description"],
                        "contact_info": svc["contact_info"],
                    }
                )
                if created:
                    services_created += 1
                    self.stdout.write(self.style.SUCCESS(f"  ✓ Created: {svc['name']}"))
                else:
                    services_skipped += 1
                    self.stdout.write(f"  - Skipped (exists): {svc['name']}")

        self.stdout.write("")

        # Issue Categories
        self.stdout.write("Processing Issue Categories...")
        for name in ISSUE_CATEGORIES:
            obj, created = IssueCategory.objects.get_or_create(
                name=name,
                defaults={"description": f"Issues related to {name.lower()}."}
            )
            if created:
                issues_created += 1
                self.stdout.write(self.style.SUCCESS(f"  ✓ Created: {name}"))
            else:
                issues_skipped += 1
                self.stdout.write(f"  - Skipped (exists): {name}")

        self.stdout.write("")
        self.stdout.write(self.style.SUCCESS("=" * 70))
        self.stdout.write(self.style.SUCCESS("SEEDING SUMMARY"))
        self.stdout.write(self.style.SUCCESS("=" * 70))
        self.stdout.write(
            self.style.SUCCESS(
                f"Service Categories  - Created: {categories_created:>3} | Skipped: {categories_skipped:>3}"
            )
        )
        self.stdout.write(
            self.style.SUCCESS(
                f"City Services       - Created: {services_created:>3} | Skipped: {services_skipped:>3}"
            )
        )
        self.stdout.write(
            self.style.SUCCESS(
                f"Issue Categories    - Created: {issues_created:>3} | Skipped: {issues_skipped:>3}"
            )
        )
        self.stdout.write(self.style.SUCCESS("=" * 70))
        self.stdout.write(
            self.style.SUCCESS(
                f"\nTotal Services in Database: {CityService.objects.count()}"
            )
        )
        self.stdout.write(
            self.style.SUCCESS(
                f"Total Categories in Database: {ServiceCategory.objects.count()}"
            )
        )
        self.stdout.write("")
        self.stdout.write(self.style.SUCCESS("✓ Seeding completed successfully!"))
