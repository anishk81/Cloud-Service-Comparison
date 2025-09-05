from models import AWSService, ServiceCategory, PricingModel

# Sample AWS services data
AWS_SERVICES = [
    AWSService(
        id="ec2",
        name="Amazon EC2",
        description="Elastic Compute Cloud - Scalable virtual servers in the cloud",
        category=ServiceCategory.COMPUTE,
        key_features=[
            "Scalable compute capacity",
            "Multiple instance types",
            "Flexible pricing options",
            "High availability",
            "Security groups and VPCs",
            "Auto Scaling",
            "Load balancing integration"
        ],
        pricing_notes="Pricing based on instance type, region, and usage time. Free tier includes 750 hours per month of t2.micro instances.",
        pricing_models=[PricingModel.ON_DEMAND, PricingModel.RESERVED, PricingModel.SPOT, PricingModel.FREE_TIER],
        use_cases=[
            "Web applications",
            "Development environments",
            "Batch processing",
            "High-performance computing",
            "Enterprise applications"
        ],
        limitations=[
            "Instance limits per region",
            "Network performance varies by instance type",
            "Storage is separate service"
        ],
        free_tier_available=True,
        documentation_url="https://docs.aws.amazon.com/ec2/"
    ),
    AWSService(
        id="lambda",
        name="AWS Lambda",
        description="Run code without provisioning or managing servers",
        category=ServiceCategory.SERVERLESS,
        key_features=[
            "Serverless compute",
            "Event-driven execution",
            "Automatic scaling",
            "Pay-per-request pricing",
            "Multiple language support",
            "Built-in monitoring",
            "VPC support"
        ],
        pricing_notes="Pay only for compute time consumed. Free tier includes 1M requests and 400,000 GB-seconds per month.",
        pricing_models=[PricingModel.PAY_PER_USE, PricingModel.FREE_TIER],
        use_cases=[
            "API backends",
            "Data processing",
            "Real-time file processing",
            "Microservices",
            "Event-driven applications"
        ],
        limitations=[
            "15-minute maximum execution time",
            "10GB memory limit",
            "Cold start latency",
            "Concurrent execution limits"
        ],
        free_tier_available=True,
        documentation_url="https://docs.aws.amazon.com/lambda/"
    ),
    AWSService(
        id="s3",
        name="Amazon S3",
        description="Simple Storage Service - Object storage built to store and retrieve any amount of data",
        category=ServiceCategory.STORAGE,
        key_features=[
            "Virtually unlimited storage",
            "99.999999999% durability",
            "Multiple storage classes",
            "Lifecycle policies",
            "Versioning",
            "Cross-region replication",
            "Server-side encryption"
        ],
        pricing_notes="Pay for storage used, requests, and data transfer. Free tier includes 5GB standard storage and 2,000 PUT requests.",
        pricing_models=[PricingModel.PAY_PER_USE, PricingModel.FREE_TIER],
        use_cases=[
            "Backup and archiving",
            "Static website hosting",
            "Data lakes",
            "Content distribution",
            "Big data analytics"
        ],
        limitations=[
            "Object size limit of 5TB",
            "Request rate limits",
            "Cross-region transfer costs"
        ],
        free_tier_available=True,
        documentation_url="https://docs.aws.amazon.com/s3/"
    ),
    AWSService(
        id="rds",
        name="Amazon RDS",
        description="Relational Database Service - Managed relational database service",
        category=ServiceCategory.DATABASE,
        key_features=[
            "Automated backups",
            "Multi-AZ deployments",
            "Read replicas",
            "Automatic software patching",
            "Monitoring and metrics",
            "Multiple database engines",
            "Encryption at rest and in transit"
        ],
        pricing_notes="Pricing based on instance class, storage, and backup storage. Free tier includes 750 hours of db.t2.micro instances.",
        pricing_models=[PricingModel.ON_DEMAND, PricingModel.RESERVED, PricingModel.FREE_TIER],
        use_cases=[
            "Web applications",
            "E-commerce platforms",
            "Enterprise applications",
            "Data warehousing",
            "Analytics workloads"
        ],
        limitations=[
            "Storage limits vary by engine",
            "Connection limits",
            "Some features vary by database engine"
        ],
        free_tier_available=True,
        documentation_url="https://docs.aws.amazon.com/rds/"
    ),
    AWSService(
        id="dynamodb",
        name="Amazon DynamoDB",
        description="Fast and flexible NoSQL database service",
        category=ServiceCategory.DATABASE,
        key_features=[
            "Single-digit millisecond latency",
            "Fully managed",
            "Automatic scaling",
            "Global tables",
            "Built-in security",
            "Backup and restore",
            "Point-in-time recovery"
        ],
        pricing_notes="Pay for read/write capacity units and storage. Free tier includes 25GB storage and 25 read/write capacity units.",
        pricing_models=[PricingModel.ON_DEMAND, PricingModel.PAY_PER_USE, PricingModel.FREE_TIER],
        use_cases=[
            "Mobile applications",
            "Gaming",
            "IoT applications",
            "Real-time bidding",
            "Session management"
        ],
        limitations=[
            "400KB item size limit",
            "Limited query capabilities",
            "No joins or complex transactions"
        ],
        free_tier_available=True,
        documentation_url="https://docs.aws.amazon.com/dynamodb/"
    ),
    AWSService(
        id="vpc",
        name="Amazon VPC",
        description="Virtual Private Cloud - Isolated cloud resources",
        category=ServiceCategory.NETWORKING,
        key_features=[
            "Logically isolated network",
            "Control over IP address ranges",
            "Subnet configuration",
            "Route tables",
            "Internet and NAT gateways",
            "VPN connections",
            "VPC peering"
        ],
        pricing_notes="VPC itself is free. Charges apply for VPN connections, NAT gateways, and data transfer.",
        pricing_models=[PricingModel.FREE_TIER, PricingModel.PAY_PER_USE],
        use_cases=[
            "Secure cloud environments",
            "Hybrid cloud architectures",
            "Multi-tier applications",
            "Compliance requirements",
            "Network isolation"
        ],
        limitations=[
            "Route table limits",
            "Security group limits",
            "Peering connection limits"
        ],
        free_tier_available=True,
        documentation_url="https://docs.aws.amazon.com/vpc/"
    ),
    AWSService(
        id="iam",
        name="AWS IAM",
        description="Identity and Access Management - Manage access to AWS services and resources",
        category=ServiceCategory.SECURITY,
        key_features=[
            "Fine-grained permissions",
            "Multi-factor authentication",
            "Identity federation",
            "Access analyzer",
            "Temporary security credentials",
            "CloudTrail integration",
            "Policy simulation"
        ],
        pricing_notes="IAM is free to use. No additional charges for basic IAM features.",
        pricing_models=[PricingModel.FREE_TIER],
        use_cases=[
            "User access management",
            "Service-to-service authentication",
            "Compliance and auditing",
            "Temporary access",
            "Cross-account access"
        ],
        limitations=[
            "Policy size limits",
            "Number of roles/users limits",
            "Regional availability varies for some features"
        ],
        free_tier_available=True,
        documentation_url="https://docs.aws.amazon.com/iam/"
    ),
    AWSService(
        id="cloudwatch",
        name="Amazon CloudWatch",
        description="Monitoring and observability service",
        category=ServiceCategory.MANAGEMENT,
        key_features=[
            "Metrics and logs",
            "Alarms and notifications",
            "Dashboards",
            "Events and rules",
            "Container insights",
            "Application insights",
            "Custom metrics"
        ],
        pricing_notes="Pay for metrics, logs ingestion, storage, and API requests. Free tier includes basic monitoring.",
        pricing_models=[PricingModel.PAY_PER_USE, PricingModel.FREE_TIER],
        use_cases=[
            "Application monitoring",
            "Infrastructure monitoring",
            "Log analysis",
            "Automated responses",
            "Performance optimization"
        ],
        limitations=[
            "Metric resolution limits",
            "Log retention costs",
            "API rate limits"
        ],
        free_tier_available=True,
        documentation_url="https://docs.aws.amazon.com/cloudwatch/"
    ),
    AWSService(
        id="ecs",
        name="Amazon ECS",
        description="Elastic Container Service - Fully managed container orchestration service",
        category=ServiceCategory.CONTAINERS,
        key_features=[
            "Docker container management",
            "Fargate serverless option",
            "Auto Scaling",
            "Load balancer integration",
            "Service discovery",
            "Blue/green deployments",
            "IAM integration"
        ],
        pricing_notes="No additional charges for ECS. Pay for underlying AWS resources (EC2, Fargate).",
        pricing_models=[PricingModel.PAY_PER_USE, PricingModel.ON_DEMAND],
        use_cases=[
            "Microservices",
            "Batch processing",
            "Web applications",
            "Machine learning workloads",
            "Legacy application modernization"
        ],
        limitations=[
            "Task definition limits",
            "Service limits per cluster",
            "Container instance limits"
        ],
        free_tier_available=False,
        documentation_url="https://docs.aws.amazon.com/ecs/"
    ),
    AWSService(
        id="sagemaker",
        name="Amazon SageMaker",
        description="Build, train, and deploy machine learning models",
        category=ServiceCategory.MACHINE_LEARNING,
        key_features=[
            "Jupyter notebooks",
            "Built-in algorithms",
            "Model training",
            "Hyperparameter tuning",
            "Model hosting",
            "A/B testing",
            "Model monitoring"
        ],
        pricing_notes="Pay for compute instances, storage, and data processing. Free tier includes limited notebook usage.",
        pricing_models=[PricingModel.ON_DEMAND, PricingModel.PAY_PER_USE, PricingModel.FREE_TIER],
        use_cases=[
            "Predictive analytics",
            "Computer vision",
            "Natural language processing",
            "Fraud detection",
            "Recommendation systems"
        ],
        limitations=[
            "Instance type availability",
            "Model size limits",
            "Endpoint limits"
        ],
        free_tier_available=True,
        documentation_url="https://docs.aws.amazon.com/sagemaker/"
    )
]

def get_all_services():
    return AWS_SERVICES

def get_service_by_id(service_id: str):
    return next((service for service in AWS_SERVICES if service.id == service_id), None)

def get_services_by_category(category: ServiceCategory):
    return [service for service in AWS_SERVICES if service.category == category]

def get_all_categories():
    return list(ServiceCategory)
