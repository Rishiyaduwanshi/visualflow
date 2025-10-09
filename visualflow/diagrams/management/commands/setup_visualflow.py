"""
Management command to setup initial data and templates
"""

from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from diagrams.models import DiagramTemplate
from config.constants import AppConstants


class Command(BaseCommand):
    help = 'Setup initial data and templates for VisualFlow'

    def add_arguments(self, parser):
        parser.add_argument(
            '--create-admin',
            action='store_true',
            help='Create admin user (admin/admin123)',
        )

    def handle(self, *args, **options):
        self.stdout.write(self.style.SUCCESS('Setting up VisualFlow...'))

        # Create admin user if requested
        if options['create_admin']:
            self.create_admin_user()

        # Create diagram templates
        self.create_diagram_templates()

        self.stdout.write(self.style.SUCCESS('Setup completed successfully!'))

    def create_admin_user(self):
        """Create admin user for development"""
        if not User.objects.filter(username='admin').exists():
            User.objects.create_superuser(
                username='admin',
                email='admin@visualflow.com',
                password='admin123'
            )
            self.stdout.write(self.style.SUCCESS('Admin user created (admin/admin123)'))
        else:
            self.stdout.write(self.style.WARNING('Admin user already exists'))

    def create_diagram_templates(self):
        """Create default diagram templates"""
        templates = [
            {
                'name': 'E-commerce System',
                'diagram_type': 'uml',
                'template_prompt': 'Create a UML class diagram for an e-commerce system with User, Product, Order, ShoppingCart, and Payment classes',
                'sample_uml': '''@startuml
class User {
  +id: int
  +username: string
  +email: string
  +password: string
  +login()
  +logout()
}

class Product {
  +id: int
  +name: string
  +price: decimal
  +description: string
  +stock: int
}

class Order {
  +id: int
  +orderDate: date
  +status: string
  +total: decimal
  +placeOrder()
  +cancelOrder()
}

class ShoppingCart {
  +id: int
  +addProduct()
  +removeProduct()
  +getTotal()
}

User ||--o{ Order
User ||--|| ShoppingCart
Order }o--o{ Product
ShoppingCart }o--o{ Product
@enduml''',
                'description': 'Basic e-commerce system with user, product, and order management'
            },
            {
                'name': 'Library Management',
                'diagram_type': 'erd',
                'template_prompt': 'Create an ERD for a library management system with Book, Author, Member, and Loan entities',
                'sample_uml': '''@startuml
!define table(x) class x << (T,#FFAAAA) >>
!define primary_key(x) <u>x</u>
!define foreign_key(x) <i>x</i>

table(Book) {
  primary_key(book_id): int
  title: varchar(255)
  isbn: varchar(13)
  publication_year: int
  foreign_key(author_id): int
}

table(Author) {
  primary_key(author_id): int
  first_name: varchar(100)
  last_name: varchar(100)
  birth_date: date
}

table(Member) {
  primary_key(member_id): int
  first_name: varchar(100)
  last_name: varchar(100)
  email: varchar(255)
  join_date: date
}

table(Loan) {
  primary_key(loan_id): int
  foreign_key(book_id): int
  foreign_key(member_id): int
  loan_date: date
  due_date: date
  return_date: date
}

Author ||--o{ Book
Member ||--o{ Loan
Book ||--o{ Loan
@enduml''',
                'description': 'Library system with books, authors, members, and loans'
            },
            {
                'name': 'User Authentication Flow',
                'diagram_type': 'flowchart',
                'template_prompt': 'Create a flowchart for user authentication process with validation and error handling',
                'sample_uml': '''@startuml
start
:User enters credentials;
:Validate input format;
if (Valid format?) then (yes)
  :Check credentials in database;
  if (Credentials valid?) then (yes)
    if (Account active?) then (yes)
      :Generate session token;
      :Redirect to dashboard;
      stop
    else (no)
      :Show "Account disabled" error;
      stop
    endif
  else (no)
    :Show "Invalid credentials" error;
    stop
  endif
else (no)
  :Show "Invalid format" error;
  stop
endif
@enduml''',
                'description': 'Complete user authentication flow with validation'
            },
            {
                'name': 'Chat Application Architecture',
                'diagram_type': 'system_design',
                'template_prompt': 'Design system architecture for a real-time chat application with microservices',
                'sample_uml': '''@startuml
!define RECTANGLE class

RECTANGLE "Web Client" as web {
  React.js Frontend
}

RECTANGLE "Mobile App" as mobile {
  React Native
}

RECTANGLE "API Gateway" as gateway {
  Authentication
  Rate Limiting
  Routing
}

RECTANGLE "User Service" as user {
  User Management
  Authentication
  Profiles
}

RECTANGLE "Chat Service" as chat {
  Message Handling
  Room Management
  WebSocket Connections
}

RECTANGLE "Notification Service" as notify {
  Push Notifications
  Email Notifications
}

RECTANGLE "Message Queue" as queue {
  Redis/RabbitMQ
}

RECTANGLE "Database" as db {
  PostgreSQL
  User Data
  Messages
}

RECTANGLE "File Storage" as storage {
  AWS S3
  Media Files
}

web --> gateway
mobile --> gateway
gateway --> user
gateway --> chat
chat --> queue
chat --> db
chat --> storage
queue --> notify
user --> db
notify --> queue
@enduml''',
                'description': 'Microservices architecture for real-time chat application'
            }
        ]

        created_count = 0
        for template_data in templates:
            template, created = DiagramTemplate.objects.get_or_create(
                name=template_data['name'],
                diagram_type=template_data['diagram_type'],
                defaults=template_data
            )
            if created:
                created_count += 1

        if created_count > 0:
            self.stdout.write(
                self.style.SUCCESS(f'Created {created_count} diagram templates')
            )
        else:
            self.stdout.write(
                self.style.WARNING('All templates already exist')
            )