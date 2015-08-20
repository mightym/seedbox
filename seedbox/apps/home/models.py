from __future__ import unicode_literals

from django.db import models
from django.utils.translation import gettext_lazy as _

from wagtail.wagtailcore.models import Page
from wagtail.wagtailcore.fields import StreamField
from wagtail.wagtailcore import blocks
from wagtail.wagtailcore.fields import RichTextField
from wagtail.wagtailimages.blocks import ImageChooserBlock
from wagtail.wagtailembeds.blocks import EmbedBlock
from wagtail.wagtailimages.edit_handlers import ImageChooserPanel
from wagtail.wagtailadmin.edit_handlers import FieldPanel, StreamFieldPanel


from modelcluster.fields import ParentalKey
from modelcluster.tags import ClusterTaggableManager
from taggit.models import TaggedItemBase
from model_utils import Choices


class ProjectHeaderBlock(blocks.StructBlock):
    title = blocks.CharBlock(required=False)
    bgimage = ImageChooserBlock()

    class Meta:
        icon = 'cogs'
        form_classname = 'project-block'
        template = 'home/blocks/project_header.html'


class ProjectEmbedBlock(blocks.StructBlock):
    title = EmbedBlock(required=False)
    bgimage = ImageChooserBlock()

    class Meta:
        icon = 'cogs'
        form_classname = 'embed-block'
        template = 'home/blocks/project_embed.html'



class HomePage(Page):
    description = models.CharField(_('Page Description'), max_length=500, null=True, blank=True)
    subpage_types = ['ProjectPage', 'IntroPage', ]

    @property
    def projects(self):
        # Get list of live project pages that are descendants of this page
        projects = ProjectPage.objects.live().descendant_of(self).order_by('?')
        return projects

HomePage.content_panels = [
    FieldPanel('title'),
    FieldPanel('description'),
]

class IntroPage(Page):
    description = models.CharField(_('Page Description'), max_length=500, null=True, blank=True)
    subpage_types = []

IntroPage.content_panels = [
    FieldPanel('title'),
    FieldPanel('description'),
]


class ProjectTag(TaggedItemBase):
    content_object = ParentalKey('ProjectPage', related_name='tagged_items')


class ProjectPage(Page):
    subpage_types = []
    HSIZE = Choices(
        ('columns1', _('columns-1')),
        ('columns2', _('columns-2')),
        ('columns3', _('columns-3')),
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
        ('project_header', ProjectHeaderBlock()),
        ('project_embed', ProjectEmbedBlock()),
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
