"""
Pattern Intelligence Module
Step-by-step guidance for pattern drafting, draping, and garment construction
"""

import logging
from typing import Dict, Any, List, Optional
from ...bot.core.context import ConversationContext


class PatternIntelligence:
    """
    Provides intelligent guidance on pattern drafting and garment construction.
    Breaks down complex techniques into manageable steps.
    """

    def __init__(self, config: Dict[str, Any]):
        """
        Initialize Pattern Intelligence Module

        Args:
            config: Configuration for the module
        """
        self.config = config
        self.logger = logging.getLogger(__name__)
        self.pattern_library = self._load_pattern_library()

    def _load_pattern_library(self) -> Dict[str, Any]:
        """Load pattern library with common garment types"""
        return {
            'bodice': {
                'measurements': ['bust', 'waist', 'shoulder_width', 'back_length'],
                'steps': [
                    'Take accurate body measurements',
                    'Draft the back bodice block',
                    'Draft the front bodice block',
                    'Add seam allowances',
                    'Create a muslin test'
                ],
                'difficulty': 'intermediate',
                'time_estimate': '3-4 hours'
            },
            'skirt': {
                'types': ['a-line', 'pencil', 'circle', 'gathered'],
                'measurements': ['waist', 'hip', 'length'],
                'steps': [
                    'Measure waist and hip circumference',
                    'Determine desired length',
                    'Calculate fabric requirements',
                    'Draft pattern based on skirt type',
                    'Add waistband and closures'
                ],
                'difficulty': 'beginner',
                'time_estimate': '2-3 hours'
            },
            'sleeve': {
                'types': ['set-in', 'raglan', 'kimono', 'dolman'],
                'measurements': ['arm_length', 'bicep', 'wrist'],
                'steps': [
                    'Determine sleeve style',
                    'Draft sleeve cap or shoulder line',
                    'Calculate sleeve width',
                    'Add ease for movement',
                    'Attach to bodice'
                ],
                'difficulty': 'intermediate',
                'time_estimate': '2-3 hours'
            },
            'pants': {
                'measurements': ['waist', 'hip', 'inseam', 'outseam', 'crotch_depth'],
                'steps': [
                    'Take comprehensive lower body measurements',
                    'Draft front pant block',
                    'Draft back pant block',
                    'Add pocket and closure details',
                    'Fit test with muslin'
                ],
                'difficulty': 'advanced',
                'time_estimate': '4-6 hours'
            },
            'dress': {
                'types': ['shift', 'fit-and-flare', 'sheath', 'wrap'],
                'measurements': ['bust', 'waist', 'hip', 'shoulder', 'length'],
                'steps': [
                    'Combine bodice and skirt blocks',
                    'Adjust for dress style',
                    'Plan closure placement',
                    'Add design details',
                    'Create full pattern'
                ],
                'difficulty': 'intermediate',
                'time_estimate': '5-7 hours'
            }
        }

    def process(self, query: str, context: ConversationContext) -> str:
        """
        Process pattern-related queries

        Args:
            query: User's question about patterns
            context: Conversation context

        Returns:
            Response string with guidance
        """
        query_lower = query.lower()

        # Identify garment type
        garment_type = self._identify_garment_type(query_lower)

        if garment_type:
            return self._provide_pattern_guidance(garment_type, query_lower, context)

        # General pattern questions
        if any(word in query_lower for word in ['measurement', 'measure', 'size']):
            return self._measurement_guidance()

        if any(word in query_lower for word in ['draft', 'draw', 'create pattern']):
            return self._drafting_guidance()

        if any(word in query_lower for word in ['ease', 'allowance', 'fit']):
            return self._ease_and_fit_guidance()

        # Default comprehensive response
        return self._general_pattern_help()

    def _identify_garment_type(self, query: str) -> Optional[str]:
        """Identify which garment type the user is asking about"""
        for garment in self.pattern_library.keys():
            if garment in query:
                return garment
        return None

    def _provide_pattern_guidance(self, garment_type: str, query: str, context: ConversationContext) -> str:
        """Provide specific guidance for a garment type"""
        pattern_info = self.pattern_library[garment_type]
        skill_level = context.get_user_skill_level()

        response = f"**{garment_type.title()} Pattern Guidance**\n\n"

        # Add difficulty warning if needed
        if pattern_info['difficulty'] == 'advanced' and skill_level == 'beginner':
            response += "⚠️ This is an advanced pattern. Consider practicing with simpler garments first.\n\n"

        # Required measurements
        response += "**Required Measurements:**\n"
        for measurement in pattern_info['measurements']:
            response += f"  • {measurement.replace('_', ' ').title()}\n"

        response += f"\n**Estimated Time:** {pattern_info['time_estimate']}\n"
        response += f"**Difficulty Level:** {pattern_info['difficulty'].title()}\n\n"

        # Step-by-step process
        response += "**Step-by-Step Process:**\n"
        for i, step in enumerate(pattern_info['steps'], 1):
            response += f"{i}. {step}\n"

        # Add types if available
        if 'types' in pattern_info:
            response += f"\n**Common {garment_type.title()} Types:**\n"
            for style in pattern_info['types']:
                response += f"  • {style.title()}\n"

        response += "\n💡 **Pro Tip:** Always make a muslin (test garment) first to check fit before cutting your final fabric!"

        return response

    def _measurement_guidance(self) -> str:
        """Provide guidance on taking measurements"""
        return """**Taking Accurate Measurements**

For professional results, follow these measurement guidelines:

**Body Measurements:**
1. **Bust/Chest:** Measure around the fullest part of the bust, keeping tape parallel to floor
2. **Waist:** Measure at natural waistline (bend to the side to find it)
3. **Hip:** Measure around fullest part, usually 7-9" below waist
4. **Shoulder Width:** From shoulder point to shoulder point across back
5. **Arm Length:** From shoulder point to wrist with arm slightly bent

**Key Tips:**
• Use a flexible measuring tape
• Wear fitted clothing or undergarments
• Keep tape snug but not tight
• Measure twice for accuracy
• Record measurements immediately
• Take measurements every 6 months (bodies change!)

**Ease Allowance:**
Different garments require different amounts of ease:
• Close-fitting: 0-2" ease
• Fitted: 2-4" ease
• Semi-fitted: 4-6" ease
• Loose: 6"+ ease

Would you like guidance on a specific garment type?"""

    def _drafting_guidance(self) -> str:
        """Provide guidance on pattern drafting techniques"""
        return """**Pattern Drafting Basics**

**Essential Tools:**
• Pattern paper or butcher paper
• Clear ruler and curved rulers (French curve, hip curve)
• L-square or right angle ruler
• Pencils and eraser
• Measuring tape
• Tracing wheel
• Pattern weights or pins

**Basic Drafting Process:**
1. **Prepare Your Space:** Large flat surface with good lighting
2. **Start with a Block:** Begin with basic body block (sloper)
3. **Transfer Measurements:** Use your measurement chart
4. **Draw Straight Lines First:** Use ruler for all straight edges
5. **Add Curves:** Use French curves for armholes, necklines
6. **Mark Grain Lines:** Essential for proper drape
7. **Add Notches:** For matching seams accurately
8. **Label Everything:** Piece name, size, grain line, # to cut

**Common Drafting Mistakes to Avoid:**
❌ Forgetting seam allowances
❌ Not marking grain lines
❌ Skipping the muslin test
❌ Using poor quality paper
❌ Not labeling pattern pieces

**Next Steps:** Which garment would you like to draft? I can provide specific instructions."""

    def _ease_and_fit_guidance(self) -> str:
        """Provide guidance on ease and fit"""
        return """**Understanding Ease and Fit**

**What is Ease?**
Ease is the difference between body measurements and garment measurements. It allows for movement and determines the garment's fit style.

**Types of Ease:**

1. **Wearing Ease** (Minimum for movement)
   • Bust/Chest: 2-3"
   • Waist: 1"
   • Hip: 2-3"

2. **Design Ease** (Style preference)
   • Fitted: 0-2" beyond wearing ease
   • Semi-fitted: 2-4" beyond wearing ease
   • Loose: 4-8" beyond wearing ease
   • Oversized: 8"+ beyond wearing ease

**Fit Adjustment Tips:**

**If garment is too tight:**
• Check ease allowances
• Add to side seams
• Adjust darts (smaller or relocated)
• Use stretch fabric

**If garment is too loose:**
• Take in side seams
• Adjust darts (larger or add more)
• Add waist shaping
• Consider smaller size

**Common Fit Issues:**
• **Pulling across bust** → Increase bust ease or adjust dart placement
• **Gaping neckline** → Reduce neckline width or add darts
• **Tight sleeves** → Add bicep ease or adjust cap height
• **Pulling at hip** → Increase hip ease or adjust side seams

Need help with a specific fit issue? Describe what you're experiencing!"""

    def _general_pattern_help(self) -> str:
        """General help for pattern-related questions"""
        return """**Pattern Intelligence Module**

I can help you with:

**Pattern Drafting:**
• Step-by-step guidance for bodices, skirts, sleeves, pants, and dresses
• Measurement techniques
• Block/sloper creation
• Pattern grading

**Garment Construction:**
• Assembly instructions
• Seam techniques
• Finishing methods
• Professional details

**Fit & Adjustment:**
• Ease calculations
• Common fit issues
• Alteration techniques
• Body type considerations

**Available Patterns:**
• Bodice (Intermediate)
• Skirt (Beginner)
• Sleeve (Intermediate)
• Pants (Advanced)
• Dress (Intermediate)

What would you like to work on today? Ask me about a specific garment or technique!"""
