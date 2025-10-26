"""
Color Psychology Tool
Beyond basic palettes - understanding cultural color narratives
"""

import logging
from typing import Dict, Any, List, Optional
from ...bot.core.context import ConversationContext


class ColorPsychologyTool:
    """
    Provides color theory, psychology, and cultural context for fashion design.
    Goes beyond basic palettes to understand emotional and cultural impact.
    """

    def __init__(self, config: Dict[str, Any]):
        """
        Initialize Color Psychology Tool

        Args:
            config: Configuration for the module
        """
        self.config = config
        self.logger = logging.getLogger(__name__)
        self.color_database = self._load_color_database()
        self.color_schemes = self._load_color_schemes()

    def _load_color_database(self) -> Dict[str, Any]:
        """Load comprehensive color psychology database"""
        return {
            'red': {
                'psychology': {
                    'emotions': ['passion', 'energy', 'excitement', 'power', 'danger', 'love'],
                    'effects': 'Increases heart rate, creates urgency, demands attention',
                    'personality': 'Bold, confident, energetic, passionate'
                },
                'cultural_meanings': {
                    'western': 'Love, passion, danger, excitement',
                    'eastern': 'Good fortune, joy, celebration (China)',
                    'south_africa': 'Mourning',
                    'india': 'Purity, fertility, love'
                },
                'fashion_use': {
                    'best_for': ['statement pieces', 'evening wear', 'power dressing', 'athletic wear'],
                    'avoid_for': ['job interviews (too aggressive)', 'minimalist looks', 'serene settings'],
                    'styling_tips': [
                        'Use as accent color for impact',
                        'Pair with neutrals to balance intensity',
                        'Consider your skin tone (cool vs warm reds)',
                        'Perfect for confidence boost'
                    ]
                },
                'complementary': ['green', 'teal'],
                'analogous': ['orange', 'pink'],
                'skin_tone_match': {
                    'warm': 'tomato red, orange-red',
                    'cool': 'blue-red, burgundy',
                    'neutral': 'true red, cherry red'
                }
            },
            'blue': {
                'psychology': {
                    'emotions': ['calm', 'trust', 'stability', 'sadness', 'serenity', 'intelligence'],
                    'effects': 'Lowers heart rate, promotes calmness, enhances focus',
                    'personality': 'Trustworthy, peaceful, professional, reliable'
                },
                'cultural_meanings': {
                    'western': 'Trust, masculinity, corporate',
                    'middle_east': 'Protection, spirituality',
                    'global': 'Most universally liked color'
                },
                'fashion_use': {
                    'best_for': ['business wear', 'denim', 'corporate settings', 'calming environments'],
                    'avoid_for': ['making bold statements (use brighter shades)', 'very creative/artistic events'],
                    'styling_tips': [
                        'Navy is the new black - incredibly versatile',
                        'Perfect for professional settings',
                        'Pair with white for classic look',
                        'Use bright blues for summer energy'
                    ]
                },
                'complementary': ['orange', 'coral'],
                'analogous': ['purple', 'green'],
                'skin_tone_match': {
                    'warm': 'turquoise, teal, periwinkle',
                    'cool': 'royal blue, navy, sapphire',
                    'neutral': 'most blues work well'
                }
            },
            'yellow': {
                'psychology': {
                    'emotions': ['happiness', 'optimism', 'creativity', 'caution', 'cheerfulness'],
                    'effects': 'Stimulates mental activity, generates energy, attention-grabbing',
                    'personality': 'Optimistic, creative, friendly, energetic'
                },
                'cultural_meanings': {
                    'western': 'Happiness, caution',
                    'asia': 'Sacred, imperial (China)',
                    'egypt': 'Mourning',
                    'greece': 'Sadness'
                },
                'fashion_use': {
                    'best_for': ['spring/summer wear', 'accessories', 'mood-boosting outfits', 'creative events'],
                    'avoid_for': ['large areas (can be overwhelming)', 'formal evening wear', 'muted looks'],
                    'styling_tips': [
                        'Most challenging color to wear - choose right shade',
                        'Mustard and golden yellows are more wearable',
                        'Use as accent or accessory color',
                        'Pair with navy or gray to ground it'
                    ]
                },
                'complementary': ['purple', 'violet'],
                'analogous': ['orange', 'green'],
                'skin_tone_match': {
                    'warm': 'golden yellow, mustard',
                    'cool': 'lemon yellow, pale yellow',
                    'neutral': 'buttercup, sunflower'
                }
            },
            'green': {
                'psychology': {
                    'emotions': ['nature', 'growth', 'harmony', 'freshness', 'balance', 'renewal'],
                    'effects': 'Reduces stress, promotes balance, refreshing',
                    'personality': 'Balanced, natural, growth-oriented, peaceful'
                },
                'cultural_meanings': {
                    'western': 'Nature, money, envy',
                    'ireland': 'National color, luck',
                    'islam': 'Sacred color',
                    'china': 'Infidelity (green hat)'
                },
                'fashion_use': {
                    'best_for': ['spring wear', 'outdoor events', 'natural/eco fashion', 'balancing outfits'],
                    'avoid_for': ['formal business (varies by culture)', 'overly sophisticated looks'],
                    'styling_tips': [
                        'Emerald and sage are sophisticated choices',
                        'Pairs beautifully with earth tones',
                        'Use olive for military/utility vibes',
                        'Mint for fresh, spring looks'
                    ]
                },
                'complementary': ['red', 'pink'],
                'analogous': ['blue', 'yellow'],
                'skin_tone_match': {
                    'warm': 'olive, moss, lime',
                    'cool': 'emerald, teal, mint',
                    'neutral': 'sage, forest, jade'
                }
            },
            'purple': {
                'psychology': {
                    'emotions': ['luxury', 'wisdom', 'spirituality', 'creativity', 'mystery', 'royalty'],
                    'effects': 'Inspires creativity, adds luxury, can be calming or energizing',
                    'personality': 'Creative, wise, spiritual, unique'
                },
                'cultural_meanings': {
                    'western': 'Royalty, luxury, spirituality',
                    'thailand': 'Mourning (widows)',
                    'brazil': 'Death, mourning',
                    'historical': 'Wealth (purple dye was expensive)'
                },
                'fashion_use': {
                    'best_for': ['evening wear', 'creative events', 'statement pieces', 'luxury items'],
                    'avoid_for': ['conservative business (depends on shade)', 'minimalist looks'],
                    'styling_tips': [
                        'Lavender for soft, romantic looks',
                        'Deep purple for luxury and drama',
                        'Pair with gray or beige for sophistication',
                        'Use as accent for creativity'
                    ]
                },
                'complementary': ['yellow', 'gold'],
                'analogous': ['blue', 'red'],
                'skin_tone_match': {
                    'warm': 'warm purple, plum, mauve',
                    'cool': 'lavender, violet, royal purple',
                    'neutral': 'most purples work'
                }
            },
            'black': {
                'psychology': {
                    'emotions': ['power', 'elegance', 'sophistication', 'mystery', 'authority'],
                    'effects': 'Creates slimming effect, adds formality, commands respect',
                    'personality': 'Sophisticated, powerful, elegant, mysterious'
                },
                'cultural_meanings': {
                    'western': 'Mourning, formality, elegance',
                    'asia': 'Career success, knowledge',
                    'universal': 'Most versatile fashion color'
                },
                'fashion_use': {
                    'best_for': ['formal events', 'evening wear', 'professional settings', 'slimming effect'],
                    'avoid_for': ['daytime summer events (absorbs heat)', 'very casual beach settings'],
                    'styling_tips': [
                        'The ultimate wardrobe staple',
                        'All-black for sleek, modern look',
                        'Mix textures when wearing all black',
                        'Add color through accessories'
                    ]
                },
                'complementary': ['white', 'gold', 'silver'],
                'analogous': ['gray', 'charcoal'],
                'skin_tone_match': {
                    'warm': 'soft black, charcoal',
                    'cool': 'true black works beautifully',
                    'neutral': 'all blacks work well'
                }
            },
            'white': {
                'psychology': {
                    'emotions': ['purity', 'cleanliness', 'simplicity', 'innocence', 'peace'],
                    'effects': 'Creates spaciousness, promotes clarity, feels fresh',
                    'personality': 'Pure, simple, clean, peaceful'
                },
                'cultural_meanings': {
                    'western': 'Weddings, purity, peace',
                    'eastern': 'Mourning, funerals (China, Korea)',
                    'india': 'Mourning, but also worn by widows',
                    'medical': 'Cleanliness, sterility'
                },
                'fashion_use': {
                    'best_for': ['summer wear', 'weddings', 'minimalist looks', 'fresh, clean aesthetics'],
                    'avoid_for': ['messy activities', 'very formal dark-tie events'],
                    'styling_tips': [
                        'All-white for summer chic',
                        'Mix textures to add interest',
                        'Consider maintenance (shows stains)',
                        'Pair with any color for freshness'
                    ]
                },
                'complementary': ['black', 'any color'],
                'analogous': ['cream', 'ivory', 'beige'],
                'skin_tone_match': {
                    'warm': 'cream, ivory, off-white',
                    'cool': 'bright white, pure white',
                    'neutral': 'all whites work'
                }
            },
            'pink': {
                'psychology': {
                    'emotions': ['love', 'nurturing', 'femininity', 'playfulness', 'youth'],
                    'effects': 'Calming, comforting, can feel nurturing or playful',
                    'personality': 'Nurturing, romantic, playful, optimistic'
                },
                'cultural_meanings': {
                    'western': 'Femininity, romance, youth',
                    'japan': 'Masculinity (cherry blossoms)',
                    'modern': 'Shifting away from strict gender associations'
                },
                'fashion_use': {
                    'best_for': ['spring wear', 'romantic looks', 'playful outfits', 'skin-flattering colors'],
                    'avoid_for': ['overly serious business settings (depends on shade)', 'ultra-masculine looks'],
                    'styling_tips': [
                        'Millennial pink for sophisticated look',
                        'Hot pink for bold statements',
                        'Blush pink for subtle femininity',
                        'Pair with gray for modern elegance'
                    ]
                },
                'complementary': ['green', 'teal'],
                'analogous': ['red', 'purple'],
                'skin_tone_match': {
                    'warm': 'coral pink, peachy pink',
                    'cool': 'rose pink, fuchsia',
                    'neutral': 'dusty pink, blush'
                }
            },
            'orange': {
                'psychology': {
                    'emotions': ['enthusiasm', 'creativity', 'warmth', 'energy', 'vitality'],
                    'effects': 'Stimulating, energizing, promotes enthusiasm',
                    'personality': 'Energetic, creative, friendly, adventurous'
                },
                'cultural_meanings': {
                    'western': 'Energy, autumn, Halloween',
                    'netherlands': 'National color, royalty',
                    'hinduism': 'Sacred color',
                    'buddhism': 'Humility, monk robes'
                },
                'fashion_use': {
                    'best_for': ['fall wear', 'creative settings', 'energetic looks', 'accessories'],
                    'avoid_for': ['conservative business', 'subtle, understated looks'],
                    'styling_tips': [
                        'Rust and terracotta for wearability',
                        'Burnt orange for fall sophistication',
                        'Use as accent color',
                        'Pair with navy or denim'
                    ]
                },
                'complementary': ['blue', 'teal'],
                'analogous': ['red', 'yellow'],
                'skin_tone_match': {
                    'warm': 'warm orange, tangerine, rust',
                    'cool': 'coral orange, peachy orange',
                    'neutral': 'burnt orange, terracotta'
                }
            },
            'brown': {
                'psychology': {
                    'emotions': ['stability', 'earthiness', 'comfort', 'reliability', 'warmth'],
                    'effects': 'Grounding, comforting, creates sense of security',
                    'personality': 'Reliable, stable, down-to-earth, comfortable'
                },
                'cultural_meanings': {
                    'universal': 'Earth, nature, stability',
                    'western': 'Simplicity, outdoors',
                    'generally': 'Less symbolic, more practical'
                },
                'fashion_use': {
                    'best_for': ['fall/winter', 'leather goods', 'earth-tone palettes', 'casual wear'],
                    'avoid_for': ['bright summer looks', 'formal evening wear (use rich browns)'],
                    'styling_tips': [
                        'Chocolate brown is sophisticated',
                        'Camel and tan for luxury feel',
                        'Mix with cream for monochromatic elegance',
                        'Great for leather accessories'
                    ]
                },
                'complementary': ['blue', 'teal'],
                'analogous': ['orange', 'beige', 'tan'],
                'skin_tone_match': {
                    'warm': 'warm browns, camel, tan',
                    'cool': 'taupe, cooler browns',
                    'neutral': 'most browns work well'
                }
            }
        }

    def _load_color_schemes(self) -> Dict[str, Any]:
        """Load color harmony schemes"""
        return {
            'monochromatic': {
                'description': 'Variations of a single color (tints, tones, shades)',
                'effect': 'Harmonious, sophisticated, easy to pull off',
                'example': 'All blues: navy pants, sky blue shirt, pale blue accessories',
                'tips': 'Vary the intensity and value for interest'
            },
            'complementary': {
                'description': 'Colors opposite on the color wheel',
                'effect': 'High contrast, vibrant, energetic',
                'example': 'Blue and orange, red and green, purple and yellow',
                'tips': 'Use one as dominant, other as accent'
            },
            'analogous': {
                'description': 'Colors next to each other on the wheel',
                'effect': 'Harmonious, pleasing, cohesive',
                'example': 'Blue, blue-green, green',
                'tips': 'Choose one dominant color'
            },
            'triadic': {
                'description': 'Three colors evenly spaced on the wheel',
                'effect': 'Balanced, vibrant, playful',
                'example': 'Red, yellow, blue (primary) or orange, green, purple (secondary)',
                'tips': 'Use one as dominant, others as accents'
            },
            'neutral': {
                'description': 'Black, white, gray, beige, brown',
                'effect': 'Versatile, timeless, sophisticated',
                'example': 'All-black, gray and white, beige tones',
                'tips': 'Mix textures and add metallic accents for interest'
            }
        }

    def process(self, query: str, context: ConversationContext) -> str:
        """
        Process color-related queries

        Args:
            query: User's question about color
            context: Conversation context

        Returns:
            Response string with color guidance
        """
        query_lower = query.lower()

        # Check for specific color inquiries
        for color_name in self.color_database.keys():
            if color_name in query_lower:
                return self._detailed_color_analysis(color_name)

        # Color combination/palette queries
        if any(phrase in query_lower for phrase in ['combination', 'palette', 'go with', 'match', 'pair']):
            return self._color_combination_guide(query_lower)

        # Color scheme queries
        for scheme_name in self.color_schemes.keys():
            if scheme_name in query_lower:
                return self._color_scheme_guide(scheme_name)

        # Skin tone queries
        if any(phrase in query_lower for phrase in ['skin tone', 'skin color', 'complexion', 'flattering']):
            return self._skin_tone_color_guide()

        # Cultural meaning queries
        if any(word in query_lower for word in ['culture', 'cultural', 'meaning', 'symbolism']):
            return self._cultural_color_guide()

        # Psychology queries
        if any(word in query_lower for word in ['psychology', 'emotion', 'feeling', 'mood', 'effect']):
            return self._color_psychology_guide()

        return self._general_color_help()

    def _detailed_color_analysis(self, color_name: str) -> str:
        """Provide detailed analysis of a specific color"""
        color = self.color_database[color_name]

        response = f"**{color_name.title()} - Complete Color Analysis**\n\n"

        # Psychology
        psych = color['psychology']
        response += "**Psychological Impact:**\n"
        response += f"Emotions: {', '.join(psych['emotions']).title()}\n"
        response += f"Effects: {psych['effects']}\n"
        response += f"Personality: {psych['personality']}\n\n"

        # Cultural meanings
        response += "**Cultural Meanings:**\n"
        for culture, meaning in color['cultural_meanings'].items():
            response += f"  • {culture.replace('_', ' ').title()}: {meaning}\n"

        # Fashion use
        fashion = color['fashion_use']
        response += "\n**Fashion Applications:**\n"
        response += f"Best for: {', '.join(fashion['best_for'])}\n"
        response += f"Avoid for: {', '.join(fashion['avoid_for'])}\n\n"

        response += "**Styling Tips:**\n"
        for tip in fashion['styling_tips']:
            response += f"  • {tip}\n"

        # Color combinations
        response += f"\n**Color Pairings:**\n"
        response += f"Complementary: {', '.join(color['complementary']).title()}\n"
        response += f"Analogous: {', '.join(color['analogous']).title()}\n\n"

        # Skin tone matching
        response += "**Best Shades for Your Skin Tone:**\n"
        for tone, shades in color['skin_tone_match'].items():
            response += f"  • {tone.title()} skin: {shades.title()}\n"

        return response

    def _color_combination_guide(self, query: str) -> str:
        """Guide on color combinations"""
        response = "**Color Combination Guide**\n\n"

        response += "**Classic Combinations That Always Work:**\n\n"

        combinations = [
            ('Navy & White', 'Timeless nautical, crisp and clean'),
            ('Black & Gold', 'Luxury and elegance'),
            ('Gray & Pink', 'Modern and sophisticated'),
            ('Camel & Black', 'Chic and polished'),
            ('Denim & White', 'Casual perfection'),
            ('Red & Navy', 'Bold yet balanced'),
            ('Olive & Cream', 'Earthy sophistication'),
            ('Burgundy & Tan', 'Rich autumn palette')
        ]

        for combo, desc in combinations:
            response += f"  • **{combo}**: {desc}\n"

        response += "\n**Color Harmony Rules:**\n"
        response += "1. **60-30-10 Rule**: 60% dominant color, 30% secondary, 10% accent\n"
        response += "2. **Neutral Bridge**: Use neutrals to connect bold colors\n"
        response += "3. **Temperature Matching**: Warm colors with warm, cool with cool\n"
        response += "4. **Value Contrast**: Mix light and dark for visual interest\n\n"

        response += "**When Combining Colors:**\n"
        response += "  • Start with one statement color\n"
        response += "  • Add neutrals for balance\n"
        response += "  • Use color wheel for harmonious pairings\n"
        response += "  • Consider the occasion and message\n"
        response += "  • Test combinations before committing\n\n"

        response += "Need specific color pairing advice? Tell me which colors you want to combine!"

        return response

    def _color_scheme_guide(self, scheme_name: str) -> str:
        """Guide on a specific color scheme"""
        scheme = self.color_schemes[scheme_name]

        response = f"**{scheme_name.title()} Color Scheme**\n\n"
        response += f"**What It Is:**\n{scheme['description']}\n\n"
        response += f"**Visual Effect:**\n{scheme['effect']}\n\n"
        response += f"**Example:**\n{scheme['example']}\n\n"
        response += f"**Styling Tips:**\n{scheme['tips']}\n\n"

        response += "**How to Create This Look:**\n"

        if scheme_name == 'monochromatic':
            response += "1. Choose your base color\n"
            response += "2. Select lighter tints (add white)\n"
            response += "3. Select darker shades (add black)\n"
            response += "4. Vary textures for dimension\n"
            response += "5. Add metallics or neutrals as accents\n"

        elif scheme_name == 'complementary':
            response += "1. Choose your main color (60%)\n"
            response += "2. Use complementary color for accents (10-30%)\n"
            response += "3. Add neutrals to balance intensity\n"
            response += "4. Adjust saturation if too vibrant\n"
            response += "5. Use one color dominantly\n"

        elif scheme_name == 'analogous':
            response += "1. Select 3 adjacent colors on wheel\n"
            response += "2. Choose one as dominant\n"
            response += "3. Use others for supporting roles\n"
            response += "4. Keep proportions balanced\n"
            response += "5. Add neutral to ground the look\n"

        return response

    def _skin_tone_color_guide(self) -> str:
        """Guide on choosing colors for skin tone"""
        return """**Choosing Colors for Your Skin Tone**

**Determine Your Undertone:**

**Warm Undertones:**
• Veins appear greenish
• Gold jewelry flatters you
• You tan easily
• Your skin has yellow, peachy, or golden cast

**Cool Undertones:**
• Veins appear bluish
• Silver jewelry flatters you
• You burn easily
• Your skin has pink, red, or bluish cast

**Neutral Undertones:**
• Veins appear blue-green
• Both gold and silver look good
• You tan moderately
• Balanced skin tone

---

**Colors for Warm Undertones:**
• **Best Colors**: Warm reds, oranges, yellows, olive green, warm browns, camel, coral, peach
• **Avoid**: Icy colors, stark whites, cool blues
• **Neutrals**: Cream, beige, warm gray, chocolate brown

**Colors for Cool Undertones:**
• **Best Colors**: Blue-reds, cool blues, purples, emerald green, magenta, lavender
• **Avoid**: Orange, yellow-greens, warm browns
• **Neutrals**: Pure white, gray, navy, charcoal

**Colors for Neutral Undertones:**
• **Lucky You!**: Most colors work
• **Best Colors**: Soft colors in both warm and cool tones
• **Strategy**: Experiment with both palettes
• **Neutrals**: All neutrals work well

---

**Universal Flattering Colors:**
• **Teal**: Works for almost everyone
• **Purple/Plum**: Universally flattering
• **Soft Pink**: Brightens most skin tones
• **Navy**: Classic that suits all

**Pro Tips:**
1. Hold colors near your face in natural light
2. Notice if color brightens or dulls your skin
3. Don't let rules restrict you - wear what you love!
4. Adjust shades within a color family to find your perfect match

Want to know which shade of a specific color suits you? Just ask!"""

    def _cultural_color_guide(self) -> str:
        """Guide on cultural color meanings"""
        return """**Cultural Color Meanings in Fashion**

Understanding color symbolism helps create culturally sensitive designs:

**Red:**
• Western: Passion, love, danger
• China/India: Luck, celebration, weddings
• South Africa: Mourning color
• **Fashion note**: Consider context when designing for global markets

**White:**
• Western: Purity, weddings, peace
• Eastern (China, Korea, India): Mourning, funerals
• **Fashion note**: White wedding dresses aren't universal

**Black:**
• Western: Mourning, formality, elegance
• Many cultures: Sophistication, authority
• **Fashion note**: Most universally accepted for formal wear

**Yellow:**
• China: Imperial, sacred, prosperity
• Egypt/Greece: Associated with mourning
• Western: Happiness, caution
• **Fashion note**: Context matters greatly

**Purple:**
• Historically: Royalty, luxury (expensive dye)
• Thailand: Mourning (widows)
• Western: Creativity, luxury
• **Fashion note**: Often associated with high status

**Green:**
• Islam: Sacred, paradise
• Ireland: National identity
• Western: Nature, money
• **Fashion note**: Varies widely by region

**Blue:**
• Nearly universal: Trust, calm
• Middle East: Protection
• **Fashion note**: Safest color internationally

---

**Design Considerations:**

**For Global Markets:**
1. Research target culture's color associations
2. Test color palettes with cultural consultants
3. Consider religious and traditional meanings
4. Be aware of color in branding and messaging

**For Multicultural Events:**
1. Choose universally positive colors (blue, purple)
2. Avoid colors with strong negative associations
3. Consider color combinations, not just individual colors
4. When in doubt, ask or research

**Remember:**
• Context matters (wedding vs. funeral)
• Trends can shift cultural meanings
• Personal preference transcends cultural "rules"
• Fashion is increasingly global and mixed

Designing for a specific culture or event? Tell me more!"""

    def _color_psychology_guide(self) -> str:
        """General color psychology guide"""
        return """**Color Psychology in Fashion**

Colors communicate before words do. Here's how to use color psychology:

**Energy Levels:**

**High Energy Colors:**
• Red, Orange, Bright Yellow
• Use for: Confidence, energy, attention
• Avoid when: Seeking calm, subtlety

**Moderate Energy:**
• Green, Purple, Pink
• Use for: Balance, creativity, approachability
• Versatile for most occasions

**Low Energy/Calming:**
• Blue, Gray, Soft Neutrals
• Use for: Trust, professionalism, calm
• Perfect for: Stressful situations, interviews

---

**Emotional Messaging:**

**To Convey Power/Authority:**
• Black, Navy, Charcoal
• Sharp tailoring enhances effect

**To Appear Approachable:**
• Soft blues, greens, warm neutrals
• Avoid overly dark or bright

**To Show Creativity:**
• Purple, unique color combinations
• Unexpected pairings

**To Build Trust:**
• Blue (especially navy), white
• Professional settings

**To Express Joy/Optimism:**
• Yellow, bright colors, warm tones
• Social and casual settings

---

**Practical Applications:**

**Job Interview:**
• Navy or gray (trust, professionalism)
• Add subtle color for personality

**First Date:**
• Red (passion - use carefully)
• Pink or purple (romantic)
• Blue (approachable)

**Creative Presentation:**
• Purple (creativity)
• Unexpected combinations
• Avoid all-black (too corporate)

**Difficult Conversation:**
• Calm colors (blue, soft gray)
• Avoid aggressive reds

**Confidence Boost:**
• Your "power color" (what makes YOU feel good)
• Often red, but personal preference matters most

---

**The Most Important Rule:**
Wear colors that make YOU feel confident and comfortable. Psychology is a guide, not a rule book!

What emotion or message do you want to convey with color?"""

    def _general_color_help(self) -> str:
        """General color help"""
        return """**Color Psychology Tool**

I help you understand and use color beyond basic aesthetics!

**What I Offer:**

**Color Analysis:**
• Psychological effects
• Emotional impact
• Cultural meanings
• Fashion applications

**I Know About These Colors:**
Red, Blue, Yellow, Green, Purple, Pink, Orange, Brown, Black, White

**Color Combinations:**
• Harmonious palettes
• Color wheel principles
• Classic combinations
• Modern pairings

**Color Schemes:**
• Monochromatic
• Complementary
• Analogous
• Triadic
• Neutral

**Personal Color Guidance:**
• Skin tone matching
• Flattering shades
• Color confidence building

**Cultural Context:**
• Global color meanings
• Symbolic significance
• Cross-cultural considerations

**Ask Me:**
• "What does [color] mean?"
• "What colors go with [color]?"
• "What colors suit my [warm/cool/neutral] skin tone?"
• "What color should I wear for [occasion]?"
• "Tell me about [color scheme] palette"

What color question can I help with today?"""
