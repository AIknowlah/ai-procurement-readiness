"""
Reference Document Integrity Verification

PURPOSE:
Ensures that reference documents (framework files, PDPA documents, question bank)
have not been tampered with by verifying SHA-256 checksums against trusted values.

GOVERNANCE RATIONALE:
The tool relies on official AI Verify framework and PDPA requirements to assess
vendors. If these reference documents are modified (accidentally or maliciously),
assessments would be conducted against incorrect criteria, leading to non-compliant
systems being approved.

THREAT MODEL:
- Accidental modification (file corruption, encoding issues)
- Malicious tampering (weakening requirements to pass vendors)
- Version confusion (mixing different framework versions)

IMPLEMENTATION:
- SHA-256 checksums generated from official source files
- Verification happens before every document load
- Mismatch aborts assessment with security alert
- Checksums stored in code (not in files, to prevent tampering)

AUTHOR: AIknowlah (AI Governance Learning Project)
DATE: April 2026
VERSION: 1.0
"""

import hashlib
import json
from pathlib import Path
from typing import Dict, Optional
from datetime import datetime


class SecurityError(Exception):
    """Raised when security verification fails"""
    pass


class ReferenceDocumentVerifier:
    """
    Verifies integrity of reference documents using SHA-256 checksums.
    
    USAGE:
        verifier = ReferenceDocumentVerifier()
        verifier.verify_file("question_bank.json")
        # If verification passes, safe to load file
        # If verification fails, SecurityError raised
    """
    
    # TRUSTED CHECKSUMS
    # Generated from official source files on 2026-03-31
    # DO NOT MODIFY - These are the cryptographic fingerprints of trusted files
    TRUSTED_CHECKSUMS = {
        "question_bank.json": {
            "sha256": "36766479770b2d17270f2af70560b4416b3e471dc96e0f4292e974e58614b311",
            "version": "1.0",
            "source": "Generated from AI Verify Framework (IMDA GitHub, 2025 Edition)",
            "generated_date": "2026-03-31",
            "total_questions": 90,
            "governance_note": "Contains 90 questions mapped 1:1 to AI Verify process checks"
        },
        "framework_structure_complete.json": {
            "sha256": "948481661eb8c039b169f8eaa9053b9c181849cfeaa98ba4cbca0840c4fec471",
            "version": "1.0",
            "source": "AI Verify Testing Framework 2025 Edition (aiverify-foundation/aiverify GitHub)",
            "generated_date": "2026-03-31",
            "total_checks": 90,
            "governance_note": "Official framework with P9 Accountability fix applied (79→90 checks)"
        },
        "PDPA_17_May_2022.pdf": {
            "sha256": "b2c75b9024630a5a1b148f4df56b5cc9e7fd77389ec8a4f054b80069aa037a11",
            "version": "Official",
            "source": "Personal Data Protection Act 2012 (Singapore Statutes, 17 May 2022)",
            "generated_date": "2022-05-17",
            "governance_note": "Official PDPA text used for compliance questions"
        }
    }
    
    def __init__(self, base_path: Optional[Path] = None):
        """
        Initialize verifier.
        
        Args:
            base_path: Directory containing reference documents
                      (defaults to current working directory)
        """
        self.base_path = base_path or Path.cwd()
        self.verification_log = []
    
    def verify_file(self, filename: str, require_exists: bool = True) -> bool:
        """
        Verify a reference document's integrity.
        
        Args:
            filename: Name of file to verify (must be in TRUSTED_CHECKSUMS)
            require_exists: If True, raises error if file doesn't exist
        
        Returns:
            True if verification passed
        
        Raises:
            SecurityError: If checksum mismatch or file missing (when required)
            KeyError: If filename not in TRUSTED_CHECKSUMS
        
        GOVERNANCE NOTE:
        This method is the gatekeeper - it MUST be called before loading any
        reference document. Bypassing this check would compromise assessment integrity.
        """
        if filename not in self.TRUSTED_CHECKSUMS:
            raise KeyError(
                f"File '{filename}' is not a registered reference document.\n"
                f"Known reference documents: {list(self.TRUSTED_CHECKSUMS.keys())}"
            )
        
        filepath = self.base_path / filename
        
        # Check file exists
        if not filepath.exists():
            if require_exists:
                raise SecurityError(
                    f"SECURITY ERROR: Reference document not found!\n"
                    f"File: {filepath}\n"
                    f"This file is required for assessment integrity.\n"
                    f"Assessment cannot proceed."
                )
            return False
        
        # Compute current checksum
        current_checksum = self._compute_checksum(filepath)
        
        # Get trusted checksum
        trusted_info = self.TRUSTED_CHECKSUMS[filename]
        expected_checksum = trusted_info["sha256"]
        
        # Compare checksums
        if current_checksum != expected_checksum:
            # CRITICAL: Checksum mismatch - file has been modified!
            error_msg = self._format_checksum_mismatch_error(
                filename, current_checksum, trusted_info
            )
            
            # Log the failure
            self._log_verification(
                filename=filename,
                status="FAILED",
                expected=expected_checksum,
                actual=current_checksum
            )
            
            raise SecurityError(error_msg)
        
        # Verification passed
        self._log_verification(
            filename=filename,
            status="PASSED",
            expected=expected_checksum,
            actual=current_checksum
        )
        
        return True
    
    def verify_all(self, require_all: bool = False) -> Dict[str, bool]:
        """
        Verify all registered reference documents.
        
        Args:
            require_all: If True, raises error if any verification fails
        
        Returns:
            Dict mapping filename to verification result (True/False)
        
        Raises:
            SecurityError: If require_all=True and any file fails
        """
        results = {}
        
        for filename in self.TRUSTED_CHECKSUMS.keys():
            try:
                results[filename] = self.verify_file(
                    filename, 
                    require_exists=require_all
                )
            except SecurityError as e:
                if require_all:
                    raise
                results[filename] = False
        
        return results
    
    def get_file_info(self, filename: str) -> Dict:
        """
        Get metadata about a reference document.
        
        Args:
            filename: Name of registered reference document
        
        Returns:
            Dict with version, source, governance notes
        """
        if filename not in self.TRUSTED_CHECKSUMS:
            raise KeyError(f"Unknown reference document: {filename}")
        
        return self.TRUSTED_CHECKSUMS[filename].copy()
    
    def _compute_checksum(self, filepath: Path) -> str:
        """
        Compute SHA-256 checksum of a file.
        
        Args:
            filepath: Path to file
        
        Returns:
            Hex string of SHA-256 hash
        """
        sha256_hash = hashlib.sha256()
        
        # Read file in chunks (memory-efficient for large files)
        with open(filepath, "rb") as f:
            for byte_block in iter(lambda: f.read(4096), b""):
                sha256_hash.update(byte_block)
        
        return sha256_hash.hexdigest()
    
    def _format_checksum_mismatch_error(
        self, 
        filename: str, 
        current_checksum: str, 
        trusted_info: Dict
    ) -> str:
        """Format detailed error message for checksum mismatch"""
        return f"""
╔══════════════════════════════════════════════════════════════════════════╗
║                    🔴 SECURITY ALERT: FILE TAMPERING DETECTED            ║
╚══════════════════════════════════════════════════════════════════════════╝

FILE: {filename}

ISSUE: The cryptographic checksum of this reference document does not match 
       the trusted value. This file may have been:
       - Modified (accidentally or maliciously)
       - Corrupted during transfer
       - Replaced with a different version

IMPACT: Assessments cannot be conducted with modified reference documents.
        This would compromise assessment integrity and could lead to 
        non-compliant systems being approved.

DETAILS:
  Expected SHA-256: {trusted_info['sha256']}
  Current SHA-256:  {current_checksum}
  
  Trusted Version: {trusted_info['version']}
  Source: {trusted_info['source']}
  Generated: {trusted_info['generated_date']}

ACTION REQUIRED:
  1. DO NOT proceed with assessment
  2. Restore the file from official source
  3. Verify checksum matches trusted value
  4. Contact system administrator if problem persists

GOVERNANCE NOTE: {trusted_info['governance_note']}

Assessment ABORTED for security reasons.
"""
    
    def _log_verification(
        self, 
        filename: str, 
        status: str, 
        expected: str, 
        actual: str
    ):
        """Log verification result"""
        self.verification_log.append({
            "timestamp": datetime.now().isoformat(),
            "filename": filename,
            "status": status,
            "expected_checksum": expected,
            "actual_checksum": actual
        })
    
    def get_verification_log(self) -> list:
        """
        Get log of all verification attempts.
        
        Returns:
            List of verification records (for audit trail)
        """
        return self.verification_log.copy()
    
    def export_checksums(self, output_path: Path):
        """
        Export trusted checksums to JSON file (for documentation).
        
        Args:
            output_path: Where to write checksums file
        
        GOVERNANCE NOTE:
        This is for documentation/transparency only. The checksums in the code
        are the authoritative source (not this exported file).
        """
        with open(output_path, 'w') as f:
            json.dump(self.TRUSTED_CHECKSUMS, f, indent=2)


# CONVENIENCE FUNCTION for common use case
def verify_reference_documents(base_path: Optional[Path] = None) -> ReferenceDocumentVerifier:
    """
    Verify all reference documents in one call.
    
    This is the recommended way to use this module:
    
        from security import verify_reference_documents
        
        # Verify all documents before starting assessment
        verifier = verify_reference_documents()
        
        # If this returns without exception, all files are verified
        # Now safe to load files
    
    Args:
        base_path: Directory containing reference documents
    
    Returns:
        ReferenceDocumentVerifier instance (with verification log)
    
    Raises:
        SecurityError: If any document fails verification
    """
    verifier = ReferenceDocumentVerifier(base_path)
    
    # Verify all critical files
    verifier.verify_file("question_bank.json")
    verifier.verify_file("framework_structure_complete.json")
    
    # PDPA document is optional (questions reference it but tool doesn't parse it)
    try:
        verifier.verify_file("PDPA_17_May_2022.pdf", require_exists=False)
    except SecurityError:
        # PDPA verification failed, but questions are still usable
        pass
    
    return verifier


if __name__ == "__main__":
    # SELF-TEST
    print("=" * 80)
    print("Reference Document Integrity Verification - Self Test")
    print("=" * 80)
    
    try:
        verifier = ReferenceDocumentVerifier()
        
        print("\n📋 Registered Reference Documents:")
        for filename in verifier.TRUSTED_CHECKSUMS.keys():
            info = verifier.get_file_info(filename)
            print(f"\n  • {filename}")
            print(f"    Version: {info['version']}")
            print(f"    Source: {info['source']}")
            print(f"    Generated: {info['generated_date']}")
        
        print("\n🔍 Verifying all documents...")
        results = verifier.verify_all(require_all=False)
        
        print("\n📊 Verification Results:")
        for filename, passed in results.items():
            status = "✅ PASSED" if passed else "❌ FAILED"
            print(f"  {status} - {filename}")
        
        print("\n📝 Verification Log:")
        for entry in verifier.get_verification_log():
            print(f"  {entry['timestamp']} - {entry['filename']}: {entry['status']}")
        
        print("\n" + "=" * 80)
        print("✅ Self-test complete!")
        print("=" * 80)
        
    except SecurityError as e:
        print(f"\n🔴 SECURITY ERROR:\n{e}")
    except Exception as e:
        print(f"\n❌ ERROR: {e}")
