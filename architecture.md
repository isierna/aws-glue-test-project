# Learning Pipeline Architecture

## Flow
1. **Glue Workflow** (manual trigger) → `learning-pipeline-workflow-isierna`
   - Crawler: `learning-pipeline-crawler-isierna`
   - ETL Job: `learning-pipeline-etl-isierna`

2. **EventBridge Rule** → `learning-pipeline-test-trigger-isierna`
   - Trigger: Glue ETL job SUCCEEDED
   - Target: Lambda function

3. **Lambda** → `learning-pipeline-tests-isierna`
   - Runs pytest tests against S3 output
   - Results visible in CloudWatch logs

## Resources
| Resource | Name | Service |
|---|---|---|
| Workflow | learning-pipeline-workflow-isierna | Glue |
| Crawler | learning-pipeline-crawler-isierna | Glue |
| ETL Job | learning-pipeline-etl-isierna | Glue |
| EventBridge Rule | learning-pipeline-test-trigger-isierna | EventBridge |
| Lambda | learning-pipeline-tests-isierna | Lambda |
| S3 Bucket | isierna-bucket | S3 |
| RDS | learning-pipeline-db-isierna | RDS |
| Parameter Store | /learning-pipeline/rds/password | SSM |