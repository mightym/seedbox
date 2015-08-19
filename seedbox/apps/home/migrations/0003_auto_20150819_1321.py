# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import wagtail.wagtailcore.fields
import modelcluster.fields
import wagtail.wagtailimages.blocks
import django.db.models.deletion
import wagtail.wagtailcore.blocks
import modelcluster.contrib.taggit


class Migration(migrations.Migration):

    dependencies = [
        ('taggit', '0001_initial'),
        ('wagtailimages', '0006_add_verbose_names'),
        ('wagtailcore', '0001_squashed_0016_change_page_url_path_to_text_field'),
        ('home', '0002_create_homepage'),
    ]

    operations = [
        migrations.CreateModel(
            name='Project',
            fields=[
                ('page_ptr', models.OneToOneField(parent_link=True, auto_created=True, primary_key=True, serialize=False, to='wagtailcore.Page')),
                ('body', wagtail.wagtailcore.fields.RichTextField(blank=True)),
                ('hsize', models.CharField(default='columns1', max_length=10, verbose_name='Columns', choices=[('columns1', 'columns-1'), ('columns2', 'columns-2'), ('columns4', 'columns-4')])),
                ('content', wagtail.wagtailcore.fields.StreamField([('section', wagtail.wagtailcore.blocks.StructBlock([(b'title', wagtail.wagtailcore.blocks.CharBlock(required=True)), (b'bgimage', wagtail.wagtailimages.blocks.ImageChooserBlock()), (b'bgimage_width', wagtail.wagtailcore.blocks.CharBlock(default='2048', required=True)), (b'height', wagtail.wagtailcore.blocks.CharBlock(default='fullscreen', required=True)), (b'css', wagtail.wagtailcore.blocks.TextBlock(required=False)), (b'assets', wagtail.wagtailcore.blocks.ListBlock(wagtail.wagtailcore.blocks.StructBlock([('image', wagtail.wagtailimages.blocks.ImageChooserBlock()), ('css', wagtail.wagtailcore.blocks.TextBlock(required=False))])))]))])),
                ('image', models.ForeignKey(related_name='+', on_delete=django.db.models.deletion.SET_NULL, blank=True, to='wagtailimages.Image', null=True)),
            ],
            options={
                'abstract': False,
            },
            bases=('wagtailcore.page',),
        ),
        migrations.CreateModel(
            name='ProjectTag',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('content_object', modelcluster.fields.ParentalKey(related_name='tagged_items', to='home.Project')),
                ('tag', models.ForeignKey(related_name='home_projecttag_items', to='taggit.Tag')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.AddField(
            model_name='homepage',
            name='description',
            field=models.CharField(max_length=500, null=True, verbose_name='Page Description', blank=True),
        ),
        migrations.AddField(
            model_name='project',
            name='tags',
            field=modelcluster.contrib.taggit.ClusterTaggableManager(to='taggit.Tag', through='home.ProjectTag', blank=True, help_text='A comma-separated list of tags.', verbose_name='Tags'),
        ),
    ]
