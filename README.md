# 2020adsp_team_2

## About

This project is used in a class in my university. We regularly observe the quantity of UV by sunlight using a spectrometer attached with a Raspberry Pi and this project

- analyzes the result

- and posts it to Twitter.

We use [@2020adsp_team_2](https://twitter.com/2020adsp_team_2) as our Twitter account but of course you can use your own account.

## Requirements

- [`python-twitter` library](https://github.com/bear/python-twitter)

- An account for [Twitter Developer](https://developer.twitter.com/en) (see [Preparations](#preparations))

## Files

- `./twitter_local.py`

This script accesses Twitter API.

## Preparations

### `./twitter_local.py`

1. Credentials

    1. Create an account for [Twitter Developer](https://developer.twitter.com/en).

    2. Get API keys from the developer center.

    3. Create a file `twitter_credentials.json` in this project directory. It shall be of the form

    ```
    {
        "api_key":             "<api key>",
        "api_secret_key":      "<api secret key>",
        "access_token":        "<access token>",
        "access_token_secret": "<access token secret>"
    }
    ```

2. Parameters

    1. Change the contents of `./config.json` as you like. This file specifies, for example, the name of the file in which your Twitter credentials are written.

## Usage

### `twitter_local.py`

```bash
$ ./twitter_local.py <tweet content>
```

<!-- vim: set spell: -->

