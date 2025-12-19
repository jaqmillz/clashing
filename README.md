# Clash Royale Stats Tracker 🔥

Track your Clash Royale stats and get ROASTED based on your performance!

## Features

- 📊 **Real-time Stats** - Fetch live player data from Clash Royale API
- 🔥 **Performance Roasting** - Get brutally honest feedback on your gameplay
- 📈 **Historical Tracking** - Store stats in Parquet files for trend analysis
- ⚡ **7-Day Trends** - See how you've been performing this week
- 💀 **Skill Ratings** - From "Straight Trash" to "Absolute Legend"

## Setup

1. Get your API key from https://developer.clashroyale.com/

2. Create `.env` file:
```bash
cp .env.example .env
# Edit .env and add your API key
```

3. Install dependencies:
```bash
just install
```

4. Run the app:
```bash
just run
```

Then open http://localhost:3000

## Usage

Enter any player tag (with or without #) to:
- See current stats
- Get roasted based on performance
- Track historical trends
- View win rates and trophy changes

## Roasting Examples

- Lost trophies? "Maybe try a different game? 💀"
- Low win rate? "Even a coin flip would do better! 🪙"
- No three crowns? "Are you trying to win or just participating? 🎖️"

## Data Storage

Stats are automatically saved to `data/player_stats.parquet` for historical analysis using Pandas and PyArrow.

## Commands

```bash
just run          # Start server
just stop         # Stop server
just install      # Install deps
just clean-data   # Delete stats
```
