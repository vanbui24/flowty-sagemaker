## Flowty Image

### Overview

This example creates a custom image in Amazon SageMaker Studio using [Poetry](https://python-poetry.org/) to manage the Python dependencies.

### In the AWS Console
 - create SageMaker Studio using Quick Start
 - attach an IAM Role with s3 read & write access 


### Using the AWS CLI
### Creating the ECR repository
Create the ECR repository.
```
# Modify these as required. The Docker registry endpoint can be tuned based on your current region from https://docs.aws.amazon.com/general/latest/gr/ecr.html#ecr-docker-endpoints
# Image_Name must be unique to your account.

REGION=<aws-region>
ACCOUNT_ID=<account-id>
REPOSITORY_NAME=<repository>
IMAGE_NAME=<image-name>

aws --region ${REGION} ecr create-repository \
    --repository-name ${REPOSITORY_NAME}
```
If successful, output repository details

### Building the image
Build the Docker image and push to Amazon ECR.
```
aws --region ${REGION} ecr get-login-password | docker login --username AWS --password-stdin ${ACCOUNT_ID}.dkr.ecr.${REGION}.amazonaws.com/${REPOSITORY_NAME}

docker build . -t ${IMAGE_NAME} -t ${ACCOUNT_ID}.dkr.ecr.${REGION}.amazonaws.com/${REPOSITORY_NAME}:${IMAGE_NAME}
```
If successful, output: Login Succeeded


### Push the image
```
docker push ${ACCOUNT_ID}.dkr.ecr.${REGION}.amazonaws.com/${REPOSITORY_NAME}:${IMAGE_NAME}
```

### Using it with SageMaker Studio
Create a SageMaker Image with the image in ECR. 
```
# IAM Arn role in your account to be used for the SageMaker Image
ROLE_ARN=<role-arn>

aws --region ${REGION} sagemaker create-image \
    --image-name ${IMAGE_NAME} \ 
    --role-arn ${ROLE_ARN}

aws --region ${REGION} sagemaker create-image-version \
    --image-name ${IMAGE_NAME} \
    --base-image "${ACCOUNT_ID}.dkr.ecr.${REGION}.amazonaws.com/${REPOSITORY_NAME}:${IMAGE_NAME}"

# Verify the image-version is created successfully. Do NOT proceed if image-version is in CREATE_FAILED state or in any other state apart from CREATED.
aws --region ${REGION} sagemaker describe-image-version --image-name ${IMAGE_NAME}
```
If successful, output: "ImageArn" 

If successful, output: "ImageVersionArn"

### Create an AppImageConfig for this image.

AppImageConfigName must be unique to your account.

```
aws --region ${REGION} sagemaker create-app-image-config --cli-input-json file://app-image-config-input.json

```

If successful, output: "AppImageConfigArn"

### Update Domain, providing the SageMaker Image and AppImageConfig. 

Replace the placeholder for DomainId.

```
aws --region ${REGION} sagemaker update-domain --cli-input-json file://update-domain-input.json
```
If successful, output: "DomainArn"

### Notes

* Since SageMaker Studio overrides `ENTRYPOINT` and `CMD` instructions (see [documentation](https://docs.aws.amazon.com/sagemaker/latest/dg/studio-byoi-specs.html)), this sample disables the Poetry virtual environments as recommended in their [FAQ](https://python-poetry.org/docs/faq/#i-dont-want-poetry-to-manage-my-virtual-environments-can-i-disable-it). 
* Note that `ipykernel` must be installed on custom images for SageMaker Studio. If this package is not installed by default on the parent image, then it should be included in the `pyproject.toml` file. 