# Gitea2Slack - Bridging Gitea Notifications with Slack

[한국어](./README.KR.md)

## Getting Started

### Step 1: Clone the Project
```bash
git clone <this repository's link>
```

### Step 2: Create a Slack App
Navigate to the [Slack API page](https://api.slack.com/apps) and create a new app. This app will manage the notifications from Gitea to your Slack workspace.

### Step 3: Configure App Permissions
On your app's OAuth & Permissions page, add the following scopes to enable the necessary permissions:

- channels:write.invites: Invite members to public channels
- chat:write: Send messages as @Gitea Notifications
- groups:write: Manage private channels that Gitea Notifications has been added to and create new ones
- im:write: Start direct messages with people
- incoming-webhook: Post messages to specific channels in Slack
- users:read: View people in a workspace
- users:read.email: View email addresses of people in a workspace

### Step 4: Set Up Environment Variables
Copy your app's Bot User OAuth Token and paste it into the .env file in your project directory.

### Step 5: Install Dependencies and Run the Server
With the .env file configured, navigate to your project directory and set up the Python environment:

```bash
cd <to_local_project>
python -m venv ./.venv
.\.venv\Scripts\activate
pip install -r requirements.txt
python main.py
```
### Step 6: Configure Gitea Webhook
1. In your Gitea project, go to Settings > Webhooks.
2. Click on Add Webhook > Gitea.
3. For Target URL, enter http://<gitea2slack_ip>:8765/webhook where <gitea2slack_ip> is the IP address or domain of the server running Gitea2Slack.
4. Set the HTTP Method to POST.
5. Choose application/json as the POST Content Type.
6. Under Trigger On, select Custom Events.
7. Check the boxes for Pull Request Assigned and Pull Request Reviewed to specify which events should trigger notifications.

Now, your setup is complete! Gitea2Slack will forward notifications for the specified events from your Gitea repository directly to your Slack workspace, keeping your team informed and engaged.
