# 🚀 **LaunchTokens - Token Extractor Bot**

## 📌 **Overview**
LaunchTokens is a bot designed to extract tokens from various platforms. It automatically scrapes and collects information about launched tokens, bypassing common bot detection and anti-scraping measures.

## 🛠 **Features**
- **Automated Token Extraction**: Automatically runs all the scripts to extract launched tokens.
- **Bypassing Detection**: Uses rotating proxies, Firefox Genome browser, and dynamic user agents to avoid bot detection and Cloudflare challenges.
- **Cloudflare Tunnel**: Implemented bypass techniques to handle Cloudflare's anti-bot measures effectively.

## ⚙️ **Scripts Included**
Each script is designed to extract tokens from different sources:

- 🏦 **cntokens.py**: Extracts tokens from CoinToken platform.
- 📈 **coinalpha.py**: Scrapes CoinAlpha for new launches.
- 🌙 **coinmooner.py**: Collects tokens from CoinMooner.
- 🧑‍💻 **coinscope.py**: Extracts data from CoinScope.
- 🌐 **coinsgod.py**: Fetches tokens from CoinGod.
- 🎯 **coinsniper.py**: Gathers tokens from CoinSniper.
- 🗳 **coinvotecc.py**: Extracts vote data from CoinVoteCC.
- 💡 **freshcoins.py**: Scrapes FreshCoins for newly launched tokens.
- 💎 **gemfind.py**: Extracts data from GemFind.
- 🪙 **moontok.py**: Fetches new token data from MoonTok.
- ✍️ **writexlsx.py**: Writes the extracted data into an Excel file.
- 🧪 **test.py**: Utility for testing and debugging.

## 🚀 **Main Execution**
- The `main.py` script automatically runs all of the above scripts in sequence, performing token extraction from different sources.

## 🔧 **Techniques Used**
To bypass common scraping restrictions, several advanced techniques are implemented:

- **Rotating Proxies**: Ensures requests come from different IP addresses, avoiding detection.
- **Firefox Genome Browser**: Uses Firefox instead of Chromium to mimic human-like behavior and avoid bot detection systems.
- **Dynamic User Agent**: Changes the user agent string to prevent detection by anti-scraping mechanisms.

## 📝 **Problems Faced**
- **Bot Detection**: Overcome using rotating proxies and non-Chromium browsers.
- **Cloudflare Challenges**: Bypassed using the Cloudflare Tunnel and advanced techniques.

## 📂 **File Structure**
```plaintext
launchtokens/
├── cntokens.py
├── coinalpha.py
├── coinmooner.py
├── coinscope.py
├── coinsgod.py
├── coinsniper.py
├── coinvotecc.py
├── freshcoins.py
├── gemfind.py
├── moontok.py
├── writexlsx.py
├── test.py
├── main.py
└── cryptotokens.xlsx
