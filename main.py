import requests
from flask import Flask, request, jsonify
from dotenv import load_dotenv
import os

load_dotenv()

app = Flask(__name__)

SLACK_TOKEN = os.environ.get("SLACK_TOKEN")


@app.route("/webhook", methods=["POST"])
def handle_webhook():
    data = request.json

    if data["action"] == "assigned":
        email = data["pull_request"]["assignee"]["email"]
        pr_link = data["pull_request"]["url"]
        sender = data["sender"]["login"]
        pr_of = data["pull_request"]["user"]["login"]
        pr_title = data["pull_request"]["title"]
        pr_number = data["pull_request"]["number"]
        # pr_body = data["pull_request"]["body"] # Slack uses "mrkdwn" format is Incompatible with Markdown.
        slack_user_id = find_slack_user_by_email(email)
        message = f"{sender}님께서 \n{pr_of}님의 PR 리뷰요청: <{pr_link}|{pr_number}-{pr_title}>"
        if slack_user_id:
            channel_id = open_conversation(slack_user_id)
            if channel_id:
                send_slack_message(channel_id, message)
                return jsonify({"message": "Notification sent to Slack!"}), 200
            else:
                return jsonify({"error": "Failed to open conversation"}), 500
        else:
            return jsonify({"error": "Slack user not found"}), 404
    elif data["action"] == "reviewed":
        email = data["pull_request"]["user"]["email"]
        reviewer = data["sender"]["login"]
        review_type = data["review"]["type"]
        review_content = data["review"]["content"]
        slack_user_id = find_slack_user_by_email(email)
        message = f"리뷰한 사람: {reviewer} \n리뷰 타입: {review_type} \n리뷰 내용: {review_content}"
        if slack_user_id:
            channel_id = open_conversation(slack_user_id)
            if channel_id:
                send_slack_message(channel_id, message)
                return jsonify({"message": "Notification sent to Slack!"}), 200
            else:
                return jsonify({"error": "Failed to open conversation"}), 500
        else:
            return jsonify({"error": "Slack user not found"}), 404
    elif data["action"] == "unassigned":
        return jsonify({"message": "Unassigned. No message sent to Slack"}), 200


def find_slack_user_by_email(email):
    headers = {"Authorization": f"Bearer {SLACK_TOKEN}"}
    response = requests.get(
        "https://slack.com/api/users.lookupByEmail",
        headers=headers,
        params={"email": email},
    )
    if response.status_code == 200 and response.json()["ok"]:
        return response.json()["user"]["id"]
    return None


def open_conversation(user_id):
    headers = {
        "Authorization": f"Bearer {SLACK_TOKEN}",
        "Content-Type": "application/json",
    }
    payload = {"users": user_id}
    response = requests.post(
        "https://slack.com/api/conversations.open", headers=headers, json=payload
    )
    if response.status_code == 200 and response.json()["ok"]:
        return response.json()["channel"]["id"]
    else:
        print(f"Error opening conversation: {response.json()}")
        return None


def send_slack_message(channel_id, message):
    headers = {
        "Authorization": f"Bearer {SLACK_TOKEN}",
        "Content-Type": "application/json",
    }
    payload = {"channel": channel_id, "text": message}
    response = requests.post(
        "https://slack.com/api/chat.postMessage", headers=headers, json=payload
    )
    print(f"send_slack_message() response: {response.json()}")
    return response.json()


if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=8765)
