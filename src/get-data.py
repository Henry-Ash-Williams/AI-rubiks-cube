# Scrape reconstructions from reco.nz
# checks for 3x3 category, and for a correct solution

import json
import os
import re

from utils import MoveSequence, Reconstruction
import requests
from bs4 import BeautifulSoup
from random_user_agent.user_agent import UserAgent
from random_user_agent.params import SoftwareName, OperatingSystem
from rich.console import Console
from rich.progress import (
    Progress,
    SpinnerColumn,
    TextColumn,
    TimeElapsedColumn,
    TimeRemainingColumn,
    TaskProgressColumn,
    BarColumn,
    MofNCompleteColumn,
)


URL = "https://reco.nz/solve/{}"
END_ID = 12113
START_ID = 3


def scrape(id: int):
    current_url = URL.format(id)
    res = requests.get(
        current_url, headers={"User-Agent": ua_rotator.get_random_user_agent()}
    )
    soup = BeautifulSoup(res.content, features="html.parser")
    title = soup.find("h1").text

    if "3x3" not in title:
        raise Exception("Reconstruction is not a 3x3 solve")

    reconstruction = soup.find(id="reconstruction").text
    lines = [
        line.lstrip() for line in reconstruction.splitlines() if len(line.lstrip()) > 0
    ]
    scramble = lines[0]
    solve = "".join([re.sub(r"//.+", "", line) for line in lines[1:]])

    solve = MoveSequence(solve)
    scramble = MoveSequence(scramble)
    reconstruction = Reconstruction(current_url, scramble, solve)

    if not reconstruction.is_valid():
        raise Exception("Solution does not produce a solved cube")

    return reconstruction


if __name__ == "__main__":
    console = Console()
    ua_rotator = UserAgent(
        software_names=[SoftwareName.CHROME.value, SoftwareName.FIREFOX.value],
        operating_systems=[
            OperatingSystem.WINDOWS.value,
            OperatingSystem.LINUX.value,
            OperatingSystem.MACOS.value,
        ],
        limit=1000,
    )

    reconstructions = []
    urls = []
    if os.path.exists("solves.json"):
        with open("solves.json", "r") as f:
            curr_solves = json.load(f)
        urls = [solve["url"] for solve in curr_solves]
        reconstructions.extend(curr_solves)

    with Progress(
        SpinnerColumn(),
        TextColumn("[progress.description]{task.description}"),
        BarColumn(),
        TaskProgressColumn(),
        MofNCompleteColumn(),
        TimeElapsedColumn(),
        TextColumn("/"),
        TimeRemainingColumn(),
        console=console,
        expand=True,
    ) as p:
        task = p.add_task("Downloading", total=END_ID, completed=START_ID)
        try:
            for id in range(START_ID, END_ID):
                p.advance(task)
                if URL.format(id) in urls:
                    console.log(f"Already processed item: {id}, skipping...")
                    continue
                try:
                    r = scrape(id)
                    reconstructions.append(r)
                except Exception as e:
                    console.log(f"Error processing item {id}: {e}")
        except Exception as e:
            console.log(f"Error in main loop: {e}")
        finally:
            console.log("Saving data")
            with open("solves.json", "w") as file:
                json.dump(
                    [
                        r.to_dict() if isinstance(r, Reconstruction) else r
                        for r in reconstructions
                    ],
                    file,
                )
