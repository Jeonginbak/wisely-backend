# Generated by Django 3.0.6 on 2020-05-14 12:00

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='AfterShave',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=20)),
                ('price', models.PositiveIntegerField(default=0)),
            ],
            options={
                'db_table': 'after_shaves',
            },
        ),
        migrations.CreateModel(
            name='Blade',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=20)),
                ('price', models.PositiveIntegerField(default=0)),
                ('image', models.URLField(max_length=2000)),
                ('result_image', models.URLField(max_length=2000)),
            ],
            options={
                'db_table': 'blades',
            },
        ),
        migrations.CreateModel(
            name='Color',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=20)),
                ('code', models.CharField(max_length=10)),
            ],
            options={
                'db_table': 'colors',
            },
        ),
        migrations.CreateModel(
            name='ShavingGel',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=20)),
                ('price', models.PositiveIntegerField(default=0)),
                ('image', models.URLField(max_length=2000)),
                ('result_image', models.URLField(max_length=2000)),
            ],
            options={
                'db_table': 'shaving_gels',
            },
        ),
        migrations.CreateModel(
            name='SkinType',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=30)),
            ],
            options={
                'db_table': 'skin_types',
            },
        ),
        migrations.CreateModel(
            name='RazorSetImage',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('product_image', models.URLField(max_length=2000)),
                ('result_image', models.URLField(max_length=2000)),
                ('color', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='product.Color')),
            ],
            options={
                'db_table': 'razor_set_images',
            },
        ),
        migrations.CreateModel(
            name='RazorSet',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=20)),
                ('price', models.PositiveIntegerField(default=0)),
                ('image', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='product.RazorSetImage')),
            ],
            options={
                'db_table': 'razor_sets',
            },
        ),
        migrations.CreateModel(
            name='RazorImages',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('image_type', models.CharField(max_length=20)),
                ('image', models.URLField(max_length=2000)),
                ('background_image', models.URLField(max_length=2000)),
                ('color', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='product.Color')),
            ],
            options={
                'db_table': 'razor_images',
            },
        ),
        migrations.CreateModel(
            name='GiftSetImage',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('product_image', models.URLField(max_length=2000)),
                ('color', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='product.Color')),
            ],
            options={
                'db_table': 'gift_set_images',
            },
        ),
        migrations.CreateModel(
            name='GiftSet',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=20)),
                ('price', models.PositiveIntegerField(default=0)),
                ('image', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='product.GiftSetImage')),
            ],
            options={
                'db_table': 'gift_sets',
            },
        ),
        migrations.CreateModel(
            name='AfterShaveSkinType',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('image', models.URLField(max_length=2000)),
                ('result_image', models.URLField(max_length=2000)),
                ('after_shave', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='product.AfterShave')),
                ('skin_type', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='product.SkinType')),
            ],
            options={
                'db_table': 'after_shaves_skin_types',
            },
        ),
        migrations.AddField(
            model_name='aftershave',
            name='after_shave_skin_type',
            field=models.ManyToManyField(through='product.AfterShaveSkinType', to='product.SkinType'),
        ),
    ]