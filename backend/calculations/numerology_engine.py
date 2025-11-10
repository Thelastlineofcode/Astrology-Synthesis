"""
Numerology Calculation Engine

Provides numerological insights for personal development and coaching.
Includes life path, destiny, soul urge, and personality number calculations.

IMPORTANT: This is a personal development tool, NOT a scientific assessment.
For coaching, self-reflection, and team building only.
"""

from typing import Dict, Optional
from datetime import date
import logging

logger = logging.getLogger(__name__)


class NumerologyCalculator:
    """
    Numerology calculator for personal development insights.

    Provides:
    - Life path number (from birth date)
    - Destiny number (from full name)
    - Soul urge number (from vowels in name)
    - Personality number (from consonants in name)
    - Day of week insights
    """

    # Pythagorean numerology letter values
    LETTER_VALUES = {
        'A': 1, 'B': 2, 'C': 3, 'D': 4, 'E': 5, 'F': 6, 'G': 7, 'H': 8, 'I': 9,
        'J': 1, 'K': 2, 'L': 3, 'M': 4, 'N': 5, 'O': 6, 'P': 7, 'Q': 8, 'R': 9,
        'S': 1, 'T': 2, 'U': 3, 'V': 4, 'W': 5, 'X': 6, 'Y': 7, 'Z': 8,
    }

    # Vowels for soul urge calculation
    VOWELS = set('AEIOUY')

    # Master numbers (not reduced)
    MASTER_NUMBERS = {11, 22, 33}

    def __init__(self):
        """Initialize numerology calculator."""
        logger.info("NumerologyCalculator initialized")

    def calculate_life_path_number(self, birth_date: date) -> int:
        """
        Calculate life path number from birth date.

        Life path is the most important number in numerology,
        representing one's life purpose and natural tendencies.

        Args:
            birth_date: Date of birth

        Returns:
            Life path number (1-9, 11, 22, or 33)
        """
        # Method: Reduce each component separately, then reduce sum
        day = self._reduce_to_single_digit(birth_date.day)
        month = self._reduce_to_single_digit(birth_date.month)
        year = self._reduce_to_single_digit(birth_date.year)

        total = day + month + year
        life_path = self._reduce_to_single_digit(total)

        logger.debug(
            f"Life path calculation: {birth_date} -> "
            f"day={day}, month={month}, year={year} -> total={total} -> {life_path}"
        )

        return life_path

    def calculate_destiny_number(self, full_name: str) -> int:
        """
        Calculate destiny number from full name.

        Destiny number reveals one's life mission and what they're
        meant to accomplish.

        Args:
            full_name: Full birth name

        Returns:
            Destiny number (1-9, 11, 22, or 33)
        """
        return self._calculate_name_number(full_name, use_all_letters=True)

    def calculate_soul_urge_number(self, full_name: str) -> int:
        """
        Calculate soul urge number from vowels in name.

        Soul urge (heart's desire) reveals inner motivations and
        what truly drives a person.

        Args:
            full_name: Full birth name

        Returns:
            Soul urge number (1-9, 11, 22, or 33)
        """
        return self._calculate_name_number(full_name, vowels_only=True)

    def calculate_personality_number(self, full_name: str) -> int:
        """
        Calculate personality number from consonants in name.

        Personality number reveals how others perceive you and
        the outer personality you project.

        Args:
            full_name: Full birth name

        Returns:
            Personality number (1-9, 11, 22, or 33)
        """
        return self._calculate_name_number(full_name, consonants_only=True)

    def interpret_life_path_number(self, number: int) -> str:
        """
        Get interpretation for life path number.

        Focused on personal development, work style, and team dynamics.

        Args:
            number: Life path number

        Returns:
            Interpretation string
        """
        interpretations = {
            1: (
                "Natural leader and innovator. Thrives when given autonomy and the ability "
                "to pioneer new initiatives. Brings independent thinking and courage to teams. "
                "Development area: Collaboration and receptivity to others' ideas."
            ),
            2: (
                "Natural diplomat and mediator. Excels in partnership and collaborative environments. "
                "Brings emotional intelligence and harmony-building to teams. Sensitive to group dynamics. "
                "Development area: Assertiveness and setting boundaries."
            ),
            3: (
                "Creative communicator and optimist. Brings enthusiasm, fresh ideas, and positive energy. "
                "Natural at presentations, brainstorming, and team morale. Inspires creativity in others. "
                "Development area: Follow-through and depth of focus."
            ),
            4: (
                "Systematic builder and organizer. Excels at creating structures, processes, and stability. "
                "Reliable team member who ensures plans are executed thoroughly. Detail-oriented and practical. "
                "Development area: Flexibility and embracing change."
            ),
            5: (
                "Dynamic change agent and adapter. Thrives in fast-paced, evolving environments. "
                "Brings versatility, resourcefulness, and fresh perspectives. Natural at pivoting strategies. "
                "Development area: Commitment and seeing projects through to completion."
            ),
            6: (
                "Natural nurturer and responsibility-taker. Creates supportive team environments and "
                "ensures everyone is cared for. Brings harmony, service, and conscientiousness. "
                "Development area: Avoiding over-responsibility and martyrdom."
            ),
            7: (
                "Analytical thinker and researcher. Brings depth, wisdom, and intellectual rigor. "
                "Excels at independent research, analysis, and strategic thinking. Questions assumptions. "
                "Development area: Practical application and team integration."
            ),
            8: (
                "Natural executive and manifestor. Brings ambition, organizational leadership, and "
                "results orientation. Excels at resource management and achieving tangible outcomes. "
                "Development area: Work-life balance and compassion."
            ),
            9: (
                "Humanitarian visionary and integrator. Brings compassion, broad perspective, and "
                "inclusive thinking. Natural at seeing the big picture and bringing people together. "
                "Development area: Personal boundaries and letting go."
            ),
            11: (
                "Master number: Intuitive visionary and inspirer. Highly sensitive with access to "
                "deep insights and inspiration. Brings innovative ideas and spiritual perspective to work. "
                "Natural at inspiring others. Development area: Grounding vision in practical reality."
            ),
            22: (
                "Master number: Master builder and architect. Combines visionary thinking with "
                "practical execution. Can manifest large-scale projects and build lasting structures. "
                "Development area: Managing high expectations and perfectionism."
            ),
            33: (
                "Master number: Master teacher and healer. Brings profound compassion, teaching ability, "
                "and uplifting energy. Natural at mentoring, coaching, and supporting others' growth. "
                "Development area: Avoiding burnout from overgiving."
            ),
        }

        return interpretations.get(
            number,
            f"Life path {number}: Unique strengths to explore through self-reflection."
        )

    def interpret_destiny_number(self, number: int) -> str:
        """
        Get interpretation for destiny number.

        Args:
            number: Destiny number

        Returns:
            Interpretation string
        """
        interpretations = {
            1: "Destined to lead, innovate, and pioneer. Your mission involves independence and originality.",
            2: "Destined to cooperate, mediate, and harmonize. Your mission involves partnership and diplomacy.",
            3: "Destined to communicate, create, and inspire. Your mission involves self-expression and joy.",
            4: "Destined to build, organize, and establish. Your mission involves creating stable foundations.",
            5: "Destined to explore, adapt, and liberate. Your mission involves freedom and versatility.",
            6: "Destined to nurture, teach, and serve. Your mission involves responsibility and community.",
            7: "Destined to analyze, understand, and seek truth. Your mission involves wisdom and depth.",
            8: "Destined to achieve, manage, and manifest. Your mission involves power and material mastery.",
            9: "Destined to heal, complete, and serve humanity. Your mission involves compassion and letting go.",
            11: "Master destiny: Destined to inspire and illuminate. Spiritual teaching and upliftment.",
            22: "Master destiny: Destined to build on a grand scale. Material mastery for spiritual purpose.",
            33: "Master destiny: Destined to teach and heal. Compassionate service and unconditional love.",
        }

        return interpretations.get(
            number,
            f"Destiny number {number}: A unique life path to discover."
        )

    def interpret_soul_urge_number(self, number: int) -> str:
        """
        Get interpretation for soul urge number.

        Args:
            number: Soul urge number

        Returns:
            Interpretation string
        """
        interpretations = {
            1: "Deep desire for independence, leadership, and making your own way. Motivated by autonomy.",
            2: "Deep desire for partnership, harmony, and connection. Motivated by relationships and peace.",
            3: "Deep desire for self-expression, creativity, and joy. Motivated by communication and inspiration.",
            4: "Deep desire for security, order, and building something lasting. Motivated by stability.",
            5: "Deep desire for freedom, variety, and adventure. Motivated by change and new experiences.",
            6: "Deep desire to nurture, serve, and create harmony. Motivated by responsibility and care.",
            7: "Deep desire for understanding, wisdom, and inner truth. Motivated by knowledge and reflection.",
            8: "Deep desire for success, achievement, and material mastery. Motivated by power and recognition.",
            9: "Deep desire to serve humanity and make the world better. Motivated by compassion and ideals.",
            11: "Deep desire to inspire and uplift others spiritually. Motivated by intuition and illumination.",
            22: "Deep desire to build something significant and lasting. Motivated by grand visions.",
            33: "Deep desire to teach, heal, and serve with unconditional love. Motivated by compassion.",
        }

        return interpretations.get(
            number,
            f"Soul urge {number}: Inner motivations to explore."
        )

    def interpret_personality_number(self, number: int) -> str:
        """
        Get interpretation for personality number.

        Args:
            number: Personality number

        Returns:
            Interpretation string
        """
        interpretations = {
            1: "Appears confident, independent, and pioneering. First impression: strong and self-directed.",
            2: "Appears gentle, diplomatic, and sensitive. First impression: cooperative and understanding.",
            3: "Appears friendly, creative, and optimistic. First impression: expressive and entertaining.",
            4: "Appears reliable, organized, and practical. First impression: stable and trustworthy.",
            5: "Appears dynamic, adaptable, and energetic. First impression: exciting and versatile.",
            6: "Appears caring, responsible, and warm. First impression: nurturing and dependable.",
            7: "Appears thoughtful, reserved, and analytical. First impression: mysterious and intelligent.",
            8: "Appears ambitious, powerful, and successful. First impression: authoritative and competent.",
            9: "Appears compassionate, idealistic, and magnetic. First impression: wise and worldly.",
            11: "Appears inspired, intuitive, and charismatic. First impression: special and illuminated.",
            22: "Appears capable, visionary, and impressive. First impression: masterful and grounded.",
            33: "Appears loving, healing, and uplifting. First impression: compassionate teacher.",
        }

        return interpretations.get(
            number,
            f"Personality {number}: Unique outer expression."
        )

    def interpret_day_of_week(self, day_name: str) -> str:
        """
        Get insights based on day of week born.

        Ancient tradition associates personality traits with weekday of birth.

        Args:
            day_name: Name of weekday (e.g., "Monday")

        Returns:
            Day of week interpretation
        """
        interpretations = {
            "Monday": (
                "Born on Moon's day: Emotionally intuitive and responsive. Natural empathy and "
                "sensitivity to others' feelings. Brings emotional awareness to teams."
            ),
            "Tuesday": (
                "Born on Mars' day: Action-oriented and courageous. Natural drive and competitive spirit. "
                "Brings energy and initiative to projects."
            ),
            "Wednesday": (
                "Born on Mercury's day: Communicative and intellectually curious. Natural at networking "
                "and information exchange. Brings versatility and quick thinking."
            ),
            "Thursday": (
                "Born on Jupiter's day: Optimistic and growth-oriented. Natural teacher and expander. "
                "Brings wisdom, generosity, and big-picture thinking."
            ),
            "Friday": (
                "Born on Venus' day: Harmonious and aesthetically oriented. Natural at building relationships "
                "and creating beauty. Brings diplomacy and social grace."
            ),
            "Saturday": (
                "Born on Saturn's day: Disciplined and responsible. Natural at structure and long-term planning. "
                "Brings patience, perseverance, and wisdom through experience."
            ),
            "Sunday": (
                "Born on Sun's day: Confident and vital. Natural leadership and self-expression. "
                "Brings radiance, creativity, and the ability to inspire others."
            ),
        }

        return interpretations.get(
            day_name,
            f"{day_name}: Unique qualities associated with this birth day."
        )

    # Private helper methods

    def _reduce_to_single_digit(self, number: int) -> int:
        """
        Reduce a number to single digit (or master number).

        Args:
            number: Number to reduce

        Returns:
            Reduced number (1-9, 11, 22, or 33)
        """
        while number > 9:
            # Check for master numbers before reducing
            if number in self.MASTER_NUMBERS:
                return number

            # Sum the digits
            number = sum(int(digit) for digit in str(number))

        return number

    def _calculate_name_number(
        self,
        name: str,
        use_all_letters: bool = False,
        vowels_only: bool = False,
        consonants_only: bool = False,
    ) -> int:
        """
        Calculate numerology number from name.

        Args:
            name: Full name
            use_all_letters: Use all letters (destiny number)
            vowels_only: Use only vowels (soul urge)
            consonants_only: Use only consonants (personality)

        Returns:
            Calculated number
        """
        # Clean name: uppercase, remove non-letters
        clean_name = ''.join(c.upper() for c in name if c.isalpha())

        total = 0
        for letter in clean_name:
            if letter not in self.LETTER_VALUES:
                continue

            # Apply filters
            if vowels_only and letter not in self.VOWELS:
                continue
            if consonants_only and letter in self.VOWELS:
                continue

            total += self.LETTER_VALUES[letter]

        # Reduce to single digit or master number
        result = self._reduce_to_single_digit(total)

        filter_type = (
            "all" if use_all_letters else
            "vowels" if vowels_only else
            "consonants" if consonants_only else
            "unknown"
        )
        logger.debug(
            f"Name number calculation ({filter_type}): '{name}' -> "
            f"clean='{clean_name}' -> total={total} -> {result}"
        )

        return result

    def get_all_numbers(
        self,
        birth_date: date,
        full_name: Optional[str] = None,
    ) -> Dict[str, int]:
        """
        Calculate all numerology numbers at once.

        Args:
            birth_date: Date of birth
            full_name: Full birth name (optional)

        Returns:
            Dictionary with all numbers
        """
        numbers = {
            "life_path": self.calculate_life_path_number(birth_date),
        }

        if full_name:
            numbers.update({
                "destiny": self.calculate_destiny_number(full_name),
                "soul_urge": self.calculate_soul_urge_number(full_name),
                "personality": self.calculate_personality_number(full_name),
            })

        return numbers

    def get_all_interpretations(
        self,
        birth_date: date,
        full_name: Optional[str] = None,
    ) -> Dict[str, str]:
        """
        Get all interpretations at once.

        Args:
            birth_date: Date of birth
            full_name: Full birth name (optional)

        Returns:
            Dictionary with all interpretations
        """
        numbers = self.get_all_numbers(birth_date, full_name)

        interpretations = {
            "life_path": self.interpret_life_path_number(numbers["life_path"]),
            "day_of_week": self.interpret_day_of_week(birth_date.strftime("%A")),
        }

        if full_name:
            interpretations.update({
                "destiny": self.interpret_destiny_number(numbers["destiny"]),
                "soul_urge": self.interpret_soul_urge_number(numbers["soul_urge"]),
                "personality": self.interpret_personality_number(numbers["personality"]),
            })

        return interpretations
