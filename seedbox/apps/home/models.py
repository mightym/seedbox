from __future__ import unicode_literals

from django.db import models
from django.utils.translation import gettext_lazy as _

from wagtail.wagtailcore.models import Page
from wagtail.wagtailcore.fields import StreamField
from wagtail.wagtailcore import blocks
from wagtail.wagtailcore.fields import RichTextField
from wagtail.wagtailimages.blocks import ImageChooserBlock
from wagtail.wagtailimages.edit_handlers import ImageChooserPanel
from wagtail.wagtailadmin.edit_handlers import FieldPanel, StreamFieldPanel


from modelcluster.fields import ParentalKey
from modelcluster.tags import ClusterTaggableManager
from taggit.models import TaggedItemBase
from model_utils import Choices


class ProjectBlock(blocks.StructBlock):

    title = blocks.CharBlock(required=True)
    bgimage = ImageChooserBlock()
    bgimage_width = blocks.CharBlock(required=True, default='2048')
    height = blocks.CharBlock(required=True, default='fullscreen')
    css = blocks.TextBlock(required=False)

    assets = blocks.ListBlock(blocks.StructBlock([
        ('image', ImageChooserBlock()),
        ('css', blocks.TextBlock(required=False)),
    ]))

    class Meta:
        icon = 'cogs'
        form_classname = 'project-block'
        template = 'home/blocks/section.html'

    def vsize_display(self):
        return self.VSIZE[self.vsize]

    def hsize_display(self):
        return self.HSIZE[self.hsize]


class HomePage(Page):
    description = models.CharField(_('Page Description'), max_length=500, null=True, blank=True)
    subpage_types = ['ProjectPage']

    @property
    def projects(self):
        # Get list of live project pages that are descendants of this page
        projects = ProjectPage.objects.live().descendant_of(self)
        return projects

HomePage.content_panels = [
    FieldPanel('description'),
]


class ProjectTag(TaggedItemBase):
    content_object = ParentalKey('ProjectPage', related_name='tagged_items')


class ProjectPage(Page):
    subpage_types = []
    HSIZE = Choices(
        ('columns1', _('columns-1')),
        ('columns2', _('columns-2')),
        ('columns4', _('columns-4')),
    )
    body = RichTextField(blank=True)
    previewimage = models.ForeignKey(
        'wagtailimages.Image',
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='+'
    )
    hsize = models.CharField(_('Columns'), max_length=10, choices=HSIZE, default=HSIZE.columns1)
    tags = ClusterTaggableManager(through=ProjectTag, blank=True)
    search_name = "ProjectPage"
    content = StreamField([
        ('section', ProjectBlock())
    ])

    def hsize_display(self):
        return self.HSIZE[self.hsize]

    def get_parent_slug(self):
        return self.get_ancestors().reverse()[0].slug


ProjectPage.content_panels = [
    FieldPanel('title', classname="full title"),
    FieldPanel('body', classname="full"),
    ImageChooserPanel('previewimage'),
    FieldPanel('hsize', classname="hsize"),
    FieldPanel('tags', classname="collapsible collapsed"),
    StreamFieldPanel('content'),
]
