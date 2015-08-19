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
        ('wagtailredirects', '0002_add_verbose_names'),
        ('wagtailimages', '0006_add_verbose_names'),
        ('wagtailsearch', '0002_add_verbose_names'),
        ('taggit', '0001_initial'),
        ('wagtailforms', '0002_add_verbose_names'),
        ('wagtailcore', '0001_squashed_0016_change_page_url_path_to_text_field'),
        ('home', '0003_auto_20150819_1321'),
    ]

    operations = [
        migrations.CreateModel(
            name='ProjectPage',
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
        migrations.RemoveField(
            model_name='project',
            name='image',
        ),
        migrations.RemoveField(
            model_name='project',
            name='page_ptr',
        ),
        migrations.RemoveField(
            model_name='project',
            name='tags',
        ),
        migrations.AlterField(
            model_name='projecttag',
            name='content_object',
            field=modelcluster.fields.ParentalKey(related_name='tagged_items', to='home.ProjectPage'),
        ),
        migrations.DeleteModel(
            name='Project',
        ),
        migrations.AddField(
            model_name='projectpage',
            name='tags',
            field=modelcluster.contrib.taggit.ClusterTaggableManager(to='taggit.Tag', through='home.ProjectTag', blank=True, help_text='A comma-separated list of tags.', verbose_name='Tags'),
        ),
    ]
