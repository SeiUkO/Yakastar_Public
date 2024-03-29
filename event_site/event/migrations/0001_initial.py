# Generated by Django 3.0.dev20190305154108 on 2019-04-09 18:12

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Assos',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=64)),
                ('president_id', models.IntegerField()),
                ('nb_members', models.IntegerField()),
            ],
        ),
        migrations.CreateModel(
            name='Users',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('status', models.CharField(max_length=64)),
                ('login', models.CharField(max_length=64)),
                ('lastname', models.CharField(max_length=64)),
                ('firstname', models.CharField(max_length=64)),
                ('email', models.CharField(max_length=64)),
                ('promo', models.CharField(max_length=64)),
                ('phone', models.CharField(max_length=64)),
                ('signature', models.CharField(max_length=64)),
            ],
        ),
        migrations.CreateModel(
            name='Event',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=200)),
                ('date_time', models.DateTimeField(verbose_name='date_time')),
                ('end_time', models.TimeField()),
                ('begin_time', models.TimeField()),
                ('recurrence', models.BooleanField(default=False)),
                ('frequence', models.IntegerField()),
                ('until', models.DateField()),
                ('responsible', models.CharField(max_length=64)),
                ('responsible_phone', models.CharField(max_length=64)),
                ('responsible_class', models.CharField(max_length=64)),
                ('nb_days', models.IntegerField()),
                ('tutor_name', models.CharField(max_length=64)),
                ('tutor_phone', models.CharField(max_length=64)),
                ('tutor_job', models.CharField(max_length=64)),
                ('nb_ionis_student', models.IntegerField()),
                ('nb_members', models.IntegerField()),
                ('nb_externs', models.IntegerField()),
                ('description', models.CharField(default='short description', max_length=200)),
                ('civil_liability', models.BooleanField(default=False)),
                ('place', models.CharField(max_length=64)),
                ('rooms', models.CharField(max_length=200)),
                ('material', models.CharField(max_length=200)),
                ('drinks', models.IntegerField()),
                ('comment', models.CharField(default='some text', max_length=200)),
                ('assos', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='event.Assos')),
                ('users', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='event.Users')),
            ],
        ),
        migrations.CreateModel(
            name='Assos_user',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('status', models.CharField(max_length=64)),
                ('assos_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='event.Assos')),
                ('user_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='event.Users')),
            ],
        ),
    ]
