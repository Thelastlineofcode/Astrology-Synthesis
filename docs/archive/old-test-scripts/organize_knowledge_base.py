#!/usr/bin/env python3
"""Organize and rename knowledge base books with appropriate naming."""

import os
import shutil
from pathlib import Path

# Knowledge base directory
KB_DIR = Path("/Users/houseofobi/Documents/GitHub/Astrology-Synthesis/knowledge_base")
TEXTS_DIR = KB_DIR / "texts"
TEXTS_DIR.mkdir(parents=True, exist_ok=True)

# Mapping of original filenames to organized names with categories
BOOK_MAPPINGS = {
    # ============================================================================
    # VEDIC ASTROLOGY CORE TEXTS
    # ============================================================================
    "Gopala-Ratnakara.pdf": ("01_vedic_core", "Gopala_Ratnakara_Classical.pdf"),
    "Nakshatra The Authentic Heart of Vedic Astrology by Vic DiCara (z-lib.org).epub": 
        ("01_vedic_core", "Nakshatra_Authentic_Heart_Vedic_Astrology_Vic_DiCara.epub"),
    "Secrets of Nakshatras by Deepak Vishwanathan  Ram Vishwanathan [Vishwanathan, Deepak] (z-lib.org).pdf": 
        ("01_vedic_core", "Secrets_Nakshatras_Deepak_Vishwanathan.pdf"),
    "27 Stars, 27 Gods The Astrological Mythology of Ancient India by Vic DiCara, Vraja Kishor (z-lib.org).pdf": 
        ("01_vedic_core", "27_Stars_27_Gods_Mythology_Ancient_India_DiCara.pdf"),
    
    # ============================================================================
    # VEDIC ASTROLOGY ADVANCED
    # ============================================================================
    "The Art and Science of Vedic Astrology The Foundation Course by W. Ryan Kurczak, Richard Fish (z-lib.org).epub.pdf": 
        ("02_vedic_advanced", "Art_Science_Vedic_Astrology_Foundation_Kurczak_Fish.pdf"),
    "Vedic Astrology An Integrated Approach by Narasimha Rao (z-lib.org).pdf": 
        ("02_vedic_advanced", "Vedic_Astrology_Integrated_Approach_Narasimha_Rao.pdf"),
    "jyotish_astrology-and-diagnosis_sg-khot.pdf": 
        ("02_vedic_advanced", "Jyotish_Astrology_Diagnosis_SG_Khot.pdf"),
    "pdfcoffee.com_hindu-predictive-astrology-of-b-v-raman-pdf-free.pdf": 
        ("02_vedic_advanced", "Hindu_Predictive_Astrology_BV_Raman.pdf"),
    
    # ============================================================================
    # DASHA & TIMING SYSTEMS
    # ============================================================================
    "Mahadashas  The Speed of Light by kapiel raaj (z-lib.org).pdf": 
        ("03_dasha_timing", "Mahadashas_Speed_Light_Kapiel_Raaj.pdf"),
    "Conjunctions-The-Speed-of-Light-by-Kapiel-Raaj-_z-lib.org_-_1_.pdf": 
        ("03_dasha_timing", "Conjunctions_Speed_Light_Kapiel_Raaj.pdf"),
    "pdfcoffee.com_astrology-at-the-speed-of-lightpdf-pdf-free.pdf": 
        ("03_dasha_timing", "Astrology_Speed_Light_Kapiel_Raaj_2.pdf"),
    "pdfcoffee.com_jr-astrology-1-9-pdf-free.pdf": 
        ("03_dasha_timing", "JR_Astrology_Timing_Systems.pdf"),
    
    # ============================================================================
    # WESTERN ASTROLOGY FOUNDATIONS
    # ============================================================================
    "An Astrological Guide to Self-Awareness by Donna Cunningham (z-lib.org).pdf": 
        ("04_western_foundations", "Astrological_Guide_Self_Awareness_Donna_Cunningham.pdf"),
    "New Insights in Modern Astrology by Liz Greene, Stephen Arroyo (z-lib.org).pdf": 
        ("04_western_foundations", "New_Insights_Modern_Astrology_Greene_Arroyo.pdf"),
    "Simplified scientific astrology a complete textbook on the art of erecting a horoscope, with philosophic encyclopedia and tables of planetary hours by Max Heindel (z-lib.org).pdf": 
        ("04_western_foundations", "Simplified_Scientific_Astrology_Max_Heindel.pdf"),
    "The Only Astrology Book You'll Ever Need (7Summits).pdf": 
        ("04_western_foundations", "Only_Astrology_Book_Ever_Need.pdf"),
    
    # ============================================================================
    # PSYCHOLOGICAL & DEPTH ASTROLOGY
    # ============================================================================
    "Astrology for the Soul by Jan Spiller (z-lib.org).epub.pdf": 
        ("05_psychological", "Astrology_Soul_Jan_Spiller.pdf"),
    "Astrology, Karma  Transformation The Inner Dimensions of the Birth Chart by Stephen Arroyo (z-lib.org).pdf": 
        ("05_psychological", "Astrology_Karma_Transformation_Inner_Dimensions_Arroyo.pdf"),
    "Astrology, Karma  Transformation The Inner Dimensions of the Birth Chart by Stephen Arroyo (z-lib.org).epub": 
        ("05_psychological", "Astrology_Karma_Transformation_Inner_Dimensions_Arroyo.epub"),
    "The Astrology of Fate by Liz Greene (z-lib.org).pdf": 
        ("05_psychological", "Astrology_Fate_Liz_Greene.pdf"),
    "The Luminaries The Psychology of the Sun and Moon in the Horoscope by Liz Greene, Howard Sasportas (z-lib.org).epub": 
        ("05_psychological", "Luminaries_Psychology_Sun_Moon_Greene_Sasportas.epub"),
    
    # ============================================================================
    # PLANETS & ASPECTS
    # ============================================================================
    "Saturn A New Look at an Old Devil by Liz Greene, Robert Hand (z-lib.org).pdf": 
        ("06_planets_aspects", "Saturn_New_Look_Old_Devil_Greene_Hand.pdf"),
    "Exploring Jupiter The Astrological Key to Progress, Prosperity  Potential by Stephen Arroyo (z-lib.org).pdf": 
        ("06_planets_aspects", "Exploring_Jupiter_Progress_Prosperity_Arroyo.pdf"),
    "Chiron and the Healing Journey by Melanie Reinhart (z-lib.org).epub.pdf": 
        ("06_planets_aspects", "Chiron_Healing_Journey_Melanie_Reinhart.pdf"),
    "pdfcoffee.com_stephen-arroyo-astrology-psychology-and-the-four-elements-pdf-free.pdf": 
        ("06_planets_aspects", "Astrology_Psychology_Four_Elements_Arroyo.pdf"),
    
    # ============================================================================
    # HOUSES & ANGLES
    # ============================================================================
    "The Twelve Houses Understanding the Importance of the 12 Houses in Your Astrological Birthchart by Howard Sasportas (z-lib.org).pdf": 
        ("07_houses_angles", "Twelve_Houses_Understanding_Sasportas.pdf"),
    "pdfcoffee.com_stephen-arroyo-chart-interpretation-handbookpdf-pdf-free.pdf": 
        ("07_houses_angles", "Chart_Interpretation_Handbook_Arroyo.pdf"),
    
    # ============================================================================
    # SYNASTRY & RELATIONSHIPS
    # ============================================================================
    "Astrological Secrets of Friendship, Love and Marriage by Kumar Gopesh Ojha, Ashutosh Ojha (z-lib.org).pdf": 
        ("08_relationships", "Astrological_Secrets_Friendship_Love_Marriage_Ojha.pdf"),
    "Hayden's Book of Synastry A Complete Guide to Two-Chart Astrology, Composite Charts, and How to Interpret Them by Ajani Abdul-Khaliq (z-lib.org).pdf": 
        ("08_relationships", "Haydens_Book_Synastry_Composite_Charts_Abdul_Khaliq.pdf"),
    "The Secret Language of Relationships  your complete personology guide to any relationship with anyone (Gary Goldschneider) (Z-Library)-compressed.pdf": 
        ("08_relationships", "Secret_Language_Relationships_Gary_Goldschneider.pdf"),
    "Erotic Astrology  The Sex Secrets of Your Horoscope Revealed.pdf": 
        ("08_relationships", "Erotic_Astrology_Sex_Secrets_Horoscope.pdf"),
    
    # ============================================================================
    # TRANSITS & PREDICTIONS
    # ============================================================================
    "Astrological transits  the beginners guide to using planetary cycles to plan and predict your day, week, year (or destiny) by Kent, April Elliott (z-lib.org).epub": 
        ("09_transits_predictions", "Transits_Beginners_Guide_Planetary_Cycles_April_Elliott.epub"),
    "Predictive Astrology The Eagle and the Lark by Bernadette Brady (z-lib.org).pdf": 
        ("09_transits_predictions", "Predictive_Astrology_Eagle_Lark_Bernadette_Brady.pdf"),
    
    # ============================================================================
    # KARMIC ASTROLOGY
    # ============================================================================
    "Karmic Astrology, Volume 1 The Moons Nodes and Reincarnation (Karmic Astrology) by Martin Schulman (z-lib.org).pdf": 
        ("10_karmic_astrology", "Karmic_Astrology_Vol1_Moons_Nodes_Reincarnation_Schulman.pdf"),
    
    # ============================================================================
    # MEDICAL & HEALTH ASTROLOGY
    # ============================================================================
    "_A_Handbook_of_Medical_Astrology_-_Jane_Ridder-Patrick.pdf": 
        ("11_medical_health", "Handbook_Medical_Astrology_Jane_Ridder_Patrick.pdf"),
    "Medical-Astrology-book2.pdf": 
        ("11_medical_health", "Medical_Astrology_Book2.pdf"),
    "MedicalRosacrucianastrology.pdf": 
        ("11_medical_health", "Medical_Rosicrucian_Astrology.pdf"),
    "how-to-give-an-astrological-health-reading.pdf": 
        ("11_medical_health", "How_Give_Astrological_Health_Reading.pdf"),
    "pdfcoffee.com_know-thy-medicinemedical-astrology-handbook-pdf-free.pdf": 
        ("11_medical_health", "Know_Thy_Medicine_Medical_Astrology_Handbook.pdf"),
    
    # ============================================================================
    # COMPLEMENTARY SYSTEMS (Numerology, Tarot, Etc)
    # ============================================================================
    "The Secret Science of Numerology The Hidden Meaning of Numbers and Letters by Shirley Blackwell Lawrence (z-lib.org).pdf": 
        ("12_complementary_systems", "Secret_Science_Numerology_Hidden_Meaning_Lawrence.pdf"),
    "The Ultimate Guide to Numerology Use the Power of Numbers and Your Birthday Code to Manifest Money, Magic, and Miracles by Tania Gabrielle (z-lib.org).epub": 
        ("12_complementary_systems", "Ultimate_Guide_Numerology_Power_Numbers_Tania_Gabrielle.epub"),
    "Vedic Mathematics Secrets. Fun Applications of Vedic Math In Your Everyday Life by William Q. (z-lib.org).pdf": 
        ("12_complementary_systems", "Vedic_Mathematics_Secrets_Fun_Applications.pdf"),
    "The Book of Thoth (Egyptian Tarot) by Aleister Crowley Frieda Harris (z-lib.org).pdf": 
        ("12_complementary_systems", "Book_Thoth_Egyptian_Tarot_Crowley_Harris.pdf"),
    "Tarot Shadow Work Using the Dark Symbols to Heal by Christine Jette (z-lib.org).pdf": 
        ("12_complementary_systems", "Tarot_Shadow_Work_Dark_Symbols_Heal_Christine_Jette.pdf"),
    "Tarot Spreads Layouts  Techniques to Empower Your Readings by Barbara Moore (z-lib.org).epub.pdf": 
        ("12_complementary_systems", "Tarot_Spreads_Layouts_Techniques_Barbara_Moore.pdf"),
    "Tarot Tips (Special Topics in Tarot) by Ruth Ann Amberstone, Wald Amberstone (z-lib.org).pdf": 
        ("12_complementary_systems", "Tarot_Tips_Special_Topics_Ruth_Ann_Wald_Amberstone.pdf"),
    "Palmistry, Plain  Simple The Only Book You'll Ever Need by Sasha Fenton (z-lib.org).epub.pdf": 
        ("12_complementary_systems", "Palmistry_Plain_Simple_Sasha_Fenton.pdf"),
    
    # ============================================================================
    # REFERENCE & ENCYCLOPEDIC
    # ============================================================================
    "Encyclopedia of Astrology by Nicholas deVore (z-lib.org).pdf": 
        ("13_reference", "Encyclopedia_Astrology_Nicholas_deVore.pdf"),
    "The Ultimate Encyclopedia of Mythology by Arthur Cotterell (z-lib.org).pdf": 
        ("13_reference", "Ultimate_Encyclopedia_Mythology_Arthur_Cotterell.pdf"),
    
    # ============================================================================
    # HERMETIC & ESOTERIC PHILOSOPHY
    # ============================================================================
    "Hermetica The Greek Corpus Hermeticum and the Latin Asclepius in a New English Translation, with Notes and Introduction by Brian P. Copenhaver (z-lib.org).pdf": 
        ("14_hermetic_esoteric", "Hermetica_Greek_Corpus_Hermetic_Latin_Asclepius_Copenhaver.pdf"),
    "Hermetica II The Excerpts of Stobaeus, Papyrus Fragments, and Ancient Testimonies in an English Translation with Notes and Introduction by M David Litwa (z-lib.org).pdf": 
        ("14_hermetic_esoteric", "Hermetica_II_Excerpts_Stobaeus_Papyrus_Litwa.pdf"),
    "The Hermetica of Elysium by Banks Annmarie (z-lib.org).epub": 
        ("14_hermetic_esoteric", "Hermetica_Elysium_Banks_Annmarie.epub"),
    "The Hermetica The Lost Wisdom of the Pharaohs by Tim Freke  Peter Gandy (z-lib.org).pdf": 
        ("14_hermetic_esoteric", "Hermetica_Lost_Wisdom_Pharaohs_Freke_Gandy.pdf"),
    "The Language of Demons and Angels Cornelius Agrippas Occult Philosophy by Christopher I. Lehrich (z-lib.org).pdf": 
        ("14_hermetic_esoteric", "Language_Demons_Angels_Agrippas_Occult_Philosophy_Lehrich.pdf"),
    "pdfcoffee.com_titus-burckhardt-mystical-astrology-according-to-ibn-arabi-pdf-free.pdf": 
        ("14_hermetic_esoteric", "Mystical_Astrology_Ibn_Arabi_Titus_Burckhardt.pdf"),
    
    # ============================================================================
    # AYURVEDA & COMPLEMENTARY MEDICINE
    # ============================================================================
    "Ayurveda Beginner's Guide Essential Ayurvedic Principles and Practices to Balance and Heal Naturally by Susan Weis-Bohlen (z-lib.org).epub.pdf": 
        ("15_ayurveda_medicine", "Ayurveda_Beginners_Guide_Principles_Practices_Susan_Weis_Bohlen.pdf"),
    "ayuerveda-diabetes.pdf": 
        ("15_ayurveda_medicine", "Ayurveda_Diabetes.pdf"),
    "pdfcoffee.com_vedic-astrology-and-ayurveda-coursepdf-pdf-free.pdf": 
        ("15_ayurveda_medicine", "Vedic_Astrology_Ayurveda_Course.pdf"),
    "Kundalini The Arousal of the Inner Energy by Ajit Mookerjee (z-lib.org).pdf": 
        ("15_ayurveda_medicine", "Kundalini_Arousal_Inner_Energy_Ajit_Mookerjee.pdf"),
    
    # ============================================================================
    # MYSTICISM & SPIRITUALITY
    # ============================================================================
    "Taoist Secrets of Love Cultivating Male Sexual Energy by Mantak Chia, Michael Winn (z-lib.org).pdf": 
        ("16_mysticism_spirituality", "Taoist_Secrets_Love_Male_Sexual_Energy_Chia_Winn.pdf"),
    "Basic Sigil Magic by Phillip Cooper (z-lib.org).pdf": 
        ("16_mysticism_spirituality", "Basic_Sigil_Magic_Phillip_Cooper.pdf"),
    "The Alchemist by Paulo Coelho (z-lib.org).epub": 
        ("16_mysticism_spirituality", "Alchemist_Paulo_Coelho.epub"),
    "Becoming Supernatural How Common People Are Doing the Uncommon by Dr. Joe Dispenza (z-lib.org).pdf": 
        ("16_mysticism_spirituality", "Becoming_Supernatural_Uncommon_Joe_Dispenza.pdf"),
    "pdfcoffee.com_rosicrucian-cosmo-conception-2-pdf-free.pdf": 
        ("16_mysticism_spirituality", "Rosicrucian_Cosmo_Conception.pdf"),
    "Reinventing religions syncretism and transformation in Africa and the Americas by Sidney M. Greenfield, A. F. Droogers (z-lib.org).epub": 
        ("16_mysticism_spirituality", "Reinventing_Religions_Syncretism_Greenfield_Droogers.epub"),
    "pdfcoffee.com_vodou-visions-pdf-free.pdf": 
        ("16_mysticism_spirituality", "Vodou_Visions.pdf"),
    
    # ============================================================================
    # PSYCHOLOGY & HUMAN BEHAVIOR
    # ============================================================================
    "Games People Play The Psychology of Human Relationships by Eric Berne (z-lib.org).pdf": 
        ("17_psychology", "Games_People_Play_Psychology_Human_Relationships_Eric_Berne.pdf"),
    "Dark Psychology Secret The Essential Guide to Persuasion, Emotional Manipulation, Deception, Mind Control, Human Behavior, NLP and Hypnosis, How To Stop Being Manipulated And Defend Your Mind by Danie (z-lib..pdf": 
        ("17_psychology", "Dark_Psychology_Persuasion_Manipulation_Mind_Control.pdf"),
    "How To Analyze People 13 Laws About the Manipulation of the Human Mind, 7 Strategies to Quickly Figure Out Body Language, Dive into Dark Psychology and Persuasion for Making People Do What You Want by (z-.epub": 
        ("17_psychology", "How_Analyze_People_Manipulation_Mind_Body_Language.epub"),
    
    # ============================================================================
    # SPECIALIZED TEXTS
    # ============================================================================
    "Lunar astrology An attempt at a reconstruction of the ancient astrological system by Alexandre Volguine (z-lib.org).pdf": 
        ("18_specialized", "Lunar_Astrology_Reconstruction_Ancient_System_Volguine.pdf"),
    "Moola21.pdf": 
        ("18_specialized", "Moola_21.pdf"),
    "Astrology At The Speed of Light by Kapiel Raaj (z-lib.org).pdf": 
        ("18_specialized", "Astrology_Speed_Light_Comprehensive_Kapiel_Raaj.pdf"),
    "pdfcoffee.com_astrology-of-the-heart-astro-shamanism-pdf-free.pdf": 
        ("18_specialized", "Astrology_Heart_Astro_Shamanism.pdf"),
    "pdfcoffee.com_book-of-african-divination-pdf-free.pdf": 
        ("18_specialized", "Book_African_Divination.pdf"),
    
    # ============================================================================
    # ASTRONOMY & HISTORICAL
    # ============================================================================
    "Astronomy Through the Ages - Robert Wilson.pdf": 
        ("19_astronomy_historical", "Astronomy_Through_Ages_Robert_Wilson.pdf"),
    
    # ============================================================================
    # REFERENCE (Non-astrological but useful)
    # ============================================================================
    "Etymological Dictionary of Greek (vols. 1  2) by Robert Steven Paul Beekes, Lucien van Beek (z-lib.org).pdf": 
        ("20_reference_support", "Etymological_Dictionary_Greek_Vols_1_2_Beekes_Beek.pdf"),
    "Etymological Dictionary of Latin and the Other Italic Languages (Leiden Indo-European Etymological Dictionary) by Michiel de Vaan (z-lib.org).pdf": 
        ("20_reference_support", "Etymological_Dictionary_Latin_Other_Italic_Vaan.pdf"),
    "Blacks Law Dictionary by Bryan A. Garner, Bryan A. Garner (z-lib.org).pdf": 
        ("20_reference_support", "Blacks_Law_Dictionary_Bryan_Garner.pdf"),
    "The Syntax-Morphology Interface A Study of Syncretism by Matthew Baerman, Dunstan Brown, Greville G. Corbett (z-lib.org).pdf": 
        ("20_reference_support", "Syntax_Morphology_Interface_Syncretism_Baerman_Brown_Corbett.pdf"),
    
    # ============================================================================
    # MARKDOWN FILES
    # ============================================================================
    "Aniesha Voodoo Readings.md": 
        ("16_mysticism_spirituality", "Aniesha_Voodoo_Readings.md"),
}

def organize_books():
    """Rename and organize all books into categorical subdirectories."""
    count_moved = 0
    count_skipped = 0
    count_errors = 0
    
    print(f"\n📚 Organizing Knowledge Base Books")
    print("=" * 80)
    print(f"Source: {KB_DIR}")
    print(f"Target: {TEXTS_DIR}")
    print("=" * 80)
    
    for old_name, (category, new_name) in BOOK_MAPPINGS.items():
        old_path = KB_DIR / old_name
        category_dir = TEXTS_DIR / category
        category_dir.mkdir(parents=True, exist_ok=True)
        new_path = category_dir / new_name
        
        if not old_path.exists():
            print(f"⚠️  SKIP: {old_name} (not found)")
            count_skipped += 1
            continue
        
        try:
            shutil.move(str(old_path), str(new_path))
            print(f"✅ MOVE: {category}/{new_name}")
            count_moved += 1
        except Exception as e:
            print(f"❌ ERROR: {old_name} - {e}")
            count_errors += 1
    
    print("\n" + "=" * 80)
    print(f"📊 Summary:")
    print(f"  ✅ Moved: {count_moved}")
    print(f"  ⚠️  Skipped: {count_skipped}")
    print(f"  ❌ Errors: {count_errors}")
    print("=" * 80)
    
    # List categories
    categories = {}
    for category_path in sorted(TEXTS_DIR.glob("*")):
        if category_path.is_dir():
            count = len(list(category_path.glob("*")))
            categories[category_path.name] = count
    
    print(f"\n📑 Categories Created ({len(categories)}):")
    for category in sorted(categories.keys()):
        print(f"  {category}: {categories[category]} books")
    
    print(f"\n✨ Total Books Organized: {sum(categories.values())}")

if __name__ == "__main__":
    organize_books()
