"""
Design Critique System
Socratic questioning that develops critical thinking, not just validation
"""

import logging
from typing import Dict, Any, List
from ...bot.core.context import ConversationContext


class DesignCritiqueSystem:
    """
    Provides thoughtful design critique using Socratic method.
    Develops critical thinking rather than just validating ideas.
    """

    def __init__(self, config: Dict[str, Any]):
        """
        Initialize Design Critique System

        Args:
            config: Configuration for the module
        """
        self.config = config
        self.logger = logging.getLogger(__name__)
        self.critique_framework = self._load_critique_framework()

    def _load_critique_framework(self) -> Dict[str, Any]:
        """Load design critique framework"""
        return {
            'design_principles': {
                'balance': {
                    'questions': [
                        'Where does your eye go first?',
                        'Is visual weight distributed intentionally?',
                        'Are there areas that feel too heavy or too light?'
                    ],
                    'considerations': ['symmetrical vs asymmetrical', 'color weight', 'pattern distribution', 'visual hierarchy']
                },
                'proportion': {
                    'questions': [
                        'How do the garment proportions relate to the body?',
                        'What is the relationship between upper and lower body?',
                        'Are you using the golden ratio or rule of thirds?'
                    ],
                    'considerations': ['body balance', 'silhouette harmony', 'detail scale', 'length relationships']
                },
                'emphasis': {
                    'questions': [
                        'What is the focal point of your design?',
                        'How are you drawing attention to this area?',
                        'Is there a clear hierarchy of importance?'
                    ],
                    'considerations': ['color contrast', 'placement', 'detail concentration', 'texture variation']
                },
                'rhythm': {
                    'questions': [
                        'Is there visual movement in your design?',
                        'How do patterns or details repeat?',
                        'Does the eye flow smoothly through the design?'
                    ],
                    'considerations': ['repetition', 'pattern flow', 'seam lines', 'detail placement']
                },
                'unity': {
                    'questions': [
                        'Do all elements work together cohesively?',
                        'What ties the design together?',
                        'Is there a consistent theme or concept?'
                    ],
                    'considerations': ['color palette consistency', 'style coherence', 'material harmony', 'concept clarity']
                }
            },
            'critique_aspects': {
                'concept': {
                    'questions': [
                        'What inspired this design?',
                        'What story are you telling?',
                        'Who is your target wearer?',
                        'What problem does this solve or need does it fill?',
                        'How does this fit into current or future trends?'
                    ],
                    'depth_indicators': ['clear inspiration', 'defined audience', 'intentional choices', 'conceptual coherence']
                },
                'functionality': {
                    'questions': [
                        'How will this garment move with the body?',
                        'Is it appropriate for its intended use?',
                        'Have you considered ease and comfort?',
                        'How will closures and fastenings work?',
                        'Is it practical for your target wearer\'s lifestyle?'
                    ],
                    'depth_indicators': ['movement consideration', 'practical details', 'wearability', 'user needs']
                },
                'construction': {
                    'questions': [
                        'How will you construct this design?',
                        'What construction challenges might you face?',
                        'Are your fabric choices appropriate for the design?',
                        'Have you considered how seams will look and feel?',
                        'What finishing techniques will you use?'
                    ],
                    'depth_indicators': ['technical feasibility', 'material suitability', 'construction logic', 'finish quality']
                },
                'innovation': {
                    'questions': [
                        'What makes this design unique?',
                        'Are you challenging any conventions? Why or why not?',
                        'How does this differ from existing designs?',
                        'What\'s your original contribution?',
                        'Is innovation serving the design or just being different?'
                    ],
                    'depth_indicators': ['originality', 'purposeful innovation', 'market differentiation', 'creative risk']
                },
                'aesthetics': {
                    'questions': [
                        'What visual impact do you want to create?',
                        'How do colors, textures, and shapes work together?',
                        'What is the overall mood or feeling?',
                        'Does the aesthetic match the concept?',
                        'Who will find this beautiful and why?'
                    ],
                    'depth_indicators': ['visual coherence', 'intentional aesthetics', 'emotional impact', 'target appeal']
                },
                'sustainability': {
                    'questions': [
                        'What is the environmental impact of your materials?',
                        'How long will this garment last?',
                        'Can it be repaired or recycled?',
                        'Are you considering ethical production?',
                        'Does the design encourage sustainable consumption?'
                    ],
                    'depth_indicators': ['material consciousness', 'longevity', 'ethical awareness', 'environmental consideration']
                }
            },
            'critique_levels': {
                'beginner': {
                    'focus': ['concept clarity', 'basic proportions', 'color harmony', 'construction feasibility'],
                    'approach': 'Encouraging, supportive, educational',
                    'questions_per_session': 3-5
                },
                'intermediate': {
                    'focus': ['design principles', 'innovation', 'market awareness', 'technical execution'],
                    'approach': 'Challenging, thought-provoking, skill-building',
                    'questions_per_session': 5-7
                },
                'advanced': {
                    'focus': ['conceptual depth', 'cultural context', 'industry viability', 'artistic voice'],
                    'approach': 'Professional, rigorous, industry-standard',
                    'questions_per_session': 7-10
                }
            },
            'feedback_types': {
                'constructive': 'What works + what could improve + specific suggestions',
                'socratic': 'Questions that guide designer to own answers',
                'comparative': 'Reference to existing work or historical context',
                'technical': 'Specific construction or material guidance',
                'conceptual': 'Big-picture thinking and design philosophy'
            }
        }

    def process(self, query: str, context: ConversationContext) -> str:
        """
        Process design critique requests

        Args:
            query: User's design description or question
            context: Conversation context

        Returns:
            Response string with critique
        """
        query_lower = query.lower()
        skill_level = context.get_user_skill_level()

        # Determine critique type needed
        if any(phrase in query_lower for phrase in ['critique', 'feedback', 'review', 'thoughts on']):
            return self._provide_design_critique(query, skill_level, context)

        # Specific aspect questions
        for aspect in self.critique_framework['critique_aspects'].keys():
            if aspect in query_lower:
                return self._aspect_focused_critique(aspect, query, skill_level)

        # Design principle questions
        for principle in self.critique_framework['design_principles'].keys():
            if principle in query_lower:
                return self._principle_focused_questions(principle)

        # How to improve queries
        if any(phrase in query_lower for phrase in ['improve', 'better', 'fix', 'enhance']):
            return self._improvement_guidance(query, skill_level)

        # Learning to critique
        if any(phrase in query_lower for phrase in ['how to critique', 'how to evaluate', 'how to analyze']):
            return self._critique_methodology_guide()

        return self._general_critique_help()

    def _provide_design_critique(self, query: str, skill_level: str, context: ConversationContext) -> str:
        """Provide Socratic design critique"""
        response = "**Design Critique - Let's Think Deeply**\n\n"

        response += "I'm going to ask you some questions to help you think critically about your design. "
        response += "There are no wrong answers - this is about developing your design thinking.\n\n"

        # Get critique level
        level_info = self.critique_framework['critique_levels'].get(skill_level, self.critique_framework['critique_levels']['beginner'])

        response += "**Key Questions to Consider:**\n\n"

        # Concept questions
        response += "**1. Concept & Vision:**\n"
        concept_qs = self.critique_framework['critique_aspects']['concept']['questions']
        for q in concept_qs[:3]:
            response += f"  • {q}\n"

        # Functionality questions
        response += "\n**2. Functionality & Wearability:**\n"
        function_qs = self.critique_framework['critique_aspects']['functionality']['questions']
        for q in function_qs[:2]:
            response += f"  • {q}\n"

        # Aesthetics questions
        response += "\n**3. Aesthetics & Impact:**\n"
        aesthetic_qs = self.critique_framework['critique_aspects']['aesthetics']['questions']
        for q in aesthetic_qs[:2]:
            response += f"  • {q}\n"

        # Technical questions
        response += "\n**4. Construction & Feasibility:**\n"
        construction_qs = self.critique_framework['critique_aspects']['construction']['questions']
        for q in construction_qs[:2]:
            response += f"  • {q}\n"

        response += "\n**Next Steps:**\n"
        response += "1. Answer these questions honestly\n"
        response += "2. Identify any gaps in your thinking\n"
        response += "3. Research or sketch solutions\n"
        response += "4. Refine your design based on insights\n\n"

        response += "**Share your answers with me, and we'll dig deeper together!**\n\n"

        response += "💡 *Remember: Great design comes from asking the right questions, not having all the answers immediately.*"

        return response

    def _aspect_focused_critique(self, aspect: str, query: str, skill_level: str) -> str:
        """Provide critique focused on a specific aspect"""
        aspect_data = self.critique_framework['critique_aspects'][aspect]

        response = f"**{aspect.title()} - Deep Dive Critique**\n\n"

        response += f"Let's explore the {aspect} of your design through these questions:\n\n"

        for i, question in enumerate(aspect_data['questions'], 1):
            response += f"**{i}. {question}**\n"
            response += "   (Take time to really think about this)\n\n"

        response += f"**Indicators of Strong {aspect.title()}:**\n"
        for indicator in aspect_data['depth_indicators']:
            response += f"  ✓ {indicator.replace('_', ' ').title()}\n"

        response += f"\n**Reflective Exercise:**\n"
        response += f"Write down your answers to each question. Look for patterns, contradictions, or gaps in your thinking. "
        response += f"This will reveal where your {aspect} is strong and where it needs development.\n\n"

        if aspect == 'concept':
            response += "**Pro Tip:** A strong concept can be explained in one clear sentence. Can you do that with your design?"
        elif aspect == 'functionality':
            response += "**Pro Tip:** The best designs balance beauty and function. Neither should be sacrificed completely."
        elif aspect == 'innovation':
            response += "**Pro Tip:** Innovation for its own sake is gimmick. Innovation that serves the wearer is design."

        return response

    def _principle_focused_questions(self, principle: str) -> str:
        """Provide questions focused on a design principle"""
        principle_data = self.critique_framework['design_principles'][principle]

        response = f"**{principle.title()} in Design**\n\n"

        response += f"**Key Questions About {principle.title()}:**\n"
        for i, question in enumerate(principle_data['questions'], 1):
            response += f"{i}. {question}\n"

        response += f"\n**What to Consider:**\n"
        for consideration in principle_data['considerations']:
            response += f"  • {consideration.replace('_', ' ').title()}\n"

        response += f"\n**Exercise:**\n"

        if principle == 'balance':
            response += "• Take a photo of your design\n"
            response += "• Squint at it - where does your eye go?\n"
            response += "• Is the visual weight distributed intentionally?\n"
            response += "• Try the design in grayscale to see balance without color distraction\n"

        elif principle == 'proportion':
            response += "• Measure the ratios in your design\n"
            response += "• Compare to the golden ratio (1:1.618)\n"
            response += "• Check against human body proportions\n"
            response += "• Look at garment section relationships (bodice vs skirt, etc.)\n"

        elif principle == 'emphasis':
            response += "• Identify what you want people to notice first\n"
            response += "• Check if your design actually draws the eye there\n"
            response += "• Remove or tone down competing focal points\n"
            response += "• Use contrast (color, texture, detail) intentionally\n"

        elif principle == 'rhythm':
            response += "• Trace the visual path through your design\n"
            response += "• Note where the eye pauses or gets stuck\n"
            response += "• Check if repetitive elements create pleasing rhythm\n"
            response += "• Ensure movement feels intentional, not accidental\n"

        elif principle == 'unity':
            response += "• List all design elements (color, texture, details, etc.)\n"
            response += "• Ask: What connects these elements?\n"
            response += "• Identify any elements that feel out of place\n"
            response += "• Check if overall concept is clear and cohesive\n"

        return response

    def _improvement_guidance(self, query: str, skill_level: str) -> str:
        """Provide guidance on improving designs"""
        response = "**Design Improvement Framework**\n\n"

        response += "Rather than telling you what to change, let's discover it together:\n\n"

        response += "**Step 1: Identify the Core Issue**\n"
        response += "  • What specifically feels 'off' about the design?\n"
        response += "  • Is it visual (aesthetics), functional (wearability), or conceptual (idea)?\n"
        response += "  • Can you point to a specific area or element?\n\n"

        response += "**Step 2: Question the Issue**\n"
        response += "  • Why did you make that design choice originally?\n"
        response += "  • What were you trying to achieve?\n"
        response += "  • Is the issue the choice itself or the execution?\n\n"

        response += "**Step 3: Explore Alternatives**\n"
        response += "  • What are 3 different ways to solve this issue?\n"
        response += "  • What would happen if you did the opposite?\n"
        response += "  • What would [your favorite designer] do?\n\n"

        response += "**Step 4: Test Solutions**\n"
        response += "  • Sketch or sample each alternative\n"
        response += "  • Get feedback from your target audience\n"
        response += "  • Compare against your original concept\n\n"

        response += "**Step 5: Refine & Iterate**\n"
        response += "  • Choose the solution that best serves the design\n"
        response += "  • Make the change decisively\n"
        response += "  • Re-evaluate the entire design for new harmony\n\n"

        response += "**Common Improvement Areas:**\n\n"

        improvements = {
            'Too busy/complex': 'Remove elements one by one. Which removal improves the design most?',
            'Too simple/boring': 'Add one unexpected element. Texture? Color? Detail? Proportion play?',
            'Doesn\'t look cohesive': 'Limit your color palette and repeat design elements throughout',
            'Looks dated': 'Update proportions and silhouette - often the quickest modernizer',
            'Not wearable': 'Ask: Would I actually wear this? Why not? Fix that specific issue',
            'Missing something': 'Usually needs a focal point or one element of surprise'
        }

        for issue, solution in improvements.items():
            response += f"  **{issue}**\n  → {solution}\n\n"

        response += "**What specifically would you like to improve? Let's work through it together!**"

        return response

    def _critique_methodology_guide(self) -> str:
        """Teach how to critique design"""
        return """**How to Critique Fashion Design**

Learn to evaluate design like a professional critic:

**The Critique Framework:**

**1. First Impressions (30 seconds)**
• What is your immediate reaction?
• Where does your eye go first?
• What feeling does the design evoke?
• What stands out most?

*Note these gut reactions - they're valuable data*

**2. Formal Analysis (Design Principles)**
• **Balance**: Is visual weight distributed well?
• **Proportion**: Do parts relate harmoniously?
• **Emphasis**: Is there a clear focal point?
• **Rhythm**: Does the eye move smoothly through the design?
• **Unity**: Do all elements work together?

**3. Conceptual Evaluation**
• What is the designer trying to communicate?
• Is the concept clear or muddled?
• Does execution match intention?
• Is there originality or is it derivative?

**4. Technical Assessment**
• Is it well-constructed?
• Are materials appropriate?
• Would it work on a body?
• Is it wearable/functional?

**5. Contextual Consideration**
• Who is the target wearer?
• What is the occasion/use?
• How does it fit in current fashion landscape?
• Is it commercially viable (if relevant)?

**6. Innovation & Impact**
• What's new or different?
• Is innovation purposeful or gimmicky?
• Will this influence other designers?
• Does it push fashion forward?

---

**Critique Best Practices:**

**DO:**
✓ Start with what works
✓ Ask questions more than making statements
✓ Be specific ("the sleeve proportion feels off" not "it's bad")
✓ Consider the designer's intent
✓ Suggest alternatives when criticizing
✓ Separate personal taste from objective analysis

**DON'T:**
❌ Be purely negative
❌ Make it personal
❌ Use vague language ("I don't like it")
❌ Ignore context
❌ Critique without understanding the brief
❌ Forget that all design is subjective to some degree

---

**The Socratic Method in Design Critique:**

Instead of: *"This color doesn't work"*
Ask: *"What is this color communicating? Is that your intention?"*

Instead of: *"The proportions are wrong"*
Ask: *"What effect do these proportions create? Is that what you want?"*

Instead of: *"This is too complicated"*
Ask: *"If you removed one element, which would have the least impact?"*

**The Goal:**
Help designers discover their own solutions through guided questioning. This builds critical thinking skills, not just dependency on others' opinions.

---

**Practice Exercise:**

Choose any fashion image and work through the 6-step framework above. Write down your observations. Over time, this becomes second nature.

**Ready to practice? Describe a design you want to critique!**"""

    def _general_critique_help(self) -> str:
        """General critique help"""
        return """**Design Critique System**

I help you think critically about fashion design through the Socratic method.

**What I Offer:**

**Design Critique:**
• Thoughtful questioning, not just validation
• Socratic method to develop your critical thinking
• Feedback tailored to your skill level
• Professional design analysis

**Critique Aspects:**
• **Concept** - Your design vision and story
• **Functionality** - Wearability and practicality
• **Construction** - Technical feasibility
• **Innovation** - Originality and creativity
• **Aesthetics** - Visual impact and beauty
• **Sustainability** - Environmental and ethical considerations

**Design Principles:**
• Balance
• Proportion
• Emphasis
• Rhythm
• Unity

**How to Use This Tool:**

**For Design Review:**
"I'd like feedback on my [garment type] design"
*I'll ask questions to help you think deeper*

**For Specific Aspects:**
"How can I improve the concept of my design?"
*I'll focus on that specific area*

**For Learning:**
"How do I critique fashion design?"
*I'll teach you the methodology*

**For Improvement:**
"My design feels off but I don't know why"
*We'll discover the issue together*

---

**My Approach:**

I won't just tell you "good" or "bad" - that doesn't help you grow.

Instead, I'll:
1. Ask questions that make you think
2. Help you discover your own solutions
3. Guide you to stronger design decisions
4. Build your critical thinking skills

**The Goal:**
Develop your inner critic so you can evaluate your own work confidently.

---

**Ready to start?**
• Share a design for critique
• Ask about a specific design principle
• Request help improving something specific
• Learn the critique methodology

What would you like to explore?"""
