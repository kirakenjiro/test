import requests
from github import Github
import logging
import os

def main():
    # Declares tokens, keys and chart symbols for percentages.
    # ? gitKey = Github personal access token.
    # ? wakatimeAPI = Wakatime API key.
    # ? chart = The chart symbols used for the LaTex chart.
    # ? format = The format for the logging.

    githubPATKey = os.environ['PAT_KEY']
    wakatimeAPI = "https://wakatime.com/api/v1/users/current/stats/all_time?api_key={}".format(os.environ['WAKATIME_API_KEY'])

    # ! This will expire every year from Jan 1st 2024 and will need resetting.
    # Casts the Github PAT key to a Github object.
    gitPATKey = Github(githubPATKey)

    # Set the chart symbols for the LaTeX chart.
    chart = "▅▅▅▅▅▅▅▅▅▅"

    # Set the logging format and level.
    format = '%(asctime)s - %(levelname)s > %(message)s'
    logging.basicConfig(format=format, level=logging.INFO)

    # Log data to stdout, this is for debugging purposes.
    log = "Requesting Json from wakatime API."
    logging.info(log)

    # Request wakatime API and collect json data from 'WAKATIME_API_KEY'.
    try:
        result = requests.get(wakatimeAPI)
        if result.status_code == 200:
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

    # Collect json data from 'WAKATIME_API_KEY'
    jsonData = requests.get(wakatimeAPI).json()

    # Returns a list of LaTeX languages.
    if "data" in jsonData:
        LaTeX = []
        for i in jsonData["data"]["languages"]: # ? Change the second key to they key you would like to request instead of the default.
            # Round the percentage to the nearest integer if the rounded percentage is more than 5% or it will ignore the element.
            if round(i['percent']) >= 5:

                # Log data to stdout, this is for debugging purposes.
                log = "Language: {} Time: {} Percentage: {} Rounded Percentage: {}".format(i['name'], i['text'], i['percent'], round(i['percent']))
                logging.info(log)

                # Rounds the percentage to the nearest integer.
                rounded_percentage = round(i['percent'])

                # Replace a certain number of characters in the chart string based on the rounded percentage.
                chart_replaced = chart.replace('▅', '▆', int(len(chart) * rounded_percentage / 100))

                # Split the modified chart string into a list of filled symbols.
                # ? chart_split_filled = Symbols for an filled bar or one that has data.
                chart_split_filled = chart_replaced.split("▅")

                # Split the modified chart string into a list of empty symbols.
                # ? chart_split_empty = Symbols for an empty bar or one that has no data.
                chart_split_empty = chart_replaced.split("▆")

                # Create a LaTeX chart to add to the git readme.
                # ! LaTeX has weird syntax and can get messy so keep it clean.
                LaTeX.append(f"{i['name']}: <br>")
                LaTeX.append(f"$\color{{purple}}{{{''.join(chart_split_filled[0])}}}\color{{gray}}{{{''.join(chart_split_empty[-1])}}}$ {rounded_percentage}% - {i['text']}<br>")

        # Join the LaTeX list into a single string.
        LaTeX = "\n".join(LaTeX)

        # Get the repository object for the specified repository.
        repo = gitPATKey.get_repo("kirakenjiro/kirakenjiro")

        # Get the contents of the readme.md file in the main branch.
        readme = repo.get_contents("readme.md", ref="main")

        # Decode the contents of the readme.md file.
        readme = readme.decoded_content.decode("utf-8")

        # Split the readme.md file into a header, stats and footer by the <!-- Stats --> separator.
        header, _, footer = readme.partition("<!-- Stats -->")

        # Split the footer into a stats and footer by the <!-- Stats --> separator.
        footer = footer.split("<!-- Stats -->", maxsplit=1)[-1]

        # Create the new readme.md file with the header, stats and footer.
        new_readme = f"{header}<!-- Stats -->\n{LaTeX}\n<!-- Stats -->{footer}"

        # Log repo update message to stdout, this is for debugging purposes.
        log = "Updating {} with new stats.".format(repo.full_name)
        logging.info(log)

        # Set readme to an object of the readme.md file as it can't handle a string.
        readme = repo.get_contents("readme.md")

        # Updates the stats while listening for errors.
        try:
            result = repo.update_file(
                # Update the readme.md file with new stats.
                # ? The parameters passed to update_file are as follows:
                # ? contents.path: the path of the file to update.
                # ? "[📊] - Updated code stats": the commit message.
                # ? readme: the new readme.md file.
                # ? contents.sha: the old SHA of the file.
                # ? "main": the branch to commit the changes to.
                readme.path, "[📊] - Updated code stats", new_readme, readme.sha, branch="main")
            if 'commit' in result:
                commit = result['commit']
                if commit.sha:
                    log = "Passed: Updated {} with new stats! commit SHA: {}".format(repo.full_name, commit.sha)
                    logging.info(log)
                else:
                    log = "Failed: {} has failed to update with new stats! commit SHA: {}".format(repo.full_name, commit.sha)
                    raise Exception(log)
            else:
                log = "Failed: An unknown error occurred while {} was updating! commit SHA: {}".format(repo.full_name, commit.sha)
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
