import interactions,asyncio
from interactions import Extension,Button,ButtonStyle
from interactions.ext.prefixed_commands import prefixed_command
from datetime import datetime
from utils import console
import random


class Bj(Extension):
    def __init__(self, bot):
        self.bot = bot
    
    @prefixed_command()
    async def blackjack(self,ctx):
        suits = ['♠', '♡', '♢', '♣']
        ranks = ['A', '2', '3', '4', '5', '6', '7', '8', '9', '10', 'J', 'Q', 'K']
        deck = [f'{rank}{suit}' for suit in suits for rank in ranks]

        # Shuffle the deck
        random.shuffle(deck)

        # Deal initial cards to the player and the dealer
        player_hand = [deck.pop(), deck.pop()]
        dealer_hand = [deck.pop(), deck.pop()]

        # Calculate the value of a hand
        def calculate_hand_value(hand):
            values = {'A': 11, '2': 2, '3': 3, '4': 4, '5': 5, '6': 6, '7': 7, '8': 8, '9': 9, '10': 10, 'J': 10, 'Q': 10, 'K': 10}
            value = sum([values[card[:-1]] for card in hand])
            # Adjust for Aces
            num_aces = sum([1 for card in hand if card[:-1] == 'A'])
            while value > 21 and num_aces > 0:
                value -= 10
                num_aces -= 1
            return value

        # Check if a hand is a blackjack
        def is_blackjack(hand):
            return len(hand) == 2 and calculate_hand_value(hand) == 21

        # Check if a hand is bust
        def is_bust(hand):
            return calculate_hand_value(hand) > 21

    # Play the blackjack game

        # Deal initial cards
        player_hand = [deck.pop(), deck.pop()]
        dealer_hand = [deck.pop(), deck.pop()]

        # Show player's hand and one of the dealer's cards
        await ctx.send(f"Player's hand: {', '.join(player_hand)}")
        await ctx.send(f"Dealer's hand: {dealer_hand[0]}, ?")

        # Check if player has a blackjack
        if is_blackjack(player_hand):
            await ctx.send("Player has a blackjack! Player wins!")
            return

        # Player's turn
        while True:
            # Ask player to hit or stand
            def checkss(m):
                m = m.message
                return m.author == ctx.author and m.channel == ctx.channel
            await ctx.send("Do you want to hit or stand? (h/s)")
            response = await self.bot.wait_for('message_create', checks=checkss, timeout=50)
            response = response.message
            if response.content.lower() == 'h':
                # Player hits
                player_hand.append(deck.pop())
                await ctx.send(f"Player's hand: {', '.join(player_hand)}")
                if is_bust(player_hand):
                    await ctx.send("Player busts! Dealer wins!")
                    return
            elif response.content.lower() == 's':
                # Player stands
                break

        # Dealer's turn
        while calculate_hand_value(dealer_hand) < 17:
            dealer_hand.append(deck.pop())

        # Show dealer's hand
        await ctx.send(f"Dealer's hand: {', '.join(dealer_hand)}")

        # Check if dealer has a blackjack or busts
        if is_blackjack(dealer_hand):
            await ctx.send("Dealer has a blackjack! Dealer wins!")
        elif is_bust(dealer_hand):
            await ctx.send("Dealer busts! Player wins!")
        else:
            # Compare hands
            player_value = calculate_hand_value(player_hand)
            dealer_value = calculate_hand_value(dealer_hand)
            if player_value > dealer_value:
                await ctx.send("Player wins!")
            elif player_value < dealer_value:
                await ctx.send("Dealer wins!")
            else:
                await ctx.send("It's a tie!")
        # Define the deck of card