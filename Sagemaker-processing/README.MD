## Flowty Image

### Overview

This example creates a custom image for ScriptProcessor from sagemaker.processing

### Creating the ECR repository
Create the ECR repository.
```
REGION=<aws-region>
REPOSITORY=<repository-name>

aws --region ${REGION} ecr create-repository \
    --repository-name ${REPOSITORY}
```
If successful returns

### Building the image
Build the Docker image and push to Amazon ECR.
```
# Modify these as required. The Docker registry endpoint can be tuned based on your current region from https://docs.aws.amazon.com/general/latest/gr/ecr.html#ecr-docker-endpoints

ACCOUNT_ID=<account-id>
IMAGE_NAME=<image-name>

aws --region ${REGION} ecr get-login-password | docker login 
    --username AWS 
    --password-stdin ${ACCOUNT_ID}.dkr.ecr.${REGION}.amazonaws.com/${REPOSITORY}
```

### Build the image
```
docker build . -t ${IMAGE_NAME} -t ${ACCOUNT_ID}.dkr.ecr.${REGION}.amazonaws.com/${REPOSITORY}:${IMAGE_NAME}
```
### Push the image
```
docker push ${ACCOUNT_ID}.dkr.ecr.${REGION}.amazonaws.com/${REPOSITORY}:${IMAGE_NAME}
```

### Using it with Sagemaker ScriptProcessor
Clone the git repository by running the following in a new notebook (Python 3)
```
!git clone https://github.com/vanbui24/flowty-sagemaker 
```

In the Sagemaker-processing folder: Open the sagemaker-processing notebook

Set the IMAGE_URI and ROLE_ARN

```
IAM Arn role in your account to be used with the SageMaker ScriptProcessor
ROLE_ARN=<role-arn>

IMAGE_URI = ${ACCOUNT_ID}.dkr.ecr.${REGION}.amazonaws.com/${REPOSITORY}:${IMAGE_NAME}
```

Run all cells

