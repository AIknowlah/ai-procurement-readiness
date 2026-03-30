"""
============================================================================
AI Procurement Readiness Tool - BigQuery Storage Client
============================================================================
Version: 1.0
Date: 2026-03-30
Purpose: Handle all BigQuery operations for assessment storage

GOVERNANCE SIGNIFICANCE:
This module implements append-only immutable storage.
No UPDATE or DELETE operations allowed.
Every assessment is a permanent audit record.
============================================================================
"""

from google.cloud import bigquery
from google.api_core import retry
from google.cloud.exceptions import NotFound
from typing import Dict, List, Optional
import os
from datetime import datetime
import json
from dotenv import load_dotenv

# Load environment variables
load_dotenv()


class AssessmentStorage:
    """
    Manages BigQuery operations for AI procurement assessments.
    
    ARCHITECTURE NOTES:
    - Append-only: Only INSERT operations, never UPDATE/DELETE
    - Immutability: Each assessment is permanent record
    - Audit trail: Complete history preserved
    - Region: asia-southeast1 (Singapore)
    
    GOVERNANCE COMPLIANCE:
    - Aligns with PDPA audit requirements
    - Supports 7-year retention policy
    - Access controlled via GCP IAM
    """
    
    def __init__(
        self, 
        project_id: Optional[str] = None,
        dataset_id: str = "procurement_assessments",
        table_id: str = "assessments"
    ):
        """
        Initialize BigQuery client.
        
        Args:
            project_id: GCP project ID (defaults to env var GCP_PROJECT_ID)
            dataset_id: BigQuery dataset name
            table_id: BigQuery table name
            
        Environment Variables Required:
            GCP_PROJECT_ID: Your GCP project ID
            GOOGLE_APPLICATION_CREDENTIALS: Path to service account key JSON
        """
        self.project_id = project_id or os.getenv('GCP_PROJECT_ID')
        
        if not self.project_id:
            raise ValueError(
                "GCP_PROJECT_ID must be set in environment or passed as argument"
            )
        
        self.dataset_id = dataset_id
        self.table_id = table_id
        
        # Initialize BigQuery client
        self.client = bigquery.Client(project=self.project_id)
        
        # Full table reference
        self.table_ref = f"{self.project_id}.{self.dataset_id}.{self.table_id}"
        
    def create_table_if_not_exists(self) -> bool:
        """
        Create assessments table if it doesn't exist.
        
        Returns:
            True if table was created, False if already exists
            
        GOVERNANCE NOTE:
        Table schema enforces data structure and integrity.
        Partitioning by assessment_date enables efficient queries.
        """
        try:
            self.client.get_table(self.table_ref)
            print(f"Table {self.table_ref} already exists.")
            return False
        except NotFound:
            print(f"Creating table {self.table_ref}...")
            
            # Define schema
            schema = [
                bigquery.SchemaField("assessment_id", "STRING", mode="REQUIRED", 
                                    description="Unique assessment identifier"),
                bigquery.SchemaField("vendor_name", "STRING", mode="REQUIRED",
                                    description="Name of AI system vendor"),
                bigquery.SchemaField("system_name", "STRING", mode="NULLABLE",
                                    description="Name of the AI system/product"),
                bigquery.SchemaField("system_description", "STRING", mode="NULLABLE",
                                    description="Description of AI system functionality"),
                
                bigquery.SchemaField("assessment_date", "TIMESTAMP", mode="REQUIRED",
                                    description="Date assessment was conducted"),
                bigquery.SchemaField("assessor_id", "STRING", mode="REQUIRED",
                                    description="ID of government officer"),
                bigquery.SchemaField("assessor_agency", "STRING", mode="NULLABLE",
                                    description="Government agency of assessor"),
                bigquery.SchemaField("assessment_status", "STRING", mode="REQUIRED",
                                    description="Status: draft, submitted, reviewed, approved"),
                
                bigquery.SchemaField("principle_scores", "JSON", mode="REQUIRED",
                                    description="Scores per principle (JSON object)"),
                bigquery.SchemaField("total_readiness_score", "FLOAT", mode="REQUIRED",
                                    description="Overall readiness score (0.0 to 1.0)"),
                
                bigquery.SchemaField("responses", "JSON", mode="REQUIRED",
                                    description="All 90 Q&A pairs with evidence"),
                bigquery.SchemaField("evidence_files", "JSON", mode="NULLABLE",
                                    description="Evidence file metadata array"),
                
                bigquery.SchemaField("created_at", "TIMESTAMP", mode="REQUIRED",
                                    description="Record creation timestamp"),
                bigquery.SchemaField("last_modified_at", "TIMESTAMP", mode="REQUIRED",
                                    description="Last modification timestamp"),
                
                bigquery.SchemaField("procurement_stage", "STRING", mode="NULLABLE",
                                    description="Procurement stage context"),
                bigquery.SchemaField("estimated_contract_value", "FLOAT", mode="NULLABLE",
                                    description="Estimated contract value (SGD)"),
                bigquery.SchemaField("notes", "STRING", mode="NULLABLE",
                                    description="Additional assessor notes"),
            ]
            
            # Create table with partitioning
            table = bigquery.Table(self.table_ref, schema=schema)
            
            # Partition by assessment_date for query performance
            table.time_partitioning = bigquery.TimePartitioning(
                type_=bigquery.TimePartitioningType.DAY,
                field="assessment_date"
            )
            
            # Cluster by vendor_name and assessment_status
            table.clustering_fields = ["vendor_name", "assessment_status"]
            
            table = self.client.create_table(table)
            print(f"Created table {self.table_ref}")
            return True
    
    @retry.Retry(deadline=30)
    def insert_assessment(self, assessment_record: Dict) -> str:
        """
        Insert new assessment into BigQuery.
        
        Args:
            assessment_record: Complete assessment data dictionary
            
        Returns:
            assessment_id of inserted record
            
        Raises:
            ValueError: If insertion fails or required fields missing
            
        GOVERNANCE NOTES:
        - Append-only: This only INSERTs, never UPDATEs
        - Retry logic handles transient network failures
        - Validation ensures data integrity before insertion
        
        Example:
            >>> storage = AssessmentStorage()
            >>> assessment = {
            ...     "assessment_id": "ASM-2026-001",
            ...     "vendor_name": "Example AI Corp",
            ...     "principle_scores": {"P1_Transparency": 0.80, ...},
            ...     "total_readiness_score": 0.85,
            ...     # ... other required fields
            ... }
            >>> assessment_id = storage.insert_assessment(assessment)
        """
        # Validate required fields
        required_fields = [
            "assessment_id", "vendor_name", "assessment_date",
            "assessor_id", "assessment_status", "principle_scores",
            "total_readiness_score", "responses", "created_at", "last_modified_at"
        ]
        
        missing_fields = [field for field in required_fields if field not in assessment_record]
        if missing_fields:
            raise ValueError(f"Missing required fields: {missing_fields}")
        
        # Ensure timestamps are strings (BigQuery requires ISO 8601 format)
        for timestamp_field in ["assessment_date", "created_at", "last_modified_at"]:
            if isinstance(assessment_record[timestamp_field], datetime):
                assessment_record[timestamp_field] = assessment_record[timestamp_field].isoformat()
        
        # Convert principle_scores dict to JSON string if needed
        if isinstance(assessment_record.get("principle_scores"), dict):
            assessment_record["principle_scores"] = json.dumps(assessment_record["principle_scores"])
        
        # Convert responses list to JSON string if needed
        if isinstance(assessment_record.get("responses"), list):
            assessment_record["responses"] = json.dumps(assessment_record["responses"])
        
        # Convert evidence_files to JSON string if present
        if assessment_record.get("evidence_files") and isinstance(assessment_record["evidence_files"], list):
            assessment_record["evidence_files"] = json.dumps(assessment_record["evidence_files"])
        
        # Insert record
        errors = self.client.insert_rows_json(self.table_ref, [assessment_record])
        
        if errors:
            raise ValueError(f"BigQuery insert failed: {errors}")
        
        print(f"Successfully inserted assessment: {assessment_record['assessment_id']}")
        return assessment_record['assessment_id']
    
    def get_assessment_by_id(self, assessment_id: str) -> Optional[Dict]:
        """
        Retrieve assessment by ID.
        
        Args:
            assessment_id: Unique assessment identifier
            
        Returns:
            Assessment record as dictionary, or None if not found
            
        Example:
            >>> storage = AssessmentStorage()
            >>> assessment = storage.get_assessment_by_id("ASM-2026-001")
        """
        query = f"""
            SELECT *
            FROM `{self.table_ref}`
            WHERE assessment_id = @assessment_id
            LIMIT 1
        """
        
        job_config = bigquery.QueryJobConfig(
            query_parameters=[
                bigquery.ScalarQueryParameter("assessment_id", "STRING", assessment_id)
            ]
        )
        
        query_job = self.client.query(query, job_config=job_config)
        results = list(query_job.result())
        
        if not results:
            return None
        
        # Convert Row to dictionary
        row = results[0]
        return dict(row.items())
    
    def list_assessments_by_vendor(
        self, 
        vendor_name: str,
        limit: int = 10
    ) -> List[Dict]:
        """
        List all assessments for a vendor.
        
        Args:
            vendor_name: Vendor name to filter by
            limit: Maximum number of results
            
        Returns:
            List of assessment records
            
        GOVERNANCE NOTE:
        Useful for tracking vendor assessments over time.
        Shows progression of readiness scores across assessments.
        """
        query = f"""
            SELECT 
                assessment_id,
                vendor_name,
                system_name,
                assessment_date,
                total_readiness_score,
                assessment_status
            FROM `{self.table_ref}`
            WHERE vendor_name = @vendor_name
            ORDER BY assessment_date DESC
            LIMIT @limit
        """
        
        job_config = bigquery.QueryJobConfig(
            query_parameters=[
                bigquery.ScalarQueryParameter("vendor_name", "STRING", vendor_name),
                bigquery.ScalarQueryParameter("limit", "INT64", limit)
            ]
        )
        
        query_job = self.client.query(query, job_config=job_config)
        results = query_job.result()
        
        return [dict(row.items()) for row in results]
    
    def get_assessment_statistics(self) -> Dict:
        """
        Get overall statistics across all assessments.
        
        Returns:
            Dictionary with statistics:
            - total_assessments
            - unique_vendors
            - average_readiness_score
            - assessments_by_status
            
        GOVERNANCE NOTE:
        Useful for governance reporting and trend analysis.
        """
        query = f"""
            SELECT 
                COUNT(*) as total_assessments,
                COUNT(DISTINCT vendor_name) as unique_vendors,
                AVG(total_readiness_score) as avg_readiness_score,
                COUNTIF(assessment_status = 'draft') as draft_count,
                COUNTIF(assessment_status = 'submitted') as submitted_count,
                COUNTIF(assessment_status = 'reviewed') as reviewed_count,
                COUNTIF(assessment_status = 'approved') as approved_count
            FROM `{self.table_ref}`
        """
        
        query_job = self.client.query(query)
        results = list(query_job.result())
        
        if not results:
            return {}
        
        return dict(results[0].items())


# ============================================================================
# EXAMPLE USAGE
# ============================================================================

if __name__ == "__main__":
    print("=" * 60)
    print("BIGQUERY STORAGE CLIENT - EXAMPLE USAGE")
    print("=" * 60)
    
    # NOTE: This example won't run without proper GCP credentials
    # It's here to show the API usage pattern
    
    print("\n1. Initialize storage client:")
    print("   storage = AssessmentStorage()")
    print("   storage.create_table_if_not_exists()")
    
    print("\n2. Prepare assessment record:")
    print("   assessment = {")
    print("       'assessment_id': 'ASM-2026-001',")
    print("       'vendor_name': 'Example AI Corp',")
    print("       'principle_scores': {...},")
    print("       'total_readiness_score': 0.85,")
    print("       'responses': [...],")
    print("       # ... other fields")
    print("   }")
    
    print("\n3. Insert assessment:")
    print("   assessment_id = storage.insert_assessment(assessment)")
    
    print("\n4. Retrieve assessment:")
    print("   assessment = storage.get_assessment_by_id('ASM-2026-001')")
    
    print("\n5. List vendor assessments:")
    print("   assessments = storage.list_assessments_by_vendor('Example AI Corp')")
    
    print("\n6. Get statistics:")
    print("   stats = storage.get_assessment_statistics()")
    
    print("\n" + "=" * 60)
    print("To run this code:")
    print("1. Set GCP_PROJECT_ID in .env file")
    print("2. Set GOOGLE_APPLICATION_CREDENTIALS in .env")
    print("3. Ensure service account has BigQuery Data Editor role")
    print("=" * 60)
