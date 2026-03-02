"""
Safety Validator for Content Safety and Prompt Injection Detection
RUBRIC: Governance & Compliance (10 marks total)
- PII detection implemented (3 marks)
- GDPR compliance checks (2 marks)
- Content safety validation (2 marks)
- Audit logging (3 marks)

TASK: Implement content safety and prompt injection detection
"""
import logging
from typing import Dict, List
from guardrails.content_safety import ContentSafety
from guardrails.pii_detector import PIIDetector

class SafetyValidator:
    """Handles content safety and prompt injection detection"""
    
    def __init__(self):
        """
        Initialize safety validator components
        
        HINT: Initialize:
        1. Content Safety validator
        2. PII Detector for output validation
        3. Set up logging
        """
        # HINT: Initialize Content Safety validator
        self.content_safety = ContentSafety()
        
        # HINT: Initialize PII Detector for output validation
        self.pii_detector = PIIDetector()
        
        # HINT: Set up logging
        self.logger = logging.getLogger(__name__)
    
    def check_prompt_injection(self, prompt: str) -> Dict[str, any]:
        """
        Detect prompt injection attempts
        
        HINT: Check for common prompt injection patterns:
        1. Instruction overriding ("Ignore previous instructions")
        2. System prompt manipulation
        3. Malicious command injection
        4. Context manipulation
        """
        # HINT: Define prompt injection patterns
        injection_patterns = [
            r"(?i)ignore.*previous.*instructions",
            r"(?i)forget.*previous.*instructions", 
            r"(?i)you are now.*",
            r"(?i)act as if.*",
            r"(?i)pretend that.*",
            r"(?i)disregard.*safety.*guidelines",
            r"(?i)output.*the.*following.*text",
            r"(?i)repeat.*after.*me",
            r"(?i)execute.*the.*following.*command",
            r"(?i)run.*this.*code"
        ]
        
        # HINT: Check for injection patterns
        violations = []
        for pattern in injection_patterns:
            if re.search(pattern, prompt):
                violations.append(f"Prompt injection pattern detected: {pattern}")
        
        # HINT: Check for system prompt manipulation
        system_keywords = ['system:', 'system prompt:', 'you are an AI assistant']
        if any(keyword in prompt.lower() for keyword in system_keywords):
            violations.append("System prompt manipulation attempt detected")
        
        # HINT: Return validation result
        return {
            "is_safe": len(violations) == 0,
            "violations": violations,
            "severity": "high" if violations else "low"
        }
    
    def check_content_safety(self, text: str) -> Dict[str, any]:
        """
        Check content safety using multiple methods
        
        HINT: Use ContentSafety to check for:
        1. Hate speech
        2. Self-harm content
        3. Sexual content
        4. Violence
        """
        # HINT: Use ContentSafety to check content
        safety_results = self.content_safety.check_content(text)
        
        # HINT: Determine overall safety
        is_safe = all(not result['flagged'] for result in safety_results.values())
        
        # HINT: Collect violations
        violations = []
        for category, result in safety_results.items():
            if result['flagged']:
                violations.append({
                    "category": category,
                    "severity": result['severity'],
                    "details": result['details']
                })
        
        return {
            "is_safe": is_safe,
            "violations": violations,
            "severity": "high" if violations else "low"
        }
    
    def validate_input_safety(self, prompt: str) -> Dict[str, any]:
        """
        Validate input prompt for safety
        
        HINT: Combine prompt injection and content safety checks
        Return comprehensive safety report
        """
        # HINT: Check for prompt injection
        injection_check = self.check_prompt_injection(prompt)
        
        # HINT: Check content safety
        content_check = self.check_content_safety(prompt)
        
        # HINT: Determine overall safety
        is_safe = injection_check["is_safe"] and content_check["is_safe"]
        
        # HINT: Log safety check
        self.logger.info(f"Input safety check: injection_safe={injection_check['is_safe']}, content_safe={content_check['is_safe']}")
        
        # HINT: Return comprehensive report
        return {
            "is_safe": is_safe,
            "prompt_injection_check": injection_check,
            "content_safety_check": content_check,
            "overall_severity": "high" if not is_safe else "low",
            "timestamp": self._get_timestamp()
        }
    
    def validate_output_safety(self, response: str) -> Dict[str, any]:
        """
        Validate output response for safety
        
        HINT: Check for:
        1. Content safety violations
        2. PII leakage in response
        3. Malicious content
        """
        # HINT: Check content safety
        content_check = self.check_content_safety(response)
        
        # HINT: Check for PII leakage
        pii_violations = self.pii_detector.detect_pii(response)
        
        # HINT: Determine overall safety
        has_pii = len(pii_violations) > 0
        is_safe = content_check["is_safe"] and not has_pii
        
        # HINT: Log output safety check
        self.logger.info(f"Output safety check: content_safe={content_check['is_safe']}, pii_found={has_pii}")
        
        # HINT: Return comprehensive report
        return {
            "is_safe": is_safe,
            "content_safety_check": content_check,
            "pii_check": {
                "has_pii": has_pii,
                "pii_types": list(pii_violations.keys()) if pii_violations else []
            },
            "overall_severity": "high" if not is_safe else "low",
            "timestamp": self._get_timestamp()
        }
    
    def _get_timestamp(self) -> str:
        """Get current timestamp for logging"""
        from datetime import datetime
        return datetime.now().isoformat()
