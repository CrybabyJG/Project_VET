# Generated by Django 4.2 on 2024-11-15 22:13

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('cita', '0001_initial'),
        ('presentacion', '0001_initial'),
        ('unidad_medida', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Medicamento',
            fields=[
                ('ID_Medicamento', models.AutoField(primary_key=True, serialize=False)),
                ('Codigo_Medicamento', models.CharField(max_length=10, unique=True, verbose_name='Código de medicamento')),
                ('Nombre_Medicamento', models.CharField(max_length=200, verbose_name='Nombre del Medicamento')),
                ('Precio', models.DecimalField(decimal_places=2, max_digits=10, verbose_name='Precio')),
                ('ID_Presentacion', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='presentacion.presentacion', verbose_name='Presentación del medicamento')),
                ('ID_Unidad_Medida', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='unidad_medida.unidadmedida', verbose_name='Unidad de medida')),
            ],
            options={
                'verbose_name_plural': 'Medicamentos',
            },
        ),
        migrations.CreateModel(
            name='DetalleMedicamento',
            fields=[
                ('ID_DetalleEnfermedades', models.AutoField(primary_key=True, serialize=False)),
                ('Cantidad', models.IntegerField(verbose_name='Cantidad')),
                ('Descripcion', models.CharField(max_length=300, verbose_name='Descripcion')),
                ('ID_Cita', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='cita.cita', verbose_name='Cita No.')),
                ('ID_Medicamento', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='detalles', to='medicamento.medicamento', verbose_name='Medicamento')),
            ],
            options={
                'verbose_name_plural': 'Detalles Medicamentos',
            },
        ),
    ]
