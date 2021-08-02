# Discord Cartel Bot

Cartel is a bot written in Python for the server CartelPvP

## Installation

Use the package manager [pip](https://pip.pypa.io/en/stable/) to install the requirements.

```bash
py -3 -m pip install -U discord.py
```

Install asyncio
```bash
pip install asyncio
```

Install python-dotenv
```bash
pip install python-dotenv
```

Install requests
```bash
python -m pip install requests
```

Install psutil
```bash
pip install psutil
```

## config.json (example)

```json
{
  "server_details": [
    {
      "announcements_id": "860117203683770399",
      "ticket_logs_id": "859442000255123476",
      "ticket_category_id": "859442055867793438",
      "ticket_channel_id": "859486071871111189",
      "verified_role_id": "859724691643039774",
      "configured_ip": "IP_configured",
      "welcome_channel_id": "867422970791985183",
      "logging_channel": "865541976950833172",
      "admins": [
        574958028651233281,
        373556761015353354,
        426902176661635082
      ]
    }
  ]
}
```

## blacklist.json (example)


```json
[
"badword1",
"badword2
]
