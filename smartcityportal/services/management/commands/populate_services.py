from django.core.management.base import BaseCommand
from services.models import ServiceCategory, CityService


class Command(BaseCommand):
    help = 'Populate database with sample service categories and services'

    def handle(self, *args, **kwargs):
        # Clear existing data
        CityService.objects.all().delete()
        ServiceCategory.objects.all().delete()

        # Create categories
        transportation = ServiceCategory.objects.create(
            name='Transportation',
            description='Public transportation and traffic services'
        )
        utilities = ServiceCategory.objects.create(
            name='Utilities',
            description='Water, electricity, and gas services'
        )
        public_safety = ServiceCategory.objects.create(
            name='Public Safety',
            description='Police, fire, and emergency services'
        )
        waste = ServiceCategory.objects.create(
            name='Waste Management',
            description='Garbage collection and recycling services'
        )
        parks = ServiceCategory.objects.create(
            name='Parks & Recreation',
            description='Parks, recreation centers, and community facilities'
        )

        # Create services
        services_data = [
            {
                'category': transportation,
                'name': 'Bus Services',
                'description': 'City-wide bus transportation with multiple routes covering all major areas. Operates from 5 AM to 11 PM daily.',
                'contact_info': 'Phone: 555-0101\nEmail: businfo@smartcity.gov\nWebsite: www.smartcity.gov/bus'
            },
            {
                'category': transportation,
                'name': 'Metro Rail',
                'description': 'Fast and efficient metro rail service connecting downtown to suburbs. Three lines in operation.',
                'contact_info': 'Phone: 555-0102\nEmail: metro@smartcity.gov'
            },
            {
                'category': utilities,
                'name': 'Water Supply',
                'description': 'Clean drinking water supply and maintenance services. 24/7 emergency response available.',
                'contact_info': 'Phone: 555-0201\nEmergency: 555-0299\nEmail: water@smartcity.gov'
            },
            {
                'category': utilities,
                'name': 'Electricity Board',
                'description': 'Electrical supply and maintenance. Report outages and schedule new connections.',
                'contact_info': 'Phone: 555-0202\nEmergency: 555-0298\nEmail: power@smartcity.gov'
            },
            {
                'category': public_safety,
                'name': 'Police Department',
                'description': 'Law enforcement and public safety services. Multiple stations across the city.',
                'contact_info': 'Emergency: 911\nNon-Emergency: 555-0301\nEmail: police@smartcity.gov'
            },
            {
                'category': public_safety,
                'name': 'Fire Department',
                'description': 'Fire emergency response and prevention services. Fire safety inspections available.',
                'contact_info': 'Emergency: 911\nNon-Emergency: 555-0302\nEmail: fire@smartcity.gov'
            },
            {
                'category': waste,
                'name': 'Garbage Collection',
                'description': 'Weekly garbage collection service. Residential pickup on designated days.',
                'contact_info': 'Phone: 555-0401\nEmail: waste@smartcity.gov'
            },
            {
                'category': waste,
                'name': 'Recycling Program',
                'description': 'City-wide recycling program. Collection every two weeks. Drop-off centers available.',
                'contact_info': 'Phone: 555-0402\nEmail: recycle@smartcity.gov'
            },
            {
                'category': parks,
                'name': 'City Parks',
                'description': 'Maintenance and management of city parks and green spaces. Over 50 parks throughout the city.',
                'contact_info': 'Phone: 555-0501\nEmail: parks@smartcity.gov'
            },
            {
                'category': parks,
                'name': 'Recreation Centers',
                'description': 'Community recreation centers offering sports facilities, classes, and events.',
                'contact_info': 'Phone: 555-0502\nEmail: recreation@smartcity.gov'
            },
        ]

        for service_data in services_data:
            CityService.objects.create(**service_data)

        self.stdout.write(self.style.SUCCESS(f'Successfully created {ServiceCategory.objects.count()} categories and {CityService.objects.count()} services'))
