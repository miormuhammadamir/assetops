from django.db import migrations

class Migration(migrations.Migration):
    dependencies = [('operations', '0002_preventive_maintenance')]
    operations = [
        migrations.RenameIndex(
            model_name='workorder',
            old_name='operations__status_33d17f_idx',
            new_name='operations__status_78f3fc_idx',
        ),
    ]
