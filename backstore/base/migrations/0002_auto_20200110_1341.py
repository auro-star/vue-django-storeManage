# Generated by Django 2.2.5 on 2020-01-10 13:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='area',
            name='area_status',
            field=models.IntegerField(choices=[(0, '停用'), (1, '启用')], default=0, verbose_name='区域状态'),
        ),
        migrations.AlterField(
            model_name='center',
            name='center_status',
            field=models.IntegerField(choices=[(0, '停用'), (1, '启用')], default=0, verbose_name='中心状态'),
        ),
        migrations.AlterField(
            model_name='customer',
            name='customer_status',
            field=models.IntegerField(choices=[(0, '停用'), (1, '启用')], default=0, verbose_name='客户状态'),
        ),
        migrations.AlterField(
            model_name='department',
            name='dpm_status',
            field=models.IntegerField(choices=[(0, '停用'), (1, '启用')], default=0, verbose_name='部门状态'),
        ),
        migrations.AlterField(
            model_name='material',
            name='material_status',
            field=models.IntegerField(choices=[(0, '停用'), (1, '启用')], default=0, verbose_name='物料状态'),
        ),
        migrations.AlterField(
            model_name='materialtype',
            name='type_status',
            field=models.IntegerField(choices=[(0, '停用'), (1, '启用')], default=0, verbose_name='物料类别状态'),
        ),
        migrations.AlterField(
            model_name='meterage',
            name='meterage_status',
            field=models.IntegerField(choices=[(0, '停用'), (1, '启用')], default=0, verbose_name='计量单位状态'),
        ),
        migrations.AlterField(
            model_name='organization',
            name='orga_status',
            field=models.IntegerField(choices=[(0, '停用'), (1, '启用')], default=0, verbose_name='组织状态'),
        ),
        migrations.AlterField(
            model_name='role',
            name='role_status',
            field=models.IntegerField(choices=[(0, '停用'), (1, '启用')], default=0, verbose_name='角色状态'),
        ),
        migrations.AlterField(
            model_name='supplier',
            name='supply_status',
            field=models.IntegerField(choices=[(0, '停用'), (1, '启用')], default=0, verbose_name='供应商状态'),
        ),
    ]