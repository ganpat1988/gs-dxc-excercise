import json
import cfnresponse
import boto3

ssm_client = boto3.client('ssm', region_name='us-east-1')
s3_client = boto3.client('s3')
bucket = 'dx-excercise'
key = 'files'

def handler(event, context):
    print('EVENT', event)

    responseData = {},

    username_param = ssm_client.get_parameter(Name='dx-exercise-username')['Parameter']['Value']
    filename_param = ssm_client.get_parameter(Name='dx-exercise-username')['Parameter']['Name']
    file_key = 'files/'+filename_param+'.txt'

    SUCCESS = "SUCCESS"
    FAILED = "FAILED"

    try:
        if event['RequestType'] == 'Create' or event['RequestType'] == 'Update':
            print('creating resource')
            s3_client.put_object(
                Body=str(username_param),
                Bucket=bucket,
                Key=file_key
            )

        elif event['RequestType'] == 'Delete':
            print('deleting resource')
            s3_client.delete_object(Bucket=bucket, Key=file_key)

            responseData['Data'] = 'responseValue'
            send(event, context, cfnresponse.SUCCESS, responseData)
    except:
        print('error in lambda function')
        send(event, context, cfnresponse.FAILED, responseData)


def send(event, context, responseStatus, responseData, physicalResourceId=None, noEcho=False, reason=None):
    responseUrl = event['ResponseURL']

    print(responseUrl)

    responseBody = {
        'Status' : responseStatus,
        'Reason' : reason or "See the details in CloudWatch Log Stream: {}".format(context.log_stream_name),
        'PhysicalResourceId' : physicalResourceId or context.log_stream_name,
        'StackId' : event['StackId'],
        'RequestId' : event['RequestId'],
        'LogicalResourceId' : event['LogicalResourceId'],
        'NoEcho' : noEcho,
        'Data' : responseData
    }

    json_responseBody = json.dumps(responseBody)
    print("Response body:")
    print(json_responseBody)

    headers = {
        'content-type' : '',
        'content-length' : str(len(json_responseBody))
    }

    try:
        response = http.request('PUT', responseUrl, headers=headers, body=json_responseBody)
        print("Status code:", response.status)
    except Exception as e:
        print("send(..) failed executing http.request(..):", e)
