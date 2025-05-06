# AI Customer Assistant — Serverless Chatbot Built with Bedrock, Lambda, and Terraform on AWS


![IaC](https://img.shields.io/badge/IaC-Terraform-7B42BC?style=for-the-badge&logo=terraform)
![Cloud](https://img.shields.io/badge/Cloud-AWS-232F3E?style=for-the-badge&logo=amazonaws)
![AWS Lambda](https://img.shields.io/badge/AWS%20Lambda-Serverless-F58536?style=for-the-badge&logo=awslambda)
![Amazon Bedrock](https://img.shields.io/badge/Amazon%20Bedrock-Titan%20Text%20G1-1A6FFF?style=for-the-badge&logo=amazonaws)
![AWS Amplify](https://img.shields.io/badge/AWS%20Amplify-Frontend-FF9900?style=for-the-badge&logo=awsamplify)
![AWS DynamoDB](https://img.shields.io/badge/AWS%20DynamoDB-Session%20Log-4053D6?style=for-the-badge&logo=amazonaws)
![API Gateway](https://img.shields.io/badge/API%20Gateway-HTTP%20API-DD3464?style=for-the-badge&logo=amazonaws)
![Serverless Architecture](https://img.shields.io/badge/Architecture-Serverless-4B5563?style=for-the-badge)

This is a fully serverless AI chatbot built with Amazon Bedrock (Titan G1), Lambda, and Terraform, designed to answer customer questions in real time based on a curated FAQ prompt. The frontend is deployed using AWS Amplify with a custom Route 53 domain, and all interactions are logged in DynamoDB for session tracking.

---

## Demo

**Watch the full demo on YouTube**  


[Watch the YouTube demo](https://www.youtube.com/watch?v=VCxfDRWnaK0)

---

## Architecture

![Architecture](./screenshots/ai-customer-bot.png)

---

**Live Chatbot UI:**  
![Chatbot UI](./screenshots/Webpage.png)

**Chat Example:**  
![Chatbot Response](./screenshots/Webpage-prompt.png)

**Transcript Feature:**  
![Transcript Output](./screenshots/Download-Transcripts.png)
> *Note: The service is turned off to reduce AWS costs. All infrastructure can be redeployed using this repo.*


---
## How It Works

1. **User** types a question into the Amplify-hosted chatbot UI.
2. The frontend sends a `POST /chat` request via **API Gateway**.
   ![Postman Test](./screenshots/postman.png)
3. API Gateway invokes a **Lambda function**.
4. Lambda injects the user input into a pre-defined **FAQ prompt**.
5. The prompt is sent to **Amazon Bedrock (Titan G1)** and a response is returned.
   ![Lambda Output 1](./screenshots/7-lambda-test-success.png)
6. Lambda returns the message and logs it into **DynamoDB**.
   ![DynamoDB Log](./screenshots/9-dynamodb-chat-history.png)  
7. Session logs are viewable via DynamoDB and CloudWatch.
   ![CloudWatch Log](./screenshots/9-Cloudwatch-logs.png)

---

## Deployment with Terraform

Clone and deploy:

```bash
git clone https://github.com/yourusername/ai-customer-bot.git
cd terraform
terraform init
terraform apply
```

You will deploy:
- ✅ IAM roles & policies  
  ![IAM Terraform](./screenshots/3-terraform-iam.png)
- ✅ Lambda function  
  ![Lambda Terraform](./screenshots/4-terraform-lambda.png)
- ✅ API Gateway  
  ![API Gateway Terraform](./screenshots/13-terraform-api-gateway.png)
- ✅ DynamoDB table  
  ![DynamoDB Terraform](./screenshots/8-terraform-dynamodb.png)
- ✅ Route 53 + Amplify (custom domain setup via AWS Console)  
  The frontend was deployed using Amplify and connected to GitHub for CI/CD. A custom subdomain (`chatbot.fkvventures.com`) was added using Route 53.  
  SSL is managed by Amplify with AWS-managed ACM certificates.  
  Some parts of the setup — like domain connection and certificate validation — were done manually through the AWS Console due to Terraform limitations with Amplify and Route 53.  
  [Official AWS setup guide](https://docs.aws.amazon.com/amplify/latest/userguide/custom-domains.html)  
  ![Route 53 + Amplify](./screenshots/amplify-route53.png)


---

## Services Used

| Layer       | Service                         |
|-------------|----------------------------------|
| Frontend    | AWS Amplify + Route 53           |
| API         | Amazon API Gateway (HTTP)        |
| Compute     | AWS Lambda                       |
| AI Model    | Amazon Bedrock – Titan Text G1   |
| Database    | DynamoDB (chat session log)      |
| Monitoring  | CloudWatch (Lambda auto-logs)    |
| Infra-as-Code | Terraform (backend only)       |

---

## DynamoDB Table

**Table Name:** `chat_history`  
**Partition Key:** `session_id` (String)

---

## 🔧 Future Enhancements

- Swap Titan with Claude (also via Bedrock)
- Load FAQ data dynamically from S3

---

## Connect with Me

📫 [LinkedIn](https://www.linkedin.com/in/franc-kevin-v-07108b111/)