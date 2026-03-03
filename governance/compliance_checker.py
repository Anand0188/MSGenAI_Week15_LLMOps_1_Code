"""
Compliance Checker for GDPR and PII Detection
RUBRIC: Governance & Compliance (10 marks total)
- PII detection implemented (3 marks)
- GDPR compliance checks (2 marks)
- Content safety validation (2 marks)
- Audit logging (3 marks)

TASK: Implement PII detection and GDPR compliance checking
"""
import re
import logging
from typing import Dict, List, Tuple
from guardrails.pii_detector import PIIDetector
from guardrails.content_safety import ContentSafety

class ComplianceChecker:
    """Handles PII detection and GDPR compliance validation"""
    
    def __init__(self):
        """
        Initialize compliance checker components
        
        HINT: Initialize:
        1. PII Detector
        2. Content Safety validator
        3. Set up logging
        """
        # HINT: Initialize PII Detector
        self.pii_detector = PIIDetector()
        
        # HINT: Initialize Content Safety validator
        self.content_safety = ContentSafety()
        
        # HINT: Set up logging
        self.logger = logging.getLogger(__name__)
    
    def check_pii(self, text: str) -> Dict[str, List[str]]:
        """
        Detect PII in text and return violations
        
        HINT: Use PIIDetector to find PII patterns
        Return dict with violation types and detected values
        """
        # HINT: Use PIIDetector to find PII patterns
        pii_results = self.pii_detector.detect_pii(text)
        
        # HINT: Return dict with violation types and detected values
        violations = {}
        for pii_type, values in pii_results.items():
            if values:  # Only include types that were found
                violations[pii_type] = values
        
        return violations
    
    def check_gdpr_compliance(self, text: str) -> Dict[str, bool]:
        """
        Check GDPR compliance requirements
        
        HINT: Check for:
        1. Data minimization (no unnecessary PII)
        2. Purpose limitation (appropriate use)
        3. Storage limitation (no excessive data)
        """
        # HINT: Check for PII presence
        pii_violations = self.check_pii(text)
        
        # HINT: Check for data minimization
        has_unnecessary_pii = len(pii_violations) > 0
        
        # HINT: Check for appropriate purpose (basic check for sensitive data)
        sensitive_keywords = ['password', 'ssn', 'social security', 'credit card', 'bank account']
        has_sensitive_data = any(keyword in text.lower() for keyword in sensitive_keywords)
        
        # HINT: Return compliance status
        compliance_status = {
            "data_minimization": not has_unnecessary_pii,
            "purpose_limitation": not has_sensitive_data,
            "storage_limitation": True,  # Basic implementation
            "overall_compliant": not (has_unnecessary_pii or has_sensitive_data)
        }
        
        return compliance_status
    
    def validate_compliance(self, text: str) -> Dict[str, any]:
        """
        Main compliance validation method
        
        HINT: Combine PII detection and GDPR checks
        Return comprehensive compliance report
        """
        # HINT: Check PII violations
        pii_violations = self.check_pii(text)
        
        # HINT: Check GDPR compliance
        gdpr_status = self.check_gdpr_compliance(text)
        
        # HINT: Log compliance check
        self.logger.info(f"Compliance check completed: {len(pii_violations)} PII violations found")
        
        # HINT: Return comprehensive report
        return {
            "is_compliant": gdpr_status["overall_compliant"],
            "pii_violations": pii_violations,
            "gdpr_status": gdpr_status,
            "timestamp": self._get_timestamp()
        }
    
    def _get_timestamp(self) -> str:
        """Get current timestamp for logging"""
        from datetime import datetime
        return datetime.now().isoformat()
