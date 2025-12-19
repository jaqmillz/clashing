"""Player performance roaster - talks trash based on stats"""
import random

# Whitelist of phenomenal players who get praise instead of roasts
WHITELIST = [
    '9Q8202Q2G',
    '#9Q8202Q2G',
    '#R908Y0P',
    'R908Y0P',
]

def is_whitelisted(player_tag):
    """Check if player is in the whitelist"""
    # Normalize tag (remove # if present)
    normalized_tag = player_tag.replace('#', '').upper()
    return any(normalized_tag == wl.replace('#', '').upper() for wl in WHITELIST)

def praise_player(player_data, trends):
    """Generate phenomenal praise for whitelisted players"""
    praises = []

    # Basic stats
    exp_level = player_data.get('expLevel', 0)
    trophies = player_data.get('trophies', 0)
    best_trophies = player_data.get('bestTrophies', 0)
    wins = player_data.get('wins', 0)
    losses = player_data.get('losses', 0)
    total_games = wins + losses
    lifetime_win_rate = (wins / total_games * 100) if total_games > 0 else 0

    praises.append(f"🔥 ABSOLUTE LEGEND! {lifetime_win_rate:.1f}% win rate - you're DESTROYING the competition!")
    praises.append(f"⭐ {wins:,} wins?! You're not just playing, you're DOMINATING! The arena trembles at your name!")
    praises.append(f"🏆 {trophies:,} trophies - you're climbing to GODLIKE status!")

    if trends:
        trophy_change = trends.get('trophy_change', 0)
        win_change = trends.get('win_change', 0)
        if trophy_change > 0:
            praises.append(f"📈 +{trophy_change} trophies recently?! UNSTOPPABLE MOMENTUM!")
        if win_change > 0:
            praises.append(f"💪 {win_change} recent wins - you're on FIRE! Keep crushing it!")

    praises.append(f"👑 Level {exp_level} - A TRUE MASTER of Clash Royale!")
    praises.append(f"🎯 This isn't skill anymore, this is ART! Picasso could never!")
    praises.append(f"⚡ Other players study YOUR replays to get better. You're the BLUEPRINT!")

    return praises

def roast_player(player_data, trends):
    """Generate savage, comprehensive roasts based on ALL player data"""
    # Check if player is whitelisted
    player_tag = player_data.get('tag', '')
    if is_whitelisted(player_tag):
        return praise_player(player_data, trends)

    roasts = []

    # Basic stats
    exp_level = player_data.get('expLevel', 0)
    trophies = player_data.get('trophies', 0)
    best_trophies = player_data.get('bestTrophies', 0)
    wins = player_data.get('wins', 0)
    losses = player_data.get('losses', 0)
    three_crown_wins = player_data.get('threeCrownWins', 0)

    # Calculate lifetime win rate
    total_games = wins + losses
    lifetime_win_rate = (wins / total_games * 100) if total_games > 0 else 0

    # LIFETIME PERFORMANCE ROASTS (guaranteed to find flaws)
    if lifetime_win_rate < 45:
        roasts.append(f"LIFETIME {lifetime_win_rate:.1f}% win rate across {total_games:,} games... that's COMMITMENT to mediocrity! 🤡")
    elif lifetime_win_rate < 50:
        roasts.append(f"{lifetime_win_rate:.1f}% lifetime win rate. You're literally worse than a coin flip! 🪙")
    elif lifetime_win_rate < 55:
        roasts.append(f"{lifetime_win_rate:.1f}% win rate after {total_games:,} games. Still haven't figured it out, huh? 📚")
    elif lifetime_win_rate < 60:
        roasts.append(f"{lifetime_win_rate:.1f}% win rate. Okay you're DECENT but that's after {total_games:,} games... 😬")
    else:
        roasts.append(f"{lifetime_win_rate:.1f}% win rate but we KNOW most of those are 2v2s or against noobs 🤖")

    # LOSS TOTAL ROASTS (always savage)
    if losses > 10000:
        roasts.append(f"{losses:,} LOSSES?! That's not a stat, that's a war crime! 💀")
    elif losses > 5000:
        roasts.append(f"{losses:,} losses. You've been taking L's since the Stone Age! 🗿")
    elif losses > 1000:
        roasts.append(f"{losses:,} losses... at least you're consistent! 📉")

    # TROPHY GAP ROASTS (current vs best)
    trophy_gap = best_trophies - trophies
    if trophy_gap > 1000:
        roasts.append(f"DOWN {trophy_gap:,} trophies from your peak?! That's not a fall, that's PLUMMETING! 🪂")
    elif trophy_gap > 500:
        roasts.append(f"{trophy_gap} trophies below your best. Peak performance was clearly a fluke! 📉")
    elif trophy_gap > 200:
        roasts.append(f"{trophy_gap} trophies off your peak. We've seen better days, haven't we? 😔")
    elif trophy_gap == 0:
        roasts.append(f"At your peak trophies? Cool. Still doesn't mean you're good though! 😤")

    # LEVEL VS TROPHIES ROASTS
    if exp_level >= 60 and trophies < 8000:
        roasts.append(f"Level {exp_level} with only {trophies:,} trophies?! YEARS of playing for THIS?! ⏰💀")
    elif exp_level >= 50 and trophies < 7000:
        roasts.append(f"Level {exp_level}... {trophies:,} trophies... the TIME you've wasted! 🤦")
    elif exp_level >= 40 and trophies < 6000:
        roasts.append(f"Level {exp_level} stuck at {trophies:,} trophies. Skill issue is REAL! 📚")
    elif exp_level >= 30 and trophies < 5000:
        roasts.append(f"Level {exp_level} can't break 5000? Delete the app! 🗑️")

    # THREE CROWN EFFICIENCY
    if total_games > 0:
        three_crown_rate = (three_crown_wins / total_games * 100)
        if three_crown_rate < 5:
            roasts.append(f"Only {three_crown_rate:.1f}% three crowns?! Do you even ATTACK?! 😴")
        elif three_crown_rate < 10:
            roasts.append(f"{three_crown_rate:.1f}% three crown rate. Barely trying to win! 🎖️")

    # CLAN ROASTS
    clan = player_data.get('clan', {})
    if clan:
        clan_role = clan.get('role', 'member')
        donations = player_data.get('donations', 0)
        donations_received = player_data.get('donationsReceived', 0)

        if donations < donations_received:
            roasts.append(f"More donations RECEIVED than given?! Classic leech behavior! 🦠")

        if clan_role == 'leader':
            if trophies < 7000:
                roasts.append(f"You're a LEADER with {trophies:,} trophies?! Your clan must be STRUGGLING! 👑💀")
        elif clan_role == 'coLeader':
            if trophies < 6500:
                roasts.append(f"Co-leader with {trophies:,} trophies... carrying the clan to DEFEAT! 📉")

        if donations == 0:
            roasts.append("Zero donations?! At least PRETEND to help your clan! 🤝")
    else:
        roasts.append("Not even in a clan? Solo career going GREAT I see! 😂")

    # CARDS ROASTS
    cards = player_data.get('cards', [])
    if cards:
        total_cards = len(cards)
        max_level_cards = sum(1 for c in cards if c.get('level', 0) >= 14)
        avg_level = sum(c.get('level', 0) for c in cards) / total_cards if total_cards > 0 else 0

        if max_level_cards == 0 and exp_level > 40:
            roasts.append(f"Level {exp_level} with ZERO max level cards?! What are you even doing?! 💸")

        if avg_level < 10 and exp_level > 30:
            roasts.append(f"Average card level {avg_level:.1f}... upgrade something maybe?! 📈")

        # Star levels (cosmetic flex)
        star_cards = sum(1 for c in cards if c.get('starLevel', 0) > 0)
        if star_cards == 0 and exp_level > 45:
            roasts.append("Not a SINGLE star level? Can't even flex cosmetics! ✨")

    # CHALLENGE PERFORMANCE
    challenge_max = player_data.get('challengeMaxWins', 0)
    challenge_cards = player_data.get('challengeCardsWon', 0)

    if challenge_max < 8 and exp_level > 30:
        roasts.append(f"Max {challenge_max} challenge wins?! Can't handle the REAL competition! 🏆")
    elif challenge_max < 12 and exp_level > 40:
        roasts.append(f"Only {challenge_max} max challenge wins. So close to 12 but so far! 🎯")

    if challenge_cards < 5000 and total_games > 5000:
        roasts.append(f"Only {challenge_cards:,} challenge cards won. Scared of challenges? 😨")

    # TOURNAMENT PERFORMANCE
    tournament_cards = player_data.get('tournamentCardsWon', 0)
    tournament_games = player_data.get('tournamentBattleCount', 0)

    if tournament_games > 100 and tournament_cards < 10000:
        roasts.append(f"{tournament_games} tournament games, {tournament_cards:,} cards won... ROUGH! 💀")

    # WAR PERFORMANCE
    war_day_wins = player_data.get('warDayWins', 0)
    clan_cards = player_data.get('clanCardsCollected', 0)

    if war_day_wins < 100 and total_games > 3000:
        roasts.append(f"Only {war_day_wins} war wins?! Not a team player, are we? 🤝")

    if clan_cards > 100000 and trophies < 7000:
        roasts.append(f"{clan_cards:,} clan cards but {trophies:,} trophies?! GRINDING for nothing! 🎡")

    # RECENT TRENDS (if available)
    if trends:
        trophy_change = trends.get('trophy_change', 0)
        win_rate = trends.get('win_rate')
        loss_change = trends.get('loss_change', 0)
        win_change = trends.get('win_change', 0)

        # Recent trophy performance
        if trophy_change < -200:
            roasts.append(f"HEMORRHAGING {abs(trophy_change)} trophies this week?! UNINSTALL! 🗑️")
        elif trophy_change < -100:
            roasts.append(f"Down {abs(trophy_change)} trophies. Skill regression is REAL! 📉")
        elif trophy_change < -50:
            roasts.append(f"Lost {abs(trophy_change)} trophies. We're going BACKWARDS! ⏪")
        elif trophy_change < 0:
            roasts.append(f"Negative trophy week. That's the OPPOSITE of progress! 😬")
        elif trophy_change == 0:
            roasts.append("Zero trophy movement? Just EXISTING at this point! 😴")
        elif trophy_change < 100:
            roasts.append(f"Only +{trophy_change} trophies? Moving slower than a glacier! 🧊")

        # Recent win rate
        if win_rate is not None:
            if win_rate < 35:
                roasts.append(f"{win_rate}% win rate this week?! An AI playing random cards would do better! 🤖")
            elif win_rate < 45:
                roasts.append(f"{win_rate}% recent win rate. That's PAINFUL to watch! 😭")
            elif win_rate < 50:
                roasts.append(f"{win_rate}% win rate. Still can't crack 50%... SAD! 😔")

        # Loss analysis
        if loss_change > 30:
            roasts.append(f"{loss_change} losses this week?! Touch grass. Seriously. 🌱")

        if loss_change > win_change * 2:
            roasts.append("TWO losses for every win?! That's not a ratio, that's a DISASTER! 💥")

    # ALWAYS add a random savage roast to guarantee negativity
    savage_roasts = [
        "After all this time, THIS is your best? Tragic! 💀",
        "I've seen better stats from bots! 🤖",
        "Your opponents must LOVE seeing you in matchmaking! 😂",
        "Bet your clan is just THRILLED to have you! 🙄",
        "These stats are giving 'participation trophy' energy! 🏆",
        "Not even the matchmaking algorithm thinks you're good! 🎰",
        "Your deck isn't the problem... YOU are! 👆",
        "I'd ask if you need tips but it might be too late! ⏰",
        "These numbers are EMBARRASSING! Did you try? 🤔",
        "Your parents must be so proud of these stats! 👨‍👩‍👦"
    ]
    roasts.append(random.choice(savage_roasts))

    return roasts

def get_performance_emoji(player_data, trends):
    """Get emoji based on overall performance"""
    # Check if player is whitelisted
    player_tag = player_data.get('tag', '')
    if is_whitelisted(player_tag):
        return "👑"

    if not trends:
        return "📊"

    trophy_change = trends.get('trophy_change', 0)
    win_rate = trends.get('win_rate', 50)

    if trophy_change < -100 or (win_rate and win_rate < 30):
        return "💀"
    elif trophy_change < 0 or (win_rate and win_rate < 45):
        return "📉"
    elif trophy_change < 50:
        return "😐"
    elif trophy_change < 150:
        return "📈"
    else:
        return "🔥"

def get_skill_rating(player_data, trends):
    """Brutally honest skill rating based on comprehensive stats"""
    # Check if player is whitelisted
    player_tag = player_data.get('tag', '')
    if is_whitelisted(player_tag):
        return "🏆 PHENOMENAL - ABSOLUTE GOAT STATUS"

    # Calculate lifetime win rate
    wins = player_data.get('wins', 0)
    losses = player_data.get('losses', 0)
    total_games = wins + losses
    lifetime_win_rate = (wins / total_games * 100) if total_games > 0 else 50

    # Base score on lifetime performance
    score = lifetime_win_rate

    # Adjust for recent trends
    if trends:
        win_rate = trends.get('win_rate') or 50
        trophy_change = trends.get('trophy_change', 0)

        # Weight recent performance
        score = (lifetime_win_rate * 0.6) + (win_rate * 0.3) + (trophy_change / 20)

    # Trophy adjustment
    trophies = player_data.get('trophies', 0)
    if trophies < 5000:
        score -= 15
    elif trophies < 6000:
        score -= 10
    elif trophies < 7000:
        score -= 5

    # Savage ratings (biased toward negativity)
    if score < 30:
        return "Absolute Garbage 🗑️💀"
    elif score < 40:
        return "Certified Bot 🤖"
    elif score < 48:
        return "Needs Serious Help 📚🆘"
    elif score < 52:
        return "Below Average (trash) 😬"
    elif score < 56:
        return "Painfully Mid 😐"
    elif score < 60:
        return "Barely Decent 👍"
    elif score < 65:
        return "Okay I Guess 🤷"
    elif score < 70:
        return "Actually Not Bad 💪"
    elif score < 75:
        return "Pretty Good (rare) 🔥"
    else:
        return "Cracked (but probably got lucky) 👑"
