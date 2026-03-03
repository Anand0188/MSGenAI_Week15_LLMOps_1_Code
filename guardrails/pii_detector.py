"""
PII Detector Guardrail
RUBRIC: Guardrails Implementation (10 marks total)
- Content safety guardrail implemented (5 marks)
- PII detection guardrail implemented (5 marks)

TASK: Implement regex-based PII detection
"""
import re
import logging
from typing import Dict, List, Any

class PIIDetector:
    """PII detection guardrail using regex patterns"""
    
    def __init__(self):
        """
        Initialize PII detector with regex patterns
        
        HINT: Define regex patterns for different PII types
        """
        # HINT: Define email pattern
        self.email_pattern = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
        
        # HINT: Define phone number patterns (US and international)
        self.phone_patterns = [
            r'\b\d{3}-\d{3}-\d{4}\b',  # US format: 123-456-7890
            r'\b\(\d{3}\)\s?\d{3}-\d{4}\b',  # US format: (123) 456-7890
            r'\b\d{10}\b',  # 10 digit number
            r'\+\d{1,3}[-.\s]?\d{1,4}[-.\s]?\d{1,4}[-.\s]?\d{1,9}\b'  # International
        ]
        
        # HINT: Define SSN pattern (US format)
        self.ssn_pattern = r'\b\d{3}-\d{2}-\d{4}\b'
        
        # HINT: Define credit card pattern
        self.credit_card_pattern = r'\b(?:\d[ -]*?){13,16}\b'
        
        # HINT: Define passport number patterns
        self.passport_patterns = [
            r'\b[A-Z0-9]{6,9}\b',  # General passport format
            r'\b[A-Z]{1,2}\d{6,7}\b'  # Country code + numbers
        ]
        
        # HINT: Define address patterns
        self.address_patterns = [
            r'\d+\s+[A-Za-z0-9\s]+(?:Street|St|Avenue|Ave|Road|Rd|Boulevard|Blvd|Lane|Ln|Drive|Dr)\b',
            r'\b\d{5}(?:-\d{4})?\b'  # ZIP codes
        ]
        
        # HINT: Set up logging
        self.logger = logging.getLogger(__name__)
    
    def detect_pii(self, text: str) -> Dict[str, List[str]]:
        """
        Detect PII in text and return categorized results
        
        HINT: Check each PII type and return dict with detected values
        """
        results = {}
        
        # HINT: Detect emails
        emails = self._find_matches(text, self.email_pattern)
        if emails:
            results["email"] = emails
        
        # HINT: Detect phone numbers
        phones = []
        for pattern in self.phone_patterns:
            phones.extend(self._find_matches(text, pattern))
        if phones:
            results["phone"] = phones
        
        # HINT: Detect SSN
        ssn = self._find_matches(text, self.ssn_pattern)
        if ssn:
            results["ssn"] = ssn
        
        # HINT: Detect credit cards
        credit_cards = self._find_matches(text, self.credit_card_pattern)
        if credit_cards:
            results["credit_card"] = credit_cards
        
        # HINT: Detect passport numbers
        passports = []
        for pattern in self.passport_patterns:
            passports.extend(self._find_matches(text, pattern))
        if passports:
            results["passport"] = passports
        
        # HINT: Detect addresses
        addresses = []
        for pattern in self.address_patterns:
            addresses.extend(self._find_matches(text, pattern))
        if addresses:
            results["address"] = addresses
        
        return results
    
    def _find_matches(self, text: str, pattern: str) -> List[str]:
        """
        Find all matches for a regex pattern in text
        
        HINT: Use re.findall to extract all matches
        """
        matches = re.findall(pattern, text, re.IGNORECASE)
        return matches
    
    def has_pii(self, text: str) -> bool:
        """
        Quick check if text contains any PII
        
        HINT: Return True if any PII type is detected
        """
        pii_results = self.detect_pii(text)
        return len(pii_results) > 0
    
    def get_pii_summary(self, text: str) -> Dict[str, Any]:
        """
        Get summary of PII detection results
        
        HINT: Return summary with counts and types detected
        """
        pii_results = self.detect_pii(text)
        
        # HINT: Count total PII instances
        total_pii = sum(len(values) for values in pii_results.values())
        
        # HINT: Get types detected
        types_detected = list(pii_results.keys())
        
        return {
            "has_pii": total_pii > 0,
            "total_pii_count": total_pii,
            "types_detected": types_detected,
            "detailed_results": pii_results,
            "severity": self._calculate_severity(total_pii, types_detected)
        }
    
    def _calculate_severity(self, total_count: int, types: List[str]) -> str:
        """
        Calculate severity level based on PII count and types
        
        HINT: Return severity level (low, medium, high)
        """
        if total_count == 0:
            return "none"
        elif total_count <= 2 and len(types) <= 2:
            return "low"
        elif total_count <= 5 and len(types) <= 3:
            return "medium"
        else:
            return "high"
    
    def redact_pii(self, text: str) -> str:
        """
        Redact PII from text by replacing with placeholders
        
        HINT: Replace detected PII with [REDACTED] placeholders
        """
        redacted_text = text
        
        # HINT: Redact emails
        redacted_text = re.sub(self.email_pattern, "[REDACTED_EMAIL]", redacted_text, flags=re.IGNORECASE)
        
        # HINT: Redact phone numbers
        for pattern in self.phone_patterns:
            redacted_text = re.sub(pattern, "[REDACTED_PHONE]", redacted_text, flags=re.IGNORECASE)
        
        # HINT: Redact SSN
        redacted_text = re.sub(self.ssn_pattern, "[REDACTED_SSN]", redacted_text)
        
        # HINT: Redact credit cards
        redacted_text = re.sub(self.credit_card_pattern, "[REDACTED_CREDIT_CARD]", redacted_text)
        
        # HINT: Redact passport numbers
        for pattern in self.passport_patterns:
            redacted_text = re.sub(pattern, "[REDACTED_PASSPORT]", redacted_text, flags=re.IGNORECASE)
        
        # HINT: Redact addresses
        for pattern in self.address_patterns:
            redacted_text = re.sub(pattern, "[REDACTED_ADDRESS]", redacted_text, flags=re.IGNORECASE)
        
        return redacted_text