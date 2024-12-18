# Generated by Django 4.2 on 2024-11-15 22:13

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('estado_venta', '0001_initial'),
        ('clientes', '0001_initial'),
        ('medicamento', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Venta',
            fields=[
                ('ID_Venta', models.AutoField(primary_key=True, serialize=False)),
                ('Codigo_Venta', models.CharField(max_length=10, unique=True, verbose_name='Código de venta')),
                ('Descripcion', models.CharField(max_length=200, verbose_name='Descripción')),
                ('Fecha', models.DateField(auto_now_add=True, verbose_name='Fecha')),
                ('ID_Cliente', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='clientes.clientes', verbose_name='Cliente')),
                ('ID_EstadoVenta', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='estado_venta.estadodeventa', verbose_name='Estado de la venta')),
            ],
            options={
                'verbose_name_plural': 'Ventas',
            },
        ),
        migrations.CreateModel(
            name='DetalleVenta',
            fields=[
                ('ID_DetalleVenta', models.AutoField(primary_key=True, serialize=False)),
                ('Cantidad', models.IntegerField(verbose_name='Cantidad')),
                ('Precio', models.DecimalField(decimal_places=2, max_digits=10, verbose_name='Precio')),
                ('ID_Medicamento', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='medicamento.medicamento', verbose_name='Medicamento')),
                ('ID_Venta', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='detalles', to='venta.venta')),
            ],
            options={
                'verbose_name_plural': 'Detalles de ventas',
            },
        ),
    ]
