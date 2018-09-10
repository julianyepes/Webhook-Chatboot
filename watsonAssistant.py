import watson_developer_cloud

# Set up watson Assistant service.
service = watson_developer_cloud.AssistantV1(
        username = 'c3ddb0d8-f39a-4fab-842d-1d4967bdf38e', # replace with service username
        password = 'OhYBxhczAKfn', # replace with service password
        version = '2018-02-16'
)
workspace_id = '8dbb4a73-acee-4ae2-a1fc-c3d4421debd9' # replace with workspace ID

def callWatsonAssistantAPI(user_input, context):

        # Send message to Assistant service.
        return service.message(
                workspace_id = workspace_id,
                input = {
                        'text': user_input
                },
                context = context
        )
        # Print the output from dialog, if any.
        #if response['output']['text']:vcap@0f5e92f5-5000-418e-41a1-7270:~/app$ cat watsonAssistent.py
