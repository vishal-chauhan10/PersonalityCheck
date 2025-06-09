from datetime import date
import g4f
from typing import List, Optional, Dict
import asyncio

# Pythagorean Numerology System
PYTHAGOREAN_MAP = {
    'a': 1, 'j': 1, 's': 1,
    'b': 2, 'k': 2, 't': 2,
    'c': 3, 'l': 3, 'u': 3,
    'd': 4, 'm': 4, 'v': 4,
    'e': 5, 'n': 5, 'w': 5,
    'f': 6, 'o': 6, 'x': 6,
    'g': 7, 'p': 7, 'y': 7,
    'h': 8, 'q': 8, 'z': 8,
    'i': 9, 'r': 9
}

def reduce_number(n: int, allow_master: bool = True) -> int:
    """Reduce a number to a single digit or master number if allowed."""
    if allow_master and n in [11, 22, 33]:
        return n
    while n > 9:
        n = sum(int(d) for d in str(n))
        if allow_master and n in [11, 22, 33]:
            break
    return n

class NumerologyCalculator:
    def __init__(self, name: str, birth_date: date):
        self.name = name
        self.birth_date = birth_date

    def calculate_name_number(self, filter_func=None) -> int:
        """Calculate number from name using optional filter function for vowels/consonants."""
        name = self.name.lower()
        numbers = [PYTHAGOREAN_MAP[char] for char in name 
                  if char.isalpha() and char in PYTHAGOREAN_MAP 
                  and (filter_func(char) if filter_func else True)]
        total = sum(numbers)
        return reduce_number(total)

    def calculate_life_path_number(self) -> int:
        """Calculate Life Path Number from birth date following numerological rules."""
        # Get individual components
        day = self.birth_date.day
        month = self.birth_date.month
        year = self.birth_date.year
        
        # Reduce each component
        day_sum = reduce_number(day)
        month_sum = reduce_number(month)
        year_sum = reduce_number(year)
        
        # Calculate final life path number
        life_path = day_sum + month_sum + year_sum
        return reduce_number(life_path)

    def calculate_destiny_number(self) -> int:
        """Calculate Expression/Destiny Number from full name."""
        return self.calculate_name_number()

    def calculate_soul_urge_number(self) -> int:
        """Calculate Soul Urge (Heart's Desire) Number from vowels in name."""
        return self.calculate_name_number(lambda c: c in 'aeiou')

    def calculate_personality_number(self) -> int:
        """Calculate Personality Number from consonants in name."""
        return self.calculate_name_number(lambda c: c not in 'aeiou')

    def calculate_birthday_number(self) -> int:
        """Calculate Birthday Number - day of birth (usually not reduced)."""
        day = self.birth_date.day
        return day if day in [11, 22] else reduce_number(day, allow_master=False)

    def calculate_maturity_number(self) -> int:
        """Calculate Maturity Number from Life Path and Destiny numbers."""
        life_path = self.calculate_life_path_number()
        destiny = self.calculate_destiny_number()
        return reduce_number(life_path + destiny)

    def calculate_personal_year(self) -> int:
        """Calculate Personal Year number."""
        current_year = date.today().year
        # Reduce month and day
        month_day = reduce_number(self.birth_date.month + self.birth_date.day, allow_master=False)
        # Reduce current year
        year_number = reduce_number(current_year, allow_master=False)
        return reduce_number(month_day + year_number)

    def calculate_karmic_lessons(self) -> List[int]:
        """Calculate Karmic Lesson Numbers (missing numbers in name)."""
        name = self.name.lower()
        name_numbers = {PYTHAGOREAN_MAP[char] for char in name 
                       if char.isalpha() and char in PYTHAGOREAN_MAP}
        all_numbers = set(range(1, 10))  # Pythagorean system uses 1-9
        return sorted(list(all_numbers - name_numbers))

    def get_complete_profile(self) -> Dict:
        """Calculate all numerological numbers."""
        return {
            "life_path_number": self.calculate_life_path_number(),
            "destiny_number": self.calculate_destiny_number(),
            "soul_urge_number": self.calculate_soul_urge_number(),
            "personality_number": self.calculate_personality_number(),
            "birthday_number": self.calculate_birthday_number(),
            "maturity_number": self.calculate_maturity_number(),
            "personal_year": self.calculate_personal_year(),
            "karmic_lessons": self.calculate_karmic_lessons()
        }

async def get_personality_analysis(
    name: str,
    birth_date: date,
    life_path: int,
    responses: Optional[List[dict]] = None
) -> dict:
    """Generate comprehensive personality analysis using free GPT API."""
    calculator = NumerologyCalculator(name, birth_date)
    profile = calculator.get_complete_profile()
    
    system_prompt = """You are a highly experienced numerologist with decades of expertise in providing comprehensive numerological analyses. Your deep understanding of numerology's spiritual and practical aspects allows you to offer profound insights into people's lives.

Provide a detailed analysis covering the following aspects:

1. Core Numbers Analysis:
- Life Path Number {life_path}: Life purpose, lessons, and journey
- Expression/Destiny Number {destiny}: Natural talents and life direction
- Soul Urge Number {soul_urge}: Inner motivations and desires
- Personality Number {personality}: External persona and impression on others
- Birthday Number {birthday}: Special talents and characteristics

2. Advanced Numerological Indicators:
- Maturity Number {maturity}: Long-term development and life goals
- Personal Year {personal_year}: Current year's themes and opportunities
- Karmic Lessons {karmic_lessons}: Areas for spiritual growth

3. Comprehensive Life Analysis:
- Personal Strengths: Natural abilities and talents
- Growth Opportunities: Areas for development
- Life Challenges: Obstacles and how to overcome them
- Career Path: Suitable professions and work environments
- Relationships: Compatibility insights and relationship patterns

4. Spiritual and Personal Development:
- Spiritual Journey: Path to personal enlightenment
- Life Purpose: Core mission and contribution
- Personal Growth: Development opportunities
- Daily Practices: Recommended activities for growth

5. Practical Guidance:
- Action Steps: Specific recommendations for personal development
- Career Advice: Professional development strategies
- Relationship Guidance: Tips for better relationships
- Financial Insights: Money management and abundance
- Health & Wellness: Lifestyle recommendations

Format your response with clear headings and subheadings. Provide specific, actionable advice while maintaining an empowering and positive tone. Include both strengths and growth areas, framing challenges as opportunities for development.

Remember to integrate how different numbers interact with each other and provide a holistic view of the person's numerological profile."""

    user_prompt = f"""Based on the complete numerological profile:
    - Name: {name}
    - Birth Date: {birth_date.strftime('%d-%m-%Y')}
    - Life Path Number: {profile['life_path_number']}
    - Destiny Number: {profile['destiny_number']}
    - Soul Urge Number: {profile['soul_urge_number']}
    - Personality Number: {profile['personality_number']}
    - Birthday Number: {profile['birthday_number']}
    - Maturity Number: {profile['maturity_number']}
    - Personal Year: {profile['personal_year']}
    - Karmic Lessons: {', '.join(map(str, profile['karmic_lessons']))}
    
    Please provide a comprehensive numerological analysis following the structure outlined in the system prompt. Make the analysis specific to this unique combination of numbers and their interactions."""

    try:
        g4f.debug.logging = False
        response = await g4f.ChatCompletion.create_async(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": system_prompt.format(**profile)},
                {"role": "user", "content": user_prompt}
            ],
            timeout=120
        )
        
        return {**profile, "analysis": response}
    except Exception as e:
        return {
            **profile,
            "analysis": generate_fallback_analysis(profile)
        }

def generate_fallback_analysis(profile: Dict) -> str:
    """Generate a basic analysis when API is unavailable."""
    return f"""
    <h2>Your Numerological Profile</h2>
    
    <h3>Core Numbers</h3>
    <p>Life Path Number {profile['life_path_number']}: {get_life_path_basic_meaning(profile['life_path_number'])}</p>
    <p>Destiny Number {profile['destiny_number']}: {get_destiny_basic_meaning(profile['destiny_number'])}</p>
    <p>Soul Urge Number {profile['soul_urge_number']}: Your inner motivations and desires.</p>
    <p>Personality Number {profile['personality_number']}: How others perceive you.</p>
    
    <h3>Additional Insights</h3>
    <p>Birthday Number {profile['birthday_number']}: Special talents and gifts.</p>
    <p>Maturity Number {profile['maturity_number']}: Your long-term development.</p>
    <p>Personal Year {profile['personal_year']}: Current year's theme.</p>
    
    <h3>Areas for Growth</h3>
    <p>Karmic Lessons: {', '.join(map(str, profile['karmic_lessons']))}</p>
    
    <p>Note: This is a basic analysis. The detailed analysis service is currently experiencing technical difficulties. Please try again later.</p>
    """

def get_life_path_basic_meaning(number: int) -> str:
    """Get basic meaning for Life Path numbers."""
    meanings = {
        1: "leadership, independence, and innovation",
        2: "cooperation, diplomacy, and sensitivity",
        3: "creativity, self-expression, and communication",
        4: "stability, hard work, and practical achievement",
        5: "freedom, adventure, and versatility",
        6: "responsibility, nurturing, and harmony",
        7: "analysis, wisdom, and spiritual growth",
        8: "power, abundance, and material success",
        9: "humanitarian service, compassion, and universal wisdom",
        11: "spiritual enlightenment and intuitive guidance",
        22: "master building and manifesting grand visions",
        33: "spiritual teaching and selfless service"
    }
    return meanings.get(number, "unique personal development")

def get_destiny_basic_meaning(number: int) -> str:
    """Get basic meaning for Destiny numbers."""
    meanings = {
        1: "becoming a leader and pioneer in your chosen field",
        2: "building partnerships and fostering cooperation",
        3: "expressing creativity and inspiring others",
        4: "building lasting foundations and achieving through determination",
        5: "bringing positive change and embracing freedom",
        6: "creating harmony and helping others",
        7: "seeking wisdom and sharing knowledge",
        8: "achieving material success and wielding power responsibly",
        9: "serving humanity and making a global impact",
        11: "inspiring and enlightening others",
        22: "building lasting structures that benefit humanity",
        33: "becoming a spiritual teacher and healer"
    }
    return meanings.get(number, "fulfilling your unique potential") 