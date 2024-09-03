from django.db import migrations

def create_initial_categories_and_currencies(apps, schema_editor):
    Category = apps.get_model('inventory', 'Category')
    Category.objects.get_or_create(name='Electronics')
    Category.objects.get_or_create(name='Furniture')
    Category.objects.get_or_create(name='Clothing')
    Category.objects.get_or_create(name='Shoes')
    Category.objects.get_or_create(name='Food')
    Category.objects.get_or_create(name='Drinks')

    Currency = apps.get_model('inventory', 'Currency')
    Currency.objects.get_or_create(code='NGN', symbol='₦')
    Currency.objects.get_or_create(code='USD', symbol='$')

class Migration(migrations.Migration):

    dependencies = [
        ('inventory', '0001_initial'),
    ]

    operations = [
        migrations.RunPython(create_initial_categories_and_currencies),
    ]
