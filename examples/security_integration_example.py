"""
Example: Integrating Reference Document Integrity Verification

This shows how to integrate security.py into your assessment workflow.

USAGE IN YOUR WORKFLOW:
Add verification at the START of any workflow that loads reference documents.
"""

from pathlib import Path
from security import verify_reference_documents, SecurityError


def load_question_bank_safely():
    """
    Load question bank with integrity verification.
    
    BEFORE (insecure):
        with open('question_bank.json') as f:
            questions = json.load(f)
    
    AFTER (secure):
        verify_reference_documents()  # <- Add this line
        with open('question_bank.json') as f:
            questions = json.load(f)
    """
    import json
    
    try:
        # STEP 1: Verify integrity BEFORE loading
        print("🔍 Verifying reference document integrity...")
        verifier = verify_reference_documents()
        print("✅ All reference documents verified")
        
        # STEP 2: Now safe to load
        print("📂 Loading question bank...")
        with open('question_bank.json', 'r') as f:
            questions = json.load(f)
        
        print(f"✅ Loaded {len(questions['questions'])} questions")
        return questions
        
    except SecurityError as e:
        # CRITICAL: Document integrity check failed
        print(f"\n🔴 SECURITY ERROR: {e}")
        print("\n⛔ Assessment ABORTED - Cannot proceed with tampered documents")
        raise
    except Exception as e:
        print(f"\n❌ ERROR: {e}")
        raise


def example_workflow_integration():
    """
    Example: Full assessment workflow with security checks.
    """
    print("="*80)
    print("ASSESSMENT WORKFLOW - With Security Integration")
    print("="*80)
    
    # STEP 1: Verify all reference documents at workflow start
    try:
        print("\n[SECURITY CHECK] Verifying reference documents...")
        verifier = verify_reference_documents()
        
        # Get and display verification log
        log = verifier.get_verification_log()
        print(f"✅ {len(log)} documents verified successfully")
        
    except SecurityError as e:
        print(f"\n🔴 SECURITY ALERT: {e}")
        print("\n⛔ Workflow TERMINATED for security reasons")
        return False
    
    # STEP 2: Now safe to proceed with assessment
    print("\n[WORKFLOW] Starting assessment...")
    questions = load_question_bank_safely()
    
    # STEP 3: Continue with normal workflow
    print(f"[WORKFLOW] Assessment ready with {len(questions['questions'])} questions")
    
    # Rest of your workflow...
    print("\n✅ Workflow completed successfully")
    return True


if __name__ == "__main__":
    print("\n" + "="*80)
    print("INTEGRATION EXAMPLE")
    print("="*80)
    
    # Run example workflow
    success = example_workflow_integration()
    
    print("\n" + "="*80)
    if success:
        print("✅ Integration example completed successfully")
    else:
        print("❌ Integration example failed (security check)")
    print("="*80 + "\n")
