from discord import SyncWebhook
import os

githubPATKey = os.environ['PAT_KEY']
wakatimeAPI = "https://wakatime.com/api/v1/users/current/stats/all_time?api_key={}".format(os.environ['WAKATIME_API_KEY'])

print(githubPATKey)
print(wakatimeAPI)
