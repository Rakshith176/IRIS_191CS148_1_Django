# Generated by Django 3.0.8 on 2020-10-20 14:04

from django.db import migrations
import isbn_field.fields
import isbn_field.validators


class Migration(migrations.Migration):

    dependencies = [
        ('Lib', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='book',
            name='isbn',
            field=isbn_field.fields.ISBNField(clean_isbn=False, max_length=28, unique=True, validators=[isbn_field.validators.ISBNValidator], verbose_name='ISBN'),
        ),
    ]
