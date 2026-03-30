"""
============================================================================
Generate Assessment Report from BigQuery
============================================================================
Version: 1.0
Date: 2026-03-30
Purpose: Pull assessment from BigQuery and generate Word report

USAGE:
    python generate_report_from_bigquery.py ASM-2026-001
============================================================================
"""

import sys
from bigquery_storage import AssessmentStorage
from report_generator import AssessmentReportGenerator


def generate_report_for_assessment(assessment_id: str):
    """
    Generate Word report for a specific assessment.
    
    Args:
        assessment_id: Assessment ID from BigQuery
        
    Returns:
        Path to generated report
    """
    print(f"\n{'='*60}")
    print(f"GENERATING REPORT FOR {assessment_id}")
    print(f"{'='*60}\n")
    
    # Step 1: Fetch assessment from BigQuery
    print(f"[1/3] Fetching assessment from BigQuery...")
    storage = AssessmentStorage(dataset_id="procurement_assessments")
    assessment_data = storage.get_assessment_by_id(assessment_id)
    
    if not assessment_data:
        print(f"❌ ERROR: Assessment {assessment_id} not found in BigQuery")
        return None
    
    print(f"✓ Found assessment for vendor: {assessment_data['vendor_name']}")
    
    # Step 2: Generate report
    print(f"\n[2/3] Generating Word document...")
    generator = AssessmentReportGenerator()
    report_filename = generator.generate_report(assessment_data)
    
    # Step 3: Confirm
    print(f"\n[3/3] Complete!")
    print(f"{'='*60}")
    print(f"Report generated: {report_filename}")
    print(f"Vendor: {assessment_data['vendor_name']}")
    print(f"Readiness: {assessment_data['total_readiness_score']:.0%}")
    print(f"{'='*60}\n")
    
    return report_filename


def list_available_assessments():
    """List all assessments in BigQuery."""
    print("\nAvailable Assessments:")
    print("=" * 60)
    
    storage = AssessmentStorage(dataset_id="procurement_assessments")
    
    # Query all assessments
    from google.cloud import bigquery
    query = f"""
        SELECT 
            assessment_id,
            vendor_name,
            total_readiness_score,
            assessment_date,
            assessment_status
        FROM `{storage.table_ref}`
        ORDER BY assessment_date DESC
    """
    
    results = storage.client.query(query).result()
    
    for row in results:
        print(f"{row.assessment_id:25} | {row.vendor_name:20} | {row.total_readiness_score:.0%} | {row.assessment_status}")
    
    print("=" * 60)


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("\nUSAGE:")
        print("  python generate_report_from_bigquery.py <assessment_id>")
        print("\nEXAMPLE:")
        print("  python generate_report_from_bigquery.py ASM-2026-001")
        print()
        
        # List available assessments
        try:
            list_available_assessments()
        except Exception as e:
            print(f"Could not list assessments: {e}")
    else:
        assessment_id = sys.argv[1]
        generate_report_for_assessment(assessment_id)
