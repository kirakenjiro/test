import requests
from github import Github
import logging
import os

def main():
    # Get the Github PAT and Wakatime API key from the environment variables.
    # Encode the wakatime API key using base64.
    # ? GIT_PAT_KEY = Github personal access token.
    # ? WAKATIME_API_KEY = Wakatime API key.
    # ? wakatimeAPIKey64 = Wakatime API key encoded in base64.
    # ? wakatimeAPI = Wakatime API URL.
    githubPATKey = os.environ['GIT_PAT_KEY']
    wakatimeAPIKey = os.environ['WAKATIME_API_KEY']
    wakatimeAPIKey64 = base64.b64encode(wakatimeAPIKey.encode()).decode()

    # ! This will expire every year from Jan 1st 2024 and will need resetting.
    # Casts the githubPATKey to a Github object.
    gitPATKey = Github(githubPATKey)

    # Define the API endpoint
    wakatimeAPI = "https://wakatime.com/api/v1/users/current/stats/last_7_days"

    # Set the chart symbols for the LaTeX chart.
    chart = "▅▅▅▅▅▅▅▅▅▅"

    # Set the logging format and level.
    format = '%(asctime)s - %(levelname)s > %(message)s'
    logging.basicConfig(format=format, level=logging.INFO)

    # Log data to stdout, this is for debugging purposes.
    log = "Requesting Json from wakatime API."
    logging.info(log)

    # Request wakatimeAPI and collect json from 'jsonData'.
    try:
        result = requests.get(wakatimeAPI)
        if result.status_code == 200:
            jsonData = requests.get(wakatimeAPI).json()
            log = "Passed: Json was collected from the API."
            logging.info(log)
        elif result.status_code == 401:
            log = "Failed: The API key is invalid. Please check the API key."
            raise Exception(log)
        elif result.status_code == 404:
            log = "Failed: The API was not found. Please check the URL."
            raise Exception(log)
        elif result.status_code == 500:
            log = "Failed: The API is currently down."
            raise Exception(log)
        else:
            log = "Failed: An unknown error has occurred while requesting the API."
            raise Exception(log)
    except Exception as error:
        logging.error(error)

    # Check if the json data contains the key "data".
    # ? To check for a different key, change the second key to the key you would like to check.
    # ? This will check if the json data contains the key "languages" and iterate though each language in the data.
    if "data" in jsonData:
        LaTeX = []
        for i in jsonData["data"]["languages"]: # ? Change the second key to they key you would like to request instead of the default.
            # Round the percentage to the nearest integer if the rounded percentage is more than 5% or it will ignore the element.
            if round(i['percent']) >= 5:

                # Log data to stdout, this is for debugging purposes.
                log = "Language: {} Time: {} Percentage: {} Rounded Percentage: {}".format(i['name'], i['text'], i['percent'], round(i['percent']))
                logging.info(log)

                # Rounds the percentage to the nearest integer.
                roundedPercentage = round(i['percent'])

                # Replace a certain number of characters in the chart string based on the rounded percentage.
                chartReplaced = chart.replace('▅', '▆', int(len(chart) * roundedPercentage / 100))

                # Split the modified chart string into a list of filled symbols.
                # ? chart_split_filled = Symbols for an filled bar or one that has data.
                chartSplitFilled = chartReplaced.split("▅")

                # Split the modified chart string into a list of empty symbols.
                # ? chart_split_empty = Symbols for an empty bar or one that has no data.
                chartSplitEmpty = chartReplaced.split("▆")

                # Create a LaTeX chart to add to the git readme.
                # ! LaTeX has weird syntax and can get messy so keep it clean.
                LaTeX.append(f"{i['name']}: <br>")
                LaTeX.append(f"$\color{{purple}}{{{''.join(chartSplitFilled[0])}}}\color{{gray}}{{{''.join(chartSplitEmpty[-1])}}}$ {roundedPercentage}% - {i['text']}<br>")

        # Join the LaTeX list into a single string.
        LaTeX = "\n".join(LaTeX)

        # Get the repository object for the specified repository.
        repo = githubPATKey.get_repo("kirakenjiro/kirakenjiro")

        # Get the contents of the readme.md file in the main branch.
        readme = repo.get_contents("readme.md", ref="main")

        # Decode the contents of the readme.md file.
        readme = readme.decoded_content.decode("utf-8")

        # Split the readme.md file into a header, stats and footer by the <!-- Stats --> separator.
        header, _, footer = readme.partition("<!-- Stats -->")

        # Split the footer into a stats and footer by the <!-- Stats --> separator.
        footer = footer.split("<!-- Stats -->", maxsplit=1)[-1]

        # Create the updated readme.md file with the header, stats and footer.
        updatedReadme = f"{header}<!-- Stats -->\n{LaTeX}\n<!-- Stats -->{footer}"

        # Log repo update message to stdout, this is for debugging purposes.
        log = "Updating {} with new stats.".format(repo.full_name)
        logging.info(log)

        # Set readme to an object of the readme.md file as it can't handle a string.
        readme = repo.get_contents("readme.md")

        # Update the readme.md file with new stats.
        # ? The parameters passed to update_file are as follows:
        # ? contents.path: The path of the file to update.
        # ? [📊] - Updated code stats: The commit message.
        # ? updatedReadme: The new readme.md file.
        # ? contents.sha: The old SHA of the file.
        # ? main: The branch to commit the changes to.
        try:
            result = repo.update_file(readme.path, "[📊] - Updated code stats", updatedReadme, readme.sha, branch="main")
            if 'commit' in result:
                commit = result['commit']
                if commit.sha:
                    log = "Passed: Updated {} with new stats! commit SHA: {}".format(repo.full_name, commit.sha)
                    logging.info(log)
                else:
                    log = "Failed: {} has failed to update with new stats!".format(repo.full_name)
                    raise Exception(log)
            else:
                log = "Failed: An unknown error occurred while the repo was updating!"
                raise Exception(log)

        except Exception as error:
            logging.error(error)

#  ? Lets be honest, None of us knows what this does, we just use it.
# This is the entry point for the program.
if __name__ == '__main__':
    main()
else:
    print("This script is not meant to be imported.")
    while true:
        try:
            raise Exception()
        except Exception:
            pass # Me every morning.
