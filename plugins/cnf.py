
import requests
from bs4 import BeautifulSoup

from Archx import Archx, Message


@Archx.on_cmd(
    "cnf",
    about={
        "header": "Install any command on any operating system.",
        "usage": "{tr}cnf\n{tr}cnf [command ]",
        "examples": "{tr}cnf python",
    },
)
async def cnf(message: Message):

    await message.edit("`Searching...`")
    base_url = "https://command-not-found.com/"

    if not message.input_str:
        # find a random command
        page = requests.get(base_url)
        soup = BeautifulSoup(page.content, "lxml", from_encoding="utf-8")
        cmd = soup.find(
            "a", attrs={"class": "h5 brand-text d-block mb-1 other-command"}
        ).text.strip()
    else:
        cmd = message.input_str.split()[0]

    try:
        page = requests.get(base_url + cmd)
        soup = BeautifulSoup(page.content, "lxml", from_encoding="utf-8")

        # heading
        payload = f"**[{cmd}]({base_url + cmd})**\n"
        # description
        payload += f"{soup.find('p', attrs = {'class':'my-0'}).text.strip()}\n\n"

        lst = soup.findAll("div", attrs={"class": "command-install"})

        # items
        for row in lst:
            try:
                row["class"][2] == "d-none"
                # ignore this its stil not implemented by Łukasz
                continue
            except IndexError:
                pass
            os = row.dt.findAll(text=True, recursive=False)[-1].strip()
            command = row.dd.code.text

            payload += f"{os}\n`{command}`\n\n"

        await message.edit(payload, disable_web_page_preview=False)
    except IndexError:
        await message.edit("Command Not Found")
    except Exception as err:
        await message.err(err)
