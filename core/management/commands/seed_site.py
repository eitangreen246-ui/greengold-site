"""Seed the GreenGold site tree with on-brand starter content.

Idempotent: re-running updates existing pages (matched by slug) rather than
duplicating them. All copy here is editable later in the Wagtail admin.
"""
from django.core.management.base import BaseCommand
from wagtail.models import Page, Site

from cms.models import ContactPage, ContentPage
from home.models import HomePage


def upsert_child(parent, model, slug, title, **fields):
    existing = model.objects.filter(slug=slug).first()
    if existing:
        for key, value in {**fields, "title": title}.items():
            setattr(existing, key, value)
        existing.save()
        return existing
    page = model(slug=slug, title=title, **fields)
    parent.add_child(instance=page)
    page.save_revision().publish()
    return page


class Command(BaseCommand):
    help = "Create/refresh the GreenGold page tree with starter content."

    def handle(self, *args, **options):
        root = Page.objects.get(depth=1)

        # --- Home page (reuse the one created by the home app migration) ---
        home = HomePage.objects.first()
        if not home:
            home = HomePage(title="Home", slug="home")
            root.add_child(instance=home)
        home.title = "Home"
        home.seo_title = "Bridging Science to Tomorrow's Beauty"
        home.search_description = (
            "GreenGold Bioscience bridges cutting-edge science to the global cosmetics "
            "industry — custom delivery systems, science-based formulation, and novel raw materials."
        )
        home.body = [
            ("feature_grid", {
                "eyebrow": "What we do",
                "heading": "Three connected ways we move science into the market",
                "intro": "From sourcing breakthrough raw materials to engineering the systems that make them perform.",
                "columns": "3",
                "features": [
                    {"icon": "link", "title": "Business Development", "text": "We source, vet and represent revolutionary raw materials — connecting biotech, pharma and marine innovation to the cosmetics industry."},
                    {"icon": "layers", "title": "Delivery Systems", "text": "Custom carrier systems engineered from scratch to improve the activity and stability of your actives."},
                    {"icon": "flask", "title": "Formulation", "text": "Science-based cosmetic formulations built around our unique delivery systems — with proven, measurable results."},
                ],
            }),
            ("stats", {
                "heading": "A rare combination of academic science and industry depth",
                "stats": [
                    {"value": "2 PhD", "label": "in pharmaceutics & life sciences on the team"},
                    {"value": "40+", "label": "years of combined industry experience"},
                    {"value": "Global", "label": "partners across Europe, the US and Asia"},
                ],
            }),
            ("feature_grid", {
                "eyebrow": "Why GreenGold",
                "heading": "We bring data, not promises",
                "columns": "2",
                "features": [
                    {"icon": "microscope", "title": "Academic-grade science", "text": "Decisions grounded in proven data and current literature — we proved it works, we didn't just hear that it works."},
                    {"icon": "target", "title": "Custom, never generic", "text": "Every delivery system and formulation is engineered from zero for your specific molecule and final product."},
                    {"icon": "leaf", "title": "A real bridge to novel ingredients", "text": "Access to innovative actives from biotech, pharma and marine sources that haven't yet reached cosmetics."},
                    {"icon": "handshake", "title": "Committed to the result", "text": "We act as long-term partners, not one-off vendors. Your success is our success."},
                ],
            }),
            ("cta", {
                "heading": "Bring us your toughest formulation challenge",
                "text": "Tell us about your molecule, your product, or your market — and we'll show you what's possible.",
                "variant": "dark",
                "buttons": [
                    {"label": "Get in touch", "url": "/contact/", "style": "gold"},
                    {"label": "Explore delivery systems", "url": "/delivery-systems/", "style": "outline"},
                ],
            }),
        ]
        home.save()
        home.save_revision().publish()

        # Point the default Site at our home page.
        site = Site.objects.first()
        if site:
            site.root_page = home
            site.site_name = "GreenGold Bioscience"
            site.save()

        # --- Delivery Systems ---
        upsert_child(
            home, ContentPage, "delivery-systems", "Delivery Systems",
            search_description="Custom delivery systems for cosmetics — liposomes, ethosomes, exosomes, nanoparticles and microencapsulation, engineered for your active.",
            hero_badge="For cosmetics manufacturers",
            hero_heading="Carrier systems that make your actives actually perform",
            hero_intro="A delivery system determines whether an active reaches its target, stays stable, and delivers a measurable effect. We engineer them from scratch for your molecule and product.",
            hero_cta_label="Request a proposal",
            body=[
                ("feature_grid", {
                    "eyebrow": "Technologies",
                    "heading": "The carrier platforms we engineer",
                    "columns": "3",
                    "features": [
                        {"icon": "droplet", "title": "Liposomes", "text": "Phospholipid vesicles for encapsulating and protecting sensitive actives."},
                        {"icon": "layers", "title": "Ethosomes", "text": "Enhanced skin penetration for deeper, more effective delivery."},
                        {"icon": "sparkles", "title": "Exosomes", "text": "Next-generation carriers, including customized exosome business cases."},
                        {"icon": "atom", "title": "Nanoparticles", "text": "Precision-engineered particles for controlled release."},
                        {"icon": "flask", "title": "Microencapsulation", "text": "Stabilisation and triggered release of demanding ingredients."},
                    ],
                }),
                ("case_studies", {
                    "eyebrow": "Proven in practice",
                    "heading": "Selected delivery-system case studies",
                    "intro": "Results speak louder than names — here is what the science delivered.",
                    "items": [
                        {"name": "FollicleX™", "tagline": "Hair-loss delivery system",
                         "description": "<p>A cosmeceutical delivery system engineered for scalp and follicle targeting, backed by clinical evaluation.</p>",
                         "metrics": [{"value": "Clinical", "label": "data-backed"}, {"value": "Targeted", "label": "follicle delivery"}, {"value": "Stable", "label": "formulation"}]},
                        {"name": "SA+", "tagline": "Enhanced active stability",
                         "description": "<p>A carrier system improving the stability and activity of a sensitive active across the product shelf-life.</p>", "metrics": []},
                        {"name": "Argan Delivery System", "tagline": "Performance from a natural active",
                         "description": "<p>A bespoke system maximising the measurable performance of a natural oil-derived active.</p>", "metrics": []},
                    ],
                }),
                ("process", {
                    "eyebrow": "How we work",
                    "heading": "From screening to scale-up",
                    "steps": [
                        {"title": "Screening", "text": "We assess your active and define the delivery challenge."},
                        {"title": "Prototype", "text": "We engineer and test candidate carrier systems."},
                        {"title": "Stability", "text": "Stability, efficacy and characterisation studies."},
                        {"title": "Scale-up", "text": "Integration into your formulation and production."},
                    ],
                }),
                ("cta", {"heading": "Ready to engineer a delivery system?", "text": "Send us your brief and we'll propose an approach.", "variant": "dark",
                         "buttons": [{"label": "Request a proposal", "url": "/contact/", "style": "gold"}]}),
            ],
        )

        # --- Formulation ---
        upsert_child(
            home, ContentPage, "formulation", "Cosmetic Formulation",
            search_description="Science-based cosmetic formulation development in Israel — skincare, haircare, body care and dermo-cosmetics built around unique delivery systems.",
            hero_badge="For cosmetics manufacturers",
            hero_heading="Science-based formulation, built around delivery",
            hero_intro="We develop cosmetic formulations that use our unique delivery systems to amplify active performance and deliver proven results.",
            hero_cta_label="Start your brief",
            body=[
                ("feature_grid", {
                    "eyebrow": "Capabilities",
                    "heading": "What we formulate",
                    "columns": "2",
                    "features": [
                        {"icon": "droplet", "title": "Skincare", "text": "Serums, creams and treatments with measurable active delivery."},
                        {"icon": "sparkles", "title": "Haircare", "text": "Scalp and hair systems, including FollicleX™."},
                        {"icon": "leaf", "title": "Body care", "text": "Performance body formulations across categories."},
                        {"icon": "shield", "title": "Dermo-cosmetics", "text": "Evidence-led products that meet regulatory expectations."},
                    ],
                }),
                ("process", {
                    "eyebrow": "How it works",
                    "heading": "From questionnaire to finished brief",
                    "steps": [
                        {"title": "Questionnaire", "text": "You tell us about the target product and claims."},
                        {"title": "Brief", "text": "We translate it into a science-based development brief."},
                        {"title": "Development", "text": "We formulate, test and refine to your targets."},
                    ],
                }),
                ("cta", {"heading": "Tell us what you want to build", "text": "Fill in a short brief and we'll take it from there.", "variant": "dark",
                         "buttons": [{"label": "Start your brief", "url": "/contact/", "style": "gold"}]}),
            ],
        )

        # --- Ingredients Portfolio (BD) ---
        upsert_child(
            home, ContentPage, "ingredients", "Ingredients Portfolio",
            search_description="Novel cosmetic raw materials — marine and microalgae-derived actives, plant-based growth factors and advanced delivery molecules, vetted by scientists.",
            hero_badge="Business Development",
            hero_heading="Novel raw materials, vetted by scientists",
            hero_intro="We represent breakthrough actives from adjacent industries — each independently evaluated before we put our name behind it.",
            hero_cta_label="Request a sample",
            body=[
                ("ingredients", {
                    "eyebrow": "Portfolio",
                    "heading": "Categories we represent",
                    "intro": "Each category is backed by scientific description, applications, clinical evidence and regulatory status.",
                    "categories": [
                        {"icon": "droplet", "name": "Microalgae-derived actives", "description": "Bioactives from marine and microalgae sources with novel mechanisms.",
                         "applications": "Anti-ageing, barrier repair, soothing", "evidence": "In-vitro & clinical characterisation", "regulatory": "Cosmetic-compliant sourcing"},
                        {"icon": "leaf", "name": "Plant-based growth factors", "description": "Plant-derived growth-factor analogues for regenerative claims.",
                         "applications": "Hair, scalp, skin renewal", "evidence": "Mechanistic & efficacy data", "regulatory": "Documented origin & safety"},
                        {"icon": "atom", "name": "Advanced delivery molecules", "description": "Molecules engineered to enable or enhance delivery performance.",
                         "applications": "Penetration, stability, targeting", "evidence": "Characterisation & stability data", "regulatory": "Full technical dossier"},
                    ],
                }),
                ("cta", {"heading": "Looking for something specific?", "text": "Tell us your target claim or molecule and we'll point you to the right material.", "variant": "light",
                         "buttons": [{"label": "Request a sample", "url": "/contact/", "style": "primary"}]}),
            ],
        )

        # --- Partner With Us (Audience B) ---
        upsert_child(
            home, ContentPage, "partner", "Partner With Us",
            search_description="Raw-material and biotech manufacturers: GreenGold is your bridge into the global cosmetics industry — distribution, scientific and regulatory expertise, market access.",
            hero_badge="For raw-material manufacturers",
            hero_heading="Your bridge into the global cosmetics industry",
            hero_intro="Have breakthrough IP but no cosmetic-market access? We open the door to the world's leading brands and manufacturers — with the scientific and regulatory rigour they expect.",
            hero_cta_label="Talk to us about collaboration",
            body=[
                ("feature_grid", {
                    "eyebrow": "What we offer",
                    "heading": "How we help you reach the market",
                    "columns": "2",
                    "features": [
                        {"icon": "globe", "title": "Access to leading brands", "text": "Direct relationships with top global cosmetics brands and manufacturers."},
                        {"icon": "microscope", "title": "Scientific & regulatory know-how", "text": "Deep expertise to position your material credibly and compliantly."},
                        {"icon": "layers", "title": "Dossier & presentation prep", "text": "We build the technical story buyers and formulators need."},
                        {"icon": "shield", "title": "Vendor-qualification management", "text": "We manage the qualification process end to end."},
                    ],
                }),
                ("cta", {"heading": "Let's bring your innovation to market", "text": "Share your product and target market — we'll tell you how we can help.", "variant": "dark",
                         "buttons": [{"label": "Talk to us", "url": "/contact/", "style": "gold"}]}),
            ],
        )

        # --- About ---
        upsert_child(
            home, ContentPage, "about", "About Us",
            search_description="GreenGold Bioscience combines PhD-level science with decades of global cosmetics experience — a bridge between innovation and the beauty industry.",
            hero_heading="A scientific bridge between innovation and beauty",
            hero_intro="GreenGold Bioscience combines academic-grade science with decades of global cosmetics experience — a rare blend of scientific excellence and deep business understanding.",
            body=[
                ("values", {
                    "eyebrow": "Our core values",
                    "heading": "What we stand for",
                    "values": [
                        {"icon": "microscope", "title": "Uncompromising scientific expertise", "text": "Decisions based on proven data only — deep, current knowledge of materials, regulation and trends.", "tag": "Scientific Rigor"},
                        {"icon": "link", "title": "Connecting innovation", "text": "We spot technological potential in neighbouring industries and connect it to specific cosmetic needs.", "tag": "Bridging Innovation"},
                        {"icon": "handshake", "title": "Success-driven partnership", "text": "We treat clients as long-term partners and stay involved from opportunity to market success.", "tag": "Partnership"},
                        {"icon": "shield", "title": "Integrity & stewardship", "text": "Professional and regulatory integrity at every step — from the lab to the contract.", "tag": "Integrity"},
                    ],
                }),
                ("rich_text", {
                    "eyebrow": "Why GreenGold",
                    "heading": "The story behind the name",
                    "body": "<p><b>Green</b> stands for science and nature — the rigorous, evidence-led core of everything we do. <b>Gold</b> stands for value and premium — the measurable results and quality we deliver to our partners. Together they describe exactly what we are: a bridge between science and the future of beauty.</p>",
                }),
                ("cta", {"heading": "Work with a partner who brings data", "text": "Whether you make cosmetics or raw materials, we'd love to talk.", "variant": "dark",
                         "buttons": [{"label": "Get in touch", "url": "/contact/", "style": "gold"}]}),
            ],
        )

        # --- Contact ---
        upsert_child(
            home, ContactPage, "contact", "Contact",
            search_description="Get in touch with GreenGold Bioscience — whether you make cosmetics or raw materials, tell us about your project.",
        )

        self.stdout.write(self.style.SUCCESS("Seeded GreenGold site tree."))
