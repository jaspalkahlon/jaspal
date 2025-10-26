"""
Fabric Oracle Module
Smart fabric selection based on design intent, season, and budget constraints
"""

import logging
from typing import Dict, Any, List, Optional
from ...bot.core.context import ConversationContext


class FabricOracle:
    """
    Provides intelligent fabric recommendations based on design requirements.
    Considers drape, weight, season, care, and budget.
    """

    def __init__(self, config: Dict[str, Any]):
        """
        Initialize Fabric Oracle Module

        Args:
            config: Configuration for the module
        """
        self.config = config
        self.logger = logging.getLogger(__name__)
        self.fabric_database = self._load_fabric_database()

    def _load_fabric_database(self) -> Dict[str, Any]:
        """Load comprehensive fabric database"""
        return {
            'cotton': {
                'weight': 'light to medium',
                'drape': 'moderate',
                'stretch': 'none (unless blended)',
                'best_for': ['shirts', 'dresses', 'skirts', 'casual wear'],
                'seasons': ['spring', 'summer', 'all-season'],
                'care': 'machine washable, may shrink',
                'price_range': 'budget to mid-range',
                'properties': ['breathable', 'comfortable', 'versatile'],
                'avoid_for': ['structured jackets', 'evening gowns'],
                'beginner_friendly': True
            },
            'silk': {
                'weight': 'light to medium',
                'drape': 'excellent',
                'stretch': 'slight bias stretch',
                'best_for': ['blouses', 'dresses', 'evening wear', 'linings'],
                'seasons': ['all-season'],
                'care': 'dry clean or hand wash',
                'price_range': 'mid to high-end',
                'properties': ['luxurious', 'lustrous', 'temperature-regulating'],
                'avoid_for': ['casual wear', 'children\'s clothes'],
                'beginner_friendly': False
            },
            'wool': {
                'weight': 'medium to heavy',
                'drape': 'moderate to structured',
                'stretch': 'minimal',
                'best_for': ['coats', 'jackets', 'pants', 'skirts'],
                'seasons': ['fall', 'winter'],
                'care': 'dry clean recommended',
                'price_range': 'mid to high-end',
                'properties': ['warm', 'wrinkle-resistant', 'tailorable'],
                'avoid_for': ['summer wear', 'activewear'],
                'beginner_friendly': True
            },
            'linen': {
                'weight': 'light to medium',
                'drape': 'moderate',
                'stretch': 'none',
                'best_for': ['summer dresses', 'pants', 'shirts', 'jackets'],
                'seasons': ['spring', 'summer'],
                'care': 'machine washable, wrinkles easily',
                'price_range': 'mid-range',
                'properties': ['breathable', 'crisp', 'natural texture'],
                'avoid_for': ['fitted garments', 'winter wear'],
                'beginner_friendly': True
            },
            'jersey_knit': {
                'weight': 'light to medium',
                'drape': 'fluid',
                'stretch': 'excellent (2-way or 4-way)',
                'best_for': ['t-shirts', 'dresses', 'activewear', 'loungewear'],
                'seasons': ['all-season'],
                'care': 'machine washable',
                'price_range': 'budget to mid-range',
                'properties': ['comfortable', 'stretchy', 'wrinkle-resistant'],
                'avoid_for': ['structured garments', 'tailored pieces'],
                'beginner_friendly': True
            },
            'denim': {
                'weight': 'medium to heavy',
                'drape': 'structured',
                'stretch': 'variable (depends on blend)',
                'best_for': ['jeans', 'jackets', 'skirts', 'bags'],
                'seasons': ['all-season'],
                'care': 'machine washable',
                'price_range': 'budget to mid-range',
                'properties': ['durable', 'casual', 'versatile'],
                'avoid_for': ['formal wear', 'draping'],
                'beginner_friendly': True
            },
            'chiffon': {
                'weight': 'very light',
                'drape': 'excellent',
                'stretch': 'none',
                'best_for': ['evening wear', 'overlays', 'scarves', 'blouses'],
                'seasons': ['spring', 'summer', 'special occasion'],
                'care': 'dry clean or hand wash carefully',
                'price_range': 'budget to mid-range',
                'properties': ['sheer', 'flowing', 'romantic'],
                'avoid_for': ['structured garments', 'beginner projects'],
                'beginner_friendly': False
            },
            'satin': {
                'weight': 'light to medium',
                'drape': 'excellent',
                'stretch': 'none',
                'best_for': ['evening gowns', 'lingerie', 'linings', 'formal wear'],
                'seasons': ['all-season'],
                'care': 'dry clean or hand wash',
                'price_range': 'mid to high-end',
                'properties': ['lustrous', 'smooth', 'elegant'],
                'avoid_for': ['casual wear', 'children\'s daily wear'],
                'beginner_friendly': False
            },
            'velvet': {
                'weight': 'medium to heavy',
                'drape': 'moderate',
                'stretch': 'depends on backing',
                'best_for': ['evening wear', 'jackets', 'pants', 'accessories'],
                'seasons': ['fall', 'winter', 'special occasion'],
                'care': 'dry clean',
                'price_range': 'mid to high-end',
                'properties': ['luxurious', 'textured', 'opulent'],
                'avoid_for': ['summer wear', 'beginner projects'],
                'beginner_friendly': False
            },
            'polyester': {
                'weight': 'variable',
                'drape': 'variable',
                'stretch': 'depends on weave',
                'best_for': ['lining', 'activewear', 'budget projects'],
                'seasons': ['all-season'],
                'care': 'machine washable',
                'price_range': 'budget',
                'properties': ['durable', 'wrinkle-resistant', 'affordable'],
                'avoid_for': ['luxury garments', 'hot weather (less breathable)'],
                'beginner_friendly': True
            }
        }

    def process(self, query: str, context: ConversationContext) -> str:
        """
        Process fabric-related queries

        Args:
            query: User's question about fabrics
            context: Conversation context

        Returns:
            Response string with fabric recommendations
        """
        query_lower = query.lower()

        # Check if asking about a specific fabric
        for fabric_name in self.fabric_database.keys():
            if fabric_name.replace('_', ' ') in query_lower:
                return self._fabric_details(fabric_name)

        # Check for project-based queries
        if any(word in query_lower for word in ['what fabric', 'which fabric', 'recommend', 'suggestion']):
            return self._recommend_fabric(query_lower, context)

        # Season-based queries
        if any(season in query_lower for season in ['summer', 'winter', 'spring', 'fall', 'autumn']):
            season = next(s for s in ['summer', 'winter', 'spring', 'fall'] if s in query_lower)
            return self._seasonal_fabrics(season)

        # Budget queries
        if any(word in query_lower for word in ['budget', 'cheap', 'affordable', 'expensive', 'luxury']):
            return self._budget_recommendations(query_lower)

        # Care queries
        if any(word in query_lower for word in ['care', 'wash', 'clean', 'maintain']):
            return self._fabric_care_guide()

        # Properties queries
        if any(word in query_lower for word in ['drape', 'weight', 'stretch', 'breathable']):
            return self._property_based_search(query_lower)

        return self._general_fabric_help()

    def _fabric_details(self, fabric_name: str) -> str:
        """Provide detailed information about a specific fabric"""
        fabric = self.fabric_database[fabric_name]
        display_name = fabric_name.replace('_', ' ').title()

        response = f"**{display_name} - Complete Guide**\n\n"

        response += f"**Weight:** {fabric['weight'].title()}\n"
        response += f"**Drape:** {fabric['drape'].title()}\n"
        response += f"**Stretch:** {fabric['stretch'].title()}\n"
        response += f"**Price Range:** {fabric['price_range'].title()}\n"
        response += f"**Care:** {fabric['care'].title()}\n\n"

        response += "**Best For:**\n"
        for use in fabric['best_for']:
            response += f"  • {use.title()}\n"

        response += "\n**Recommended Seasons:**\n"
        for season in fabric['seasons']:
            response += f"  • {season.title()}\n"

        response += "\n**Key Properties:**\n"
        for prop in fabric['properties']:
            response += f"  • {prop.title()}\n"

        response += "\n**Avoid For:**\n"
        for avoid in fabric['avoid_for']:
            response += f"  • {avoid.title()}\n"

        beginner_note = "✅ Beginner-friendly" if fabric['beginner_friendly'] else "⚠️ Advanced - requires experience"
        response += f"\n**Skill Level:** {beginner_note}\n"

        return response

    def _recommend_fabric(self, query: str, context: ConversationContext) -> str:
        """Recommend fabrics based on project description"""
        recommendations = []

        # Identify garment type
        garment_keywords = {
            'dress': ['dress', 'gown'],
            'shirt': ['shirt', 'blouse', 'top'],
            'pants': ['pants', 'trousers', 'jeans'],
            'jacket': ['jacket', 'coat', 'blazer'],
            'skirt': ['skirt']
        }

        garment_type = None
        for g_type, keywords in garment_keywords.items():
            if any(kw in query for kw in keywords):
                garment_type = g_type
                break

        # Search fabrics suitable for this garment
        for fabric_name, fabric_info in self.fabric_database.items():
            if garment_type:
                best_for_str = ' '.join(fabric_info['best_for'])
                if garment_type in best_for_str:
                    recommendations.append((fabric_name, fabric_info))

        if not recommendations:
            return "Could you tell me more about your project? What type of garment are you making, and what season/occasion is it for?"

        response = f"**Fabric Recommendations for Your {garment_type.title() if garment_type else 'Project'}:**\n\n"

        for fabric_name, fabric_info in recommendations[:5]:  # Top 5 recommendations
            display_name = fabric_name.replace('_', ' ').title()
            response += f"**{display_name}**\n"
            response += f"  • Weight: {fabric_info['weight'].title()}\n"
            response += f"  • Drape: {fabric_info['drape'].title()}\n"
            response += f"  • Price: {fabric_info['price_range'].title()}\n"
            response += f"  • Best properties: {', '.join(fabric_info['properties'][:3])}\n"
            if not fabric_info['beginner_friendly']:
                response += "  ⚠️ Advanced fabric\n"
            response += "\n"

        response += "Need more specific guidance? Tell me about your design vision, season, and budget!"

        return response

    def _seasonal_fabrics(self, season: str) -> str:
        """Recommend fabrics for a specific season"""
        seasonal_fabrics = []

        for fabric_name, fabric_info in self.fabric_database.items():
            if season in fabric_info['seasons'] or 'all-season' in fabric_info['seasons']:
                seasonal_fabrics.append((fabric_name, fabric_info))

        response = f"**Best Fabrics for {season.title()}:**\n\n"

        for fabric_name, fabric_info in seasonal_fabrics:
            display_name = fabric_name.replace('_', ' ').title()
            response += f"• **{display_name}**: {', '.join(fabric_info['properties'])}\n"
            response += f"  Best for: {', '.join(fabric_info['best_for'][:3])}\n\n"

        return response

    def _budget_recommendations(self, query: str) -> str:
        """Recommend fabrics based on budget"""
        if any(word in query for word in ['budget', 'cheap', 'affordable']):
            budget_range = 'budget'
        elif any(word in query for word in ['expensive', 'luxury', 'high-end']):
            budget_range = 'high-end'
        else:
            budget_range = 'mid-range'

        matching_fabrics = []
        for fabric_name, fabric_info in self.fabric_database.items():
            if budget_range in fabric_info['price_range']:
                matching_fabrics.append((fabric_name, fabric_info))

        response = f"**{budget_range.title()} Fabric Options:**\n\n"

        for fabric_name, fabric_info in matching_fabrics:
            display_name = fabric_name.replace('_', ' ').title()
            response += f"• **{display_name}**: {fabric_info['price_range'].title()}\n"
            response += f"  Great for: {', '.join(fabric_info['best_for'][:3])}\n\n"

        return response

    def _fabric_care_guide(self) -> str:
        """Provide general fabric care guidance"""
        return """**Fabric Care Guide**

**General Care by Fabric Type:**

**Machine Washable:**
• Cotton, Linen, Jersey Knit, Denim, Polyester
• Tip: Use cold water to prevent shrinkage
• Always pre-wash before sewing!

**Dry Clean Recommended:**
• Silk, Wool, Velvet, Satin (most types)
• Tip: Factor dry cleaning costs into project budget

**Hand Wash Delicates:**
• Chiffon, delicate silks, beaded fabrics
• Use gentle detergent and cool water
• Never wring - roll in towel to remove water

**Pre-Treatment Tips:**
• **Cotton & Linen:** Pre-wash and dry to prevent shrinkage
• **Wool:** Test for felting before washing
• **Silk:** Test for colorfastness
• **Synthetics:** Usually pre-wash to remove sizing

**Storage:**
• Store fabrics rolled (not folded) to prevent creases
• Keep away from direct sunlight
• Use acid-free tissue for delicate fabrics
• Climate-controlled space prevents mold/mildew

What fabric care question do you have?"""

    def _property_based_search(self, query: str) -> str:
        """Search fabrics by specific properties"""
        if 'drape' in query or 'fluid' in query or 'flow' in query:
            prop = 'drape'
            values = ['excellent', 'fluid']
        elif 'stretch' in query:
            prop = 'stretch'
            values = ['excellent', 'good']
        elif 'breathable' in query:
            return self._breathable_fabrics()
        else:
            return "What specific fabric property are you looking for? (drape, stretch, weight, breathability)"

        matching = []
        for fabric_name, fabric_info in self.fabric_database.items():
            if any(val in fabric_info.get(prop, '').lower() for val in values):
                matching.append((fabric_name, fabric_info))

        if not matching:
            return f"No fabrics found with that specific {prop}. Can you be more specific?"

        response = f"**Fabrics with Good {prop.title()}:**\n\n"
        for fabric_name, fabric_info in matching:
            display_name = fabric_name.replace('_', ' ').title()
            response += f"• **{display_name}**: {fabric_info[prop]}\n"

        return response

    def _breathable_fabrics(self) -> str:
        """List breathable fabrics"""
        return """**Most Breathable Fabrics:**

**Summer & Hot Weather:**
1. **Cotton** - Classic breathable fiber, absorbs moisture
2. **Linen** - Most breathable, perfect for hot climates
3. **Silk** - Natural temperature regulation
4. **Chambray** - Lightweight cotton weave

**Avoid in Hot Weather:**
❌ Polyester - traps heat and moisture
❌ Velvet - too insulating
❌ Heavy wool - better for cold weather

**Pro Tip:** Look for natural fibers over synthetics for maximum breathability!"""

    def _general_fabric_help(self) -> str:
        """General help for fabric queries"""
        return """**Fabric Oracle - Your Textile Guide**

I can help you choose the perfect fabric by considering:

**By Project Type:**
• Dresses, shirts, pants, jackets, etc.
• Ask: "What fabric for a summer dress?"

**By Season:**
• Spring, Summer, Fall, Winter
• Ask: "Best fabrics for winter coats?"

**By Budget:**
• Budget-friendly to luxury options
• Ask: "Affordable fabric for beginners?"

**By Properties:**
• Drape, stretch, weight, breathability
• Ask: "Fabrics with good drape?"

**Fabric Database:**
I know about: Cotton, Silk, Wool, Linen, Jersey Knit, Denim, Chiffon, Satin, Velvet, Polyester, and more!

**Ask me:**
• "What fabric should I use for [project]?"
• "Tell me about [fabric name]"
• "Best fabrics for [season]?"
• "How do I care for [fabric]?"

What fabric question can I help you with today?"""
