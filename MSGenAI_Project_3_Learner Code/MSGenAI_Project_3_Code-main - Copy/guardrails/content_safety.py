"""
Content Safety Guardrail
RUBRIC: Guardrails Implementation (10 marks total)
- Content safety guardrail implemented (5 marks)
- PII detection guardrail implemented (5 marks)

TASK: Implement keyword-based content filtering
"""
import re
import logging
from typing import Dict, List, Any

class ContentSafety:
    """Content safety guardrail using keyword-based filtering"""
    
    def __init__(self):
        """
        Initialize content safety with keyword patterns
        
        HINT: Define keyword patterns for different content categories
        """
        # HINT: Define hate speech patterns
        self.hate_speech_patterns = [
            r"(?i)\b(nigger|nigga|kike|fag|faggot|chink|gook|spic|wetback)\b",
            r"(?i)\b(racist|white supremacist|neo-nazi|kkk)\b",
            r"(?i)\b(hate group|terrorist|extremist)\b"
        ]
        
        # HINT: Define self-harm patterns
        self.self_harm_patterns = [
            r"(?i)\b(suicide|kill myself|end my life|hang myself)\b",
            r"(?i)\b(overdose|cut myself|self harm)\b",
            r"(?i)\b(please let me die|I want to die)\b"
        ]
        
        # HINT: Define sexual content patterns
        self.sexual_content_patterns = [
            r"(?i)\b(porn|xxx|nude|naked|sexual|erotic)\b",
            r"(?i)\b(sex act|sexual content|adult content)\b",
            r"(?i)\b(pornographic|explicit content)\b"
        ]
        
        # HINT: Define violence patterns
        self.violence_patterns = [
            r"(?i)\b(murder|kill|assassinate|execute|torture)\b",
            r"(?i)\b(violence|brutality|cruelty|torture)\b",
            r"(?i)\b(weapon|gun|knife|explosive)\b"
        ]
        
        # HINT: Set up logging
        self.logger = logging.getLogger(__name__)
    
    def check_content(self, text: str) -> Dict[str, Dict[str, Any]]:
        """
        Check text for unsafe content across multiple categories
        
        HINT: Check each content category and return results
        """
        results = {}
        
        # HINT: Check hate speech
        results["hate_speech"] = self._check_category(text, self.hate_speech_patterns, "hate_speech")
        
        # HINT: Check self-harm
        results["self_harm"] = self._check_category(text, self.self_harm_patterns, "self_harm")
        
        # HINT: Check sexual content
        results["sexual_content"] = self._check_category(text, self.sexual_content_patterns, "sexual_content")
        
        # HINT: Check violence
        results["violence"] = self._check_category(text, self.violence_patterns, "violence")
        
        return results
    
    def _check_category(self, text: str, patterns: List[str], category: str) -> Dict[str, Any]:
        """
        Check text against patterns for a specific category
        
        HINT: Return dict with flagged status, severity, and details
        """
        violations = []
        
        # HINT: Check each pattern
        for pattern in patterns:
            matches = re.findall(pattern, text)
            if matches:
                violations.extend(matches)
        
        # HINT: Determine severity based on violation count
        if len(violations) == 0:
            severity = "none"
            flagged = False
        elif len(violations) <= 2:
            severity = "low"
            flagged = True
        elif len(violations) <= 5:
            severity = "medium"
            flagged = True
        else:
            severity = "high"
            flagged = True
        
        # HINT: Log content check
        if flagged:
            self.logger.warning(f"Content safety violation in {category}: {violations}")
        
        return {
            "flagged": flagged,
            "severity": severity,
            "violations": violations,
            "details": {
                "category": category,
                "pattern_count": len(patterns),
                "match_count": len(violations)
            }
        }
    
    def is_content_safe(self, text: str) -> bool:
        """
        Quick check if content is safe
        
        HINT: Return True if no violations found in any category
        """
        results = self.check_content(text)
        
        # HINT: Check if any category is flagged
        for category_result in results.values():
            if category_result["flagged"]:
                return False
        
        return True
    
    def get_violation_summary(self, text: str) -> Dict[str, Any]:
        """
        Get summary of all violations found
        
        HINT: Return summary with total violations and categories affected
        """
        results = self.check_content(text)
        
        # HINT: Count violations by category
        violations_by_category = {}
        total_violations = 0
        
        for category, result in results.items():
            if result["flagged"]:
                violations_by_category[category] = result["violations"]
                total_violations += len(result["violations"])
        
        # HINT: Determine overall severity
        if total_violations == 0:
            overall_severity = "none"
        elif total_violations <= 3:
            overall_severity = "low"
        elif total_violations <= 8:
            overall_severity = "medium"
        else:
            overall_severity = "high"
        
        return {
            "total_violations": total_violations,
            "violations_by_category": violations_by_category,
            "categories_affected": list(violations_by_category.keys()),
            "overall_severity": overall_severity,
            "is_safe": total_violations == 0
        }