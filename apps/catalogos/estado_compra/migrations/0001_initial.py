# Generated by Django 4.2 on 2024-11-15 22:13

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='EstadodeCompra',
            fields=[
                ('ID_EstadoCompra', models.AutoField(primary_key=True, serialize=False)),
                ('Codigo_EstadoCompra', models.CharField(max_length=10, verbose_name='Código de estado de compra')),
                ('Estado_Compra', models.CharField(max_length=200, verbose_name='Estado de compra')),
            ],
            options={
                'verbose_name_plural': 'Estados de compras',
            },
        ),
    ]