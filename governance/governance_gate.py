"""
Governance Gate - Main Orchestrator for All Governance Checks
RUBRIC: Governance & Compliance (10 marks total)
- PII detection implemented (3 marks)
- GDPR compliance checks (2 marks)
- Content safety validation (2 marks)
- Audit logging (3 marks)

TASK: Implement main governance orchestrator with audit logging
"""
import logging
from typing import Dict, Any, List
from datetime import datetime

from governance.safety_validator import SafetyValidator
from governance.compliance_checker import ComplianceChecker

class GovernanceGate:
    """The main orchestrator that coordinates all governance checks"""
    
    def __init__(self):
        """
        Initialize governance gate with all validators
        
        HINT: Initialize:
        1. Safety Validator
        2. Compliance Checker
        3. Set up audit logging
        """
        # HINT: Initialize Safety Validator
        self.safety_validator = SafetyValidator()
        
        # HINT: Initialize Compliance Checker
        self.compliance_checker = ComplianceChecker()
        
        # HINT: Set up audit logging
        self.logger = logging.getLogger(__name__)
        self._setup_audit_logging()
    
    def _setup_audit_logging(self):
        """Set up audit logging configuration"""
        # HINT: Configure audit logger
        audit_logger = logging.getLogger("governance.audit")
        audit_logger.setLevel(logging.INFO)
        
        # HINT: Create audit log handler if not exists
        if not audit_logger.handlers:
            handler = logging.FileHandler("logs/audit.log")
            formatter = logging.Formatter(
                '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
            )
            handler.setFormatter(formatter)
            audit_logger.addHandler(handler)
    
    def validate_input(self, text: str) -> Dict[str, Any]:
        """
        Validate input text through all governance checks
        
        HINT: Perform:
        1. Safety validation (prompt injection, content safety)
        2. Compliance validation (PII, GDPR)
        3. Audit logging
        4. Return combined results
        """
        # HINT: Perform safety validation
        safety_check = self.safety_validator.validate_input_safety(text)
        
        # HINT: Perform compliance validation
        compliance_check = self.compliance_checker.validate_compliance(text)
        
        # HINT: Determine overall validation result
        is_valid = safety_check["is_safe"] and compliance_check["is_compliant"]
        
        # HINT: Collect all violations
        all_violations = []
        
        # Add safety violations
        if not safety_check["is_safe"]:
            if safety_check["prompt_injection_check"]["violations"]:
                all_violations.extend(safety_check["prompt_injection_check"]["violations"])
            if safety_check["content_safety_check"]["violations"]:
                all_violations.extend(safety_check["content_safety_check"]["violations"])
        
        # Add compliance violations
        if not compliance_check["is_compliant"]:
            if compliance_check["pii_violations"]:
                for pii_type, values in compliance_check["pii_violations"].items():
                    all_violations.append(f"PII violation: {pii_type} - {', '.join(values)}")
        
        # HINT: Audit log entry
        audit_entry = {
            "timestamp": datetime.now().isoformat(),
            "action": "input_validation",
            "text_length": len(text),
            "is_valid": is_valid,
            "violations_count": len(all_violations),
            "violations": all_violations,
            "safety_check": safety_check,
            "compliance_check": compliance_check
        }
        
        # HINT: Log audit entry
        audit_logger = logging.getLogger("governance.audit")
        audit_logger.info(f"Input validation: valid={is_valid}, violations={len(all_violations)}")
        
        # HINT: Return validation result
        return {
            "is_valid": is_valid,
            "violations": all_violations,
            "safety_check": safety_check,
            "compliance_check": compliance_check,
            "audit_entry": audit_entry
        }
    
    def validate_output(self, text: str) -> Dict[str, Any]:
        """
        Validate output text through all governance checks
        
        HINT: Perform:
        1. Output safety validation (content safety, PII leakage)
        2. Audit logging
        3. Return combined results
        """
        # HINT: Perform output safety validation
        output_safety_check = self.safety_validator.validate_output_safety(text)
        
        # HINT: Determine overall validation result
        is_valid = output_safety_check["is_safe"]
        
        # HINT: Collect all violations
        all_violations = []
        
        # Add output safety violations
        if not output_safety_check["is_safe"]:
            if output_safety_check["content_safety_check"]["violations"]:
                all_violations.extend(output_safety_check["content_safety_check"]["violations"])
            if output_safety_check["pii_check"]["has_pii"]:
                all_violations.append(f"PII leakage detected: {', '.join(output_safety_check['pii_check']['pii_types'])}")
        
        # HINT: Audit log entry
        audit_entry = {
            "timestamp": datetime.now().isoformat(),
            "action": "output_validation",
            "text_length": len(text),
            "is_valid": is_valid,
            "violations_count": len(all_violations),
            "violations": all_violations,
            "output_safety_check": output_safety_check
        }
        
        # HINT: Log audit entry
        audit_logger = logging.getLogger("governance.audit")
        audit_logger.info(f"Output validation: valid={is_valid}, violations={len(all_violations)}")
        
        # HINT: Return validation result
        return {
            "is_valid": is_valid,
            "violations": all_violations,
            "output_safety_check": output_safety_check,
            "audit_entry": audit_entry
        }
    
    def get_governance_report(self) -> Dict[str, Any]:
        """
        Generate comprehensive governance report
        
        HINT: Return summary of governance configuration
        and capabilities
        """
        return {
            "governance_gate_version": "1.0.0",
            "capabilities": [
                "Prompt injection detection",
                "Content safety validation", 
                "PII detection and redaction",
                "GDPR compliance checking",
                "Audit logging",
                "Output safety validation"
            ],
            "validators": {
                "safety_validator": {
                    "enabled": True,
                    "checks": ["prompt_injection", "content_safety", "output_safety"]
                },
                "compliance_checker": {
                    "enabled": True,
                    "checks": ["pii_detection", "gdpr_compliance"]
                }
            },
            "audit_logging": {
                "enabled": True,
                "log_file": "logs/audit.log",
                "log_level": "INFO"
            },
            "timestamp": datetime.now().isoformat()
        }
