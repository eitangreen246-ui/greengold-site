"""Reusable StreamField blocks for editable page sections.

Each block has a matching template in templates/blocks/. Editors compose pages
from these in the Wagtail admin — no code deploys needed to change content.
"""
from wagtail import blocks
from wagtail.images.blocks import ImageChooserBlock

ICON_CHOICES = [
    ("microscope", "Microscope"),
    ("flask", "Flask"),
    ("link", "Link / bridge"),
    ("leaf", "Leaf"),
    ("globe", "Globe"),
    ("shield", "Shield / integrity"),
    ("handshake", "Handshake"),
    ("sparkles", "Sparkles"),
    ("layers", "Layers"),
    ("droplet", "Droplet"),
    ("target", "Target"),
    ("atom", "Atom"),
]


class CTAValue(blocks.StructBlock):
    label = blocks.CharBlock(required=True, max_length=60)
    page = blocks.PageChooserBlock(required=False)
    url = blocks.CharBlock(required=False, help_text="External/explicit URL (used if no page is set).")
    style = blocks.ChoiceBlock(
        choices=[("primary", "Primary (green)"), ("gold", "Gold"), ("outline", "Outline")],
        default="primary",
    )

    class Meta:
        icon = "link"
        label = "Button"


class StatBlock(blocks.StructBlock):
    value = blocks.CharBlock(max_length=20, help_text="e.g. 40+, 2, Global")
    label = blocks.CharBlock(max_length=80)

    class Meta:
        icon = "list-ul"


class StatsBlock(blocks.StructBlock):
    heading = blocks.CharBlock(required=False, max_length=120)
    stats = blocks.ListBlock(StatBlock, min_num=1)

    class Meta:
        icon = "list-ul"
        label = "Stats band"
        template = "blocks/stats_block.html"


class FeatureBlock(blocks.StructBlock):
    icon = blocks.ChoiceBlock(choices=ICON_CHOICES, required=False)
    title = blocks.CharBlock(max_length=120)
    text = blocks.TextBlock(required=False)

    class Meta:
        icon = "pick"


class FeatureGridBlock(blocks.StructBlock):
    eyebrow = blocks.CharBlock(required=False, max_length=60)
    heading = blocks.CharBlock(required=False, max_length=160)
    intro = blocks.TextBlock(required=False)
    columns = blocks.ChoiceBlock(choices=[("2", "2"), ("3", "3")], default="3")
    features = blocks.ListBlock(FeatureBlock, min_num=1)

    class Meta:
        icon = "grip"
        label = "Feature grid"
        template = "blocks/feature_grid_block.html"


class ProcessStepBlock(blocks.StructBlock):
    title = blocks.CharBlock(max_length=120)
    text = blocks.TextBlock(required=False)

    class Meta:
        icon = "order"


class ProcessBlock(blocks.StructBlock):
    eyebrow = blocks.CharBlock(required=False, max_length=60)
    heading = blocks.CharBlock(required=False, max_length=160)
    steps = blocks.ListBlock(ProcessStepBlock, min_num=1)

    class Meta:
        icon = "order"
        label = "Process steps"
        template = "blocks/process_block.html"


class MetricBlock(blocks.StructBlock):
    value = blocks.CharBlock(max_length=24)
    label = blocks.CharBlock(max_length=80)

    class Meta:
        icon = "list-ul"


class CaseStudyBlock(blocks.StructBlock):
    name = blocks.CharBlock(max_length=120, help_text="e.g. FollicleX™")
    tagline = blocks.CharBlock(required=False, max_length=160)
    description = blocks.RichTextBlock(features=["bold", "italic", "link"], required=False)
    metrics = blocks.ListBlock(MetricBlock, required=False)

    class Meta:
        icon = "doc-full"


class CaseStudiesBlock(blocks.StructBlock):
    eyebrow = blocks.CharBlock(required=False, max_length=60)
    heading = blocks.CharBlock(required=False, max_length=160)
    intro = blocks.TextBlock(required=False)
    items = blocks.ListBlock(CaseStudyBlock, min_num=1)

    class Meta:
        icon = "doc-full"
        label = "Case studies"
        template = "blocks/case_studies_block.html"


class ValueBlock(blocks.StructBlock):
    icon = blocks.ChoiceBlock(choices=ICON_CHOICES, required=False)
    title = blocks.CharBlock(max_length=120)
    text = blocks.TextBlock(required=False)
    tag = blocks.CharBlock(required=False, max_length=60)

    class Meta:
        icon = "pick"


class ValuesBlock(blocks.StructBlock):
    eyebrow = blocks.CharBlock(required=False, max_length=60)
    heading = blocks.CharBlock(required=False, max_length=160)
    values = blocks.ListBlock(ValueBlock, min_num=1)

    class Meta:
        icon = "list-ul"
        label = "Values grid"
        template = "blocks/values_block.html"


class IngredientCategoryBlock(blocks.StructBlock):
    icon = blocks.ChoiceBlock(choices=ICON_CHOICES, required=False)
    name = blocks.CharBlock(max_length=140)
    description = blocks.TextBlock(required=False)
    applications = blocks.CharBlock(required=False, max_length=240, help_text="Comma-separated applications.")
    evidence = blocks.CharBlock(required=False, max_length=240, help_text="Clinical / scientific evidence summary.")
    regulatory = blocks.CharBlock(required=False, max_length=240, help_text="Regulatory status.")

    class Meta:
        icon = "leaf"


class IngredientsBlock(blocks.StructBlock):
    eyebrow = blocks.CharBlock(required=False, max_length=60)
    heading = blocks.CharBlock(required=False, max_length=160)
    intro = blocks.TextBlock(required=False)
    categories = blocks.ListBlock(IngredientCategoryBlock, min_num=1)

    class Meta:
        icon = "leaf"
        label = "Ingredient categories"
        template = "blocks/ingredients_block.html"


class RichTextSectionBlock(blocks.StructBlock):
    eyebrow = blocks.CharBlock(required=False, max_length=60)
    heading = blocks.CharBlock(required=False, max_length=160)
    body = blocks.RichTextBlock(features=["h2", "h3", "bold", "italic", "link", "ul", "ol"])

    class Meta:
        icon = "doc-full"
        label = "Rich text section"
        template = "blocks/richtext_section_block.html"


class ImageBlock(blocks.StructBlock):
    image = ImageChooserBlock()
    caption = blocks.CharBlock(required=False, max_length=160)

    class Meta:
        icon = "image"
        template = "blocks/image_block.html"


class CTASectionBlock(blocks.StructBlock):
    heading = blocks.CharBlock(max_length=160)
    text = blocks.TextBlock(required=False)
    buttons = blocks.ListBlock(CTAValue, min_num=1, max_num=2)
    variant = blocks.ChoiceBlock(
        choices=[("dark", "Dark green"), ("light", "Light")], default="dark"
    )

    class Meta:
        icon = "link"
        label = "Call to action"
        template = "blocks/cta_block.html"


class ContentStream(blocks.StreamBlock):
    """The composable body used by every content page."""

    rich_text = RichTextSectionBlock()
    stats = StatsBlock()
    feature_grid = FeatureGridBlock()
    process = ProcessBlock()
    case_studies = CaseStudiesBlock()
    values = ValuesBlock()
    ingredients = IngredientsBlock()
    image = ImageBlock()
    cta = CTASectionBlock()

    class Meta:
        block_counts = {}
