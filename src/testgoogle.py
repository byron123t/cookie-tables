from time import sleep
from googleapiclient.errors import HttpError
from googleapiclient.discovery import build


def main():
    # Build a service object for interacting with the API. Visit
    # the Google APIs Console <http://code.google.com/apis/console>
    # to get an API key for your own application.
    service = build(
        "customsearch", "v1", developerKey="AIzaSyDzreUmljOTVjpUHpSpxumLsaPrPMCS80U"
    )

    skip = 18511
    with open('cookie_tables.txt', 'a') as outfile:
        with open ('data/cookie_table/top-1m.csv', 'r') as infile:
            count = 0
            for line in infile:
                if count >= skip:
                    error = True
                    while error:
                        try:
                            res = (
                                service.cse()
                                .list(
                                    q="privacy \"cookie table\" OR \"cookie list\" site:{}".format(line.strip()),
                                    cx="8791a697bdaa745e1",
                                )
                                .execute()
                            )
                            error = False
                        except HttpError as e:
                            sleep(5)
                    links = []
                    if 'items' in res:
                        maximum = max(len(res['items']), 3)
                        for item in res['items'][:3]:
                            print(item['link'], count)
                            links.append(item['link'])
                    outfile.write(str(links)+'\n')
                count += 1


if __name__ == "__main__":
    main()