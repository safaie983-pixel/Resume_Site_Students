from django.db import migrations
import random
import string

def gen_code():
    return ''.join(random.choices(string.ascii_uppercase + string.digits, k=8))

def populate_codes(apps, schema_editor):
    Order = apps.get_model('accounts', 'Order')
    for order in Order.objects.all():
        order.tracking_code = gen_code()
        order.save()

class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0012_alter_certificate_options_alter_customlink_options_and_more'),
    ]

    operations = [
        migrations.RunPython(populate_codes),
    ]