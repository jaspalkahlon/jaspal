"""
Troubleshooting Companion Module
Real-time problem-solving for fit issues and construction challenges
"""

import logging
from typing import Dict, Any, List
from ...bot.core.context import ConversationContext


class TroubleshootingCompanion:
    """
    Provides real-time troubleshooting for common and complex sewing issues.
    Diagnoses problems and offers step-by-step solutions.
    """

    def __init__(self, config: Dict[str, Any]):
        """
        Initialize Troubleshooting Companion Module

        Args:
            config: Configuration for the module
        """
        self.config = config
        self.logger = logging.getLogger(__name__)
        self.issue_database = self._load_issue_database()

    def _load_issue_database(self) -> Dict[str, Any]:
        """Load database of common issues and solutions"""
        return {
            'fit_issues': {
                'pulling_across_bust': {
                    'symptoms': ['fabric straining', 'horizontal wrinkles', 'gaping buttons'],
                    'causes': ['insufficient bust ease', 'dart placement wrong', 'size too small'],
                    'solutions': [
                        'Add 1-2" to bust measurement',
                        'Adjust dart position to apex',
                        'Add a princess seam for better fit',
                        'Consider full bust adjustment (FBA)'
                    ],
                    'difficulty': 'intermediate'
                },
                'gaping_neckline': {
                    'symptoms': ['fabric standing away from neck', 'shows bra/undergarments', 'loose fit'],
                    'causes': ['neckline too wide', 'shoulders too large', 'posture considerations'],
                    'solutions': [
                        'Take in shoulder seams',
                        'Reduce neckline width',
                        'Add darts at shoulders',
                        'Use narrower seam allowances at neckline'
                    ],
                    'difficulty': 'beginner'
                },
                'tight_armholes': {
                    'symptoms': ['restricted movement', 'pulling under arm', 'discomfort'],
                    'causes': ['armhole too small', 'insufficient ease', 'sleeve cap too tight'],
                    'solutions': [
                        'Lower armhole by 1/2" to 1"',
                        'Scoop out underarm area',
                        'Add gussets for more movement',
                        'Check sleeve cap ease'
                    ],
                    'difficulty': 'intermediate'
                },
                'baggy_crotch': {
                    'symptoms': ['excess fabric hanging', 'diaper effect', 'uncomfortable sitting'],
                    'causes': ['crotch depth too long', 'wrong rise measurement', 'poor fit for body type'],
                    'solutions': [
                        'Shorten crotch depth',
                        'Take in inseam',
                        'Adjust back rise',
                        'Consider different rise style (mid vs. high)'
                    ],
                    'difficulty': 'advanced'
                },
                'wrinkles_at_waist': {
                    'symptoms': ['horizontal folds', 'bunching fabric', 'poor drape'],
                    'causes': ['waist suppression incorrect', 'hip to waist ratio off', 'poor posture fit'],
                    'solutions': [
                        'Adjust dart size and position',
                        'Add or remove waist shaping',
                        'Check for sway back adjustments',
                        'Consider adding princess seams'
                    ],
                    'difficulty': 'intermediate'
                }
            },
            'construction_issues': {
                'puckered_seams': {
                    'symptoms': ['wavy seams', 'gathered appearance', 'poor finish'],
                    'causes': ['thread tension too tight', 'fabric stretching while sewing', 'wrong stitch length'],
                    'solutions': [
                        'Reduce upper thread tension',
                        'Use proper presser foot pressure',
                        'Don\'t pull fabric while sewing',
                        'Increase stitch length for lightweight fabrics',
                        'Use tissue paper under fabric'
                    ],
                    'difficulty': 'beginner'
                },
                'skipped_stitches': {
                    'symptoms': ['gaps in stitch line', 'intermittent stitching', 'weak seams'],
                    'causes': ['wrong needle type', 'dull/bent needle', 'improper threading', 'machine timing off'],
                    'solutions': [
                        'Replace needle (use ballpoint for knits)',
                        'Check needle is inserted correctly',
                        'Re-thread machine completely',
                        'Slow down sewing speed',
                        'Service machine if problem persists'
                    ],
                    'difficulty': 'beginner'
                },
                'uneven_hems': {
                    'symptoms': ['wavy hemline', 'different lengths', 'visible irregularities'],
                    'causes': ['bias cut fabric', 'stretching while handling', 'inaccurate measuring'],
                    'solutions': [
                        'Let garment hang 24 hours before hemming',
                        'Use hem gauge for consistency',
                        'Press hem thoroughly before stitching',
                        'Pin from right side at floor length',
                        'Use fusible hem tape for stability'
                    ],
                    'difficulty': 'beginner'
                },
                'gathered_sleeve_cap': {
                    'symptoms': ['puckered sleeve head', 'visible gathers', 'poor drape'],
                    'causes': ['too much ease', 'improper easing technique', 'stretching while sewing'],
                    'solutions': [
                        'Reduce ease in sleeve cap',
                        'Use ease stitching technique (not gathering)',
                        'Steam and press cap before attaching',
                        'Clip and notch curves properly',
                        'Practice setting sleeves on scrap first'
                    ],
                    'difficulty': 'intermediate'
                },
                'zipper_rippling': {
                    'symptoms': ['wavy zipper tape', 'puckered fabric', 'zipper won\'t lie flat'],
                    'causes': ['stretched fabric', 'wrong zipper foot', 'fabric too lightweight'],
                    'solutions': [
                        'Interface fabric before inserting zipper',
                        'Use proper zipper foot',
                        'Pin or baste zipper before stitching',
                        'Ensure fabric isn\'t stretched while sewing',
                        'Use fusible stay tape on zipper area'
                    ],
                    'difficulty': 'intermediate'
                },
                'thread_bunching': {
                    'symptoms': ['bird nests on underside', 'tangled thread', 'jammed machine'],
                    'causes': ['incorrect threading', 'bobbin wound wrong', 'tension issues', 'lint buildup'],
                    'solutions': [
                        'Re-thread entire machine with presser foot up',
                        'Check bobbin is wound evenly',
                        'Clean bobbin case and feed dogs',
                        'Ensure bobbin is inserted correctly',
                        'Check upper thread tension'
                    ],
                    'difficulty': 'beginner'
                }
            },
            'fabric_issues': {
                'fabric_slipping': {
                    'symptoms': ['layers shifting', 'uneven seams', 'difficult to control'],
                    'causes': ['slippery fabric', 'insufficient pinning', 'wrong presser foot'],
                    'solutions': [
                        'Use more pins or clips',
                        'Baste layers together first',
                        'Use walking foot or roller foot',
                        'Place tissue paper between layers',
                        'Reduce presser foot pressure'
                    ],
                    'difficulty': 'beginner'
                },
                'fraying_edges': {
                    'symptoms': ['threads coming loose', 'edges unraveling', 'messy seam allowances'],
                    'causes': ['loosely woven fabric', 'no edge finishing', 'handling before finishing'],
                    'solutions': [
                        'Finish edges immediately after cutting',
                        'Use serger or zigzag stitch',
                        'Apply fray check liquid',
                        'Use French seams or flat-felled seams',
                        'Handle fabric gently'
                    ],
                    'difficulty': 'beginner'
                },
                'static_cling': {
                    'symptoms': ['fabric sticking to itself', 'difficult to handle', 'shocking'],
                    'causes': ['synthetic fibers', 'dry environment', 'friction'],
                    'solutions': [
                        'Use static spray on fabric',
                        'Lightly mist with water',
                        'Use fabric softener in wash',
                        'Add lining to reduce static',
                        'Humidify sewing space'
                    ],
                    'difficulty': 'beginner'
                }
            }
        }

    def process(self, query: str, context: ConversationContext) -> str:
        """
        Process troubleshooting queries

        Args:
            query: User's problem description
            context: Conversation context

        Returns:
            Response string with solutions
        """
        query_lower = query.lower()

        # Search for matching issues
        matched_issues = self._find_matching_issues(query_lower)

        if matched_issues:
            return self._provide_solutions(matched_issues)

        # Check for specific categories
        if any(word in query_lower for word in ['fit', 'tight', 'loose', 'pulling', 'gaping']):
            return self._fit_troubleshooting_guide()

        if any(word in query_lower for word in ['seam', 'stitch', 'sewing machine', 'needle', 'thread']):
            return self._construction_troubleshooting_guide()

        if any(word in query_lower for word in ['fabric', 'material', 'fraying', 'slipping']):
            return self._fabric_troubleshooting_guide()

        # General help
        return self._general_troubleshooting_help()

    def _find_matching_issues(self, query: str) -> List[tuple]:
        """Find issues matching the user's description"""
        matches = []

        for category, issues in self.issue_database.items():
            for issue_name, issue_data in issues.items():
                # Check if any symptom or cause keywords match query
                all_keywords = issue_data['symptoms'] + issue_data['causes'] + [issue_name.replace('_', ' ')]

                for keyword in all_keywords:
                    if keyword.lower() in query:
                        matches.append((category, issue_name, issue_data))
                        break

        return matches

    def _provide_solutions(self, matched_issues: List[tuple]) -> str:
        """Provide detailed solutions for matched issues"""
        if len(matched_issues) == 1:
            category, issue_name, issue_data = matched_issues[0]
            return self._detailed_solution(issue_name, issue_data, category)

        # Multiple matches - provide overview
        response = "I found several possible issues. Here are solutions for each:\n\n"

        for category, issue_name, issue_data in matched_issues[:3]:  # Top 3 matches
            response += f"**{issue_name.replace('_', ' ').title()}**\n"
            response += f"Quick fixes:\n"
            for i, solution in enumerate(issue_data['solutions'][:2], 1):
                response += f"{i}. {solution}\n"
            response += "\n"

        response += "Want detailed help with one of these issues? Let me know which one!"

        return response

    def _detailed_solution(self, issue_name: str, issue_data: Dict[str, Any], category: str) -> str:
        """Provide detailed solution for a specific issue"""
        display_name = issue_name.replace('_', ' ').title()

        response = f"**Troubleshooting: {display_name}**\n\n"

        response += "**Symptoms:**\n"
        for symptom in issue_data['symptoms']:
            response += f"  • {symptom.title()}\n"

        response += "\n**Common Causes:**\n"
        for cause in issue_data['causes']:
            response += f"  • {cause.title()}\n"

        response += "\n**Solutions (Try in Order):**\n"
        for i, solution in enumerate(issue_data['solutions'], 1):
            response += f"{i}. {solution}\n"

        difficulty = issue_data.get('difficulty', 'intermediate')
        response += f"\n**Difficulty Level:** {difficulty.title()}\n"

        if difficulty == 'advanced':
            response += "\n⚠️ **Note:** This is an advanced fix. Consider consulting a pattern maker or taking a fitting class if you're new to alterations.\n"

        response += "\n💡 **Pro Tip:** Always test fixes on muslin first before altering your final garment!"

        return response

    def _fit_troubleshooting_guide(self) -> str:
        """Provide general fit troubleshooting guidance"""
        return """**Fit Troubleshooting Guide**

**Common Fit Issues I Can Help With:**

1. **Pulling Across Bust** - Too tight at chest
2. **Gaping Neckline** - Loose at neck/shoulders
3. **Tight Armholes** - Restricted arm movement
4. **Baggy Crotch** - Excess fabric in pants
5. **Wrinkles at Waist** - Poor waist fit

**General Fit Troubleshooting Steps:**

1. **Identify the Issue:**
   • Where is the problem occurring?
   • When did you first notice it?
   • Does it affect comfort or appearance?

2. **Check Measurements:**
   • Compare body measurements to pattern
   • Verify ease allowances
   • Check you're using correct size

3. **Analyze the Garment:**
   • Try it on inside out
   • Pin adjustments directly on body
   • Take photos to see issues clearly

4. **Make Corrections:**
   • Start with smallest adjustment
   • Test on muslin if possible
   • Document what works for next time

**Need Specific Help?**
Describe your fit issue in detail:
• Where is the problem?
• What does it look or feel like?
• What garment type?

I'll provide step-by-step solutions!"""

    def _construction_troubleshooting_guide(self) -> str:
        """Provide construction troubleshooting guidance"""
        return """**Construction Troubleshooting Guide**

**Common Construction Issues:**

**Sewing Machine Problems:**
• **Puckered Seams** - Wavy, gathered appearance
• **Skipped Stitches** - Gaps in stitch line
• **Thread Bunching** - Bird nests underneath
• **Broken Needles** - Frequent needle breakage

**Seam & Assembly Issues:**
• **Uneven Hems** - Varying lengths
• **Gathered Sleeve Caps** - Puckered sleeve head
• **Zipper Rippling** - Wavy zipper installation
• **Misaligned Patterns** - Stripes/plaids don't match

**Quick Diagnostic Questions:**

1. **Machine Issues:**
   • When did you last change the needle?
   • Is the machine clean (lint-free)?
   • Is threading correct?

2. **Technique Issues:**
   • Are you pulling fabric while sewing?
   • Is presser foot pressure correct?
   • Are you using appropriate stitch length?

3. **Material Issues:**
   • Is your fabric particularly difficult (slippery, stretchy, thick)?
   • Are you using the right needle type?
   • Is thread quality good?

**Emergency Fixes:**
• **Broken stitch line:** Restitch immediately before more unraveling
• **Crooked seam:** Remove stitches and resew
• **Wrong side sewn:** Evaluate if it's visible in final garment

Tell me what problem you're experiencing, and I'll walk you through the fix!"""

    def _fabric_troubleshooting_guide(self) -> str:
        """Provide fabric-specific troubleshooting"""
        return """**Fabric Handling Troubleshooting**

**Common Fabric Challenges:**

**Slippery Fabrics (Silk, Satin, Chiffon):**
• Fabric shifts while cutting/sewing
• **Solutions:**
  - Use more pins or pattern weights
  - Cut single layer on non-slip surface
  - Use tissue paper under fabric while sewing
  - Walking foot or roller foot

**Stretchy Fabrics (Knits, Jersey):**
• Seams wave or tunnel
• **Solutions:**
  - Use ballpoint needle
  - Stretch stitch or narrow zigzag
  - Don't pull fabric while sewing
  - Stabilize seams with clear elastic

**Bulky Fabrics (Denim, Coating, Velvet):**
• Machine struggles, thick seams
• **Solutions:**
  - Use jeans needle (size 100/16 or 110/18)
  - Longer stitch length
  - Hammer seams flat before stitching
  - Use wedge/hump jumper for thick areas

**Sheer Fabrics (Chiffon, Organza):**
• Puckering, difficult to handle
• **Solutions:**
  - Use French seams
  - Fine needle (70/10)
  - Tissue paper method
  - Shorter stitch length

**Fraying Fabrics (Linen, Loosely Woven):**
• Edges unravel quickly
• **Solutions:**
  - Finish edges immediately after cutting
  - Serge or zigzag raw edges
  - Use fray check on cut edges
  - French or flat-felled seams

What fabric are you working with? I can provide specific handling tips!"""

    def _general_troubleshooting_help(self) -> str:
        """General troubleshooting help"""
        return """**Troubleshooting Companion - Your Problem Solver**

I'm here to help diagnose and solve sewing challenges!

**I Can Help With:**

**Fit Issues:**
• Pulling, gaping, tight, loose areas
• Adjustment techniques
• Pattern modifications
• Body shape considerations

**Construction Problems:**
• Sewing machine issues
• Seam problems
• Assembly challenges
• Finishing techniques

**Fabric Challenges:**
• Difficult-to-handle materials
• Fabric-specific techniques
• Edge finishing
• Special handling needs

**How to Get Best Help:**

1. **Describe the Problem:**
   • What's wrong specifically?
   • When does it happen?
   • What have you tried?

2. **Provide Context:**
   • What are you making?
   • What fabric/materials?
   • Your skill level?

3. **Share Symptoms:**
   • How does it look?
   • How does it feel?
   • Is it functional or cosmetic?

**Example Questions:**
• "My dress is pulling across the bust"
• "Why are my seams puckering?"
• "How do I fix a gaping neckline?"
• "My satin keeps slipping while I cut"

What issue can I help you troubleshoot today?"""
