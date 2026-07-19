import requests
import urllib

postcode = input("Enter a valid UK postcode (e.g. SW1A 1AA): ")

postcodeSearch = requests.get(f"https://api.postcodes.io/postcodes/{postcode}")
fullPostcodeData = postcodeSearch.json()
postcodeData = fullPostcodeData.get("result", {})

if postcodeSearch.status_code == 200:
    constituencyName = postcodeData.get("parliamentary_constituency")
    if constituencyName == "null":
        constituencyName = postcodeData.get("senedd_constituency")
    # TODO: Add friendly error for entering a Channel Islands or Isle of Man postcode

    print(f"Your constituency is: {constituencyName}")

    encodedConstituency = urllib.parse.quote(constituencyName)

    constituencySearch = requests.get(f"https://members-api.parliament.uk/api/Location/Constituency/Search?searchText={encodedConstituency}&skip=0&take=20")
    fullConstituencyData = constituencySearch.json()
    constituencyItems = fullConstituencyData.get("items", [])

    if constituencyItems:
        constituencyValue = constituencyItems[0].get("value", {})
        currentRepresentation = constituencyValue.get("currentRepresentation", {})
        memberValue = currentRepresentation.get("member", {}).get("value", {})
        partyValue = memberValue.get("latestParty", {})
        mpName = memberValue.get("nameFullTitle")
        memberParty = partyValue.get("name")
    else:
        mpName = "MP name wasn't found."

    print(f"Your MP's name is {mpName}.")
    print(f"Their party is {memberParty}.")


elif postcodeSearch.status_code == 404:
    print(f"Something went wrong. The Postcodes API returned a 404 error, meaning the postcode wasn't found/wasn't valid. Check you didn't misspell it.")

else:
    print(f"Something went wrong. Response code: {postcodeSearch.status_code}.")



