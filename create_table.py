from bigquery_storage import AssessmentStorage

# Initialize storage client with correct dataset name
storage = AssessmentStorage(dataset_id="procurement_assessments")

# Create table if it doesn't exist
created = storage.create_table_if_not_exists()

if created:
    print("✓ Table created successfully!")
else:
    print("✓ Table already exists!")