import interactions, random, asyncio
from interactions import Extension
from interactions.ext.prefixed_commands import prefixed_command
isbj=[]
class Bj(Extension):
    def __init__(self, bot):
        self.bot = bot
    
    @prefixed_command(aliases=["bj"])
    async def blackjack(self, ctx,amount=None):
        if amount == None:
            await ctx.reply("Vous devez spécifier une mise !")
            return
        if ctx.author.id in isbj:
            await ctx.reply("Vous avez déjà une partie en cours !")
            return
        if amount == "quoicoubeh":
            await ctx.reply("t gnt ptit malin")
        try:
            amount = int(amount)
        except:
            await ctx.reply("Mise invalide !")
            return
        if amount < 1:
            await ctx.reply("Mise invalide !")
            return
        if amount > 30000 and amount != 34567:
            await ctx.reply("Mise trop élevée !")
            return
        check = self.bot.bdd.check_user(ctx.author.id)
        if check != []:
            check = check[0]
            if check["coins"] < amount:
                await ctx.reply("Vous n'avez pas assez de coins !")
                return
            coins = check["coins"] - amount
            self.bot.bdd.set_coins(coins,ctx.author.id)

        else:
            return
        isbj.append(ctx.author.id)
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

        while True:
            embed = interactions.Embed(title="BlackJack")
            embed.add_field(name="Votre main",value=f"Cartes {' '.join(['`'+player_hand[i]+'`' for i in range(len(player_hand))])} \nTotal: {calculate_hand_value(player_hand)}",inline=True)
            embed.add_field(name="Main du croupier",value=f"Cartes: `{dealer_hand[0]}` `?`\nTotal: ?",inline=True)
            embed.set_footer(text=self.bot.config['footer'])
            buttons=[interactions.Button(label="Hit",style=interactions.ButtonStyle.BLUE,custom_id="hit"),interactions.Button(label="Stand",style=interactions.ButtonStyle.BLUE,custom_id="stand")]
            msg=await ctx.reply(embed=embed,components=[buttons])
            try:
                response = await self.bot.wait_for_component(components=buttons, timeout=100,check=lambda i: i.ctx.author == ctx.author and i.ctx.message == msg)
                await response.ctx.defer(edit_origin=True)
            except asyncio.TimeoutError:
                isbj.remove(ctx.author.id)
                await ctx.reply("Temps écoulé! Vous avez perdu!")
                await msg.edit(components=[])
                return
            await response.ctx.edit(components=[])
            if response.ctx.custom_id == "hit":
                player_hand.append(deck.pop())
                if int(calculate_hand_value(player_hand)) == 21:
                    isbj.remove(ctx.author.id)
                    embed=interactions.Embed(title="BlackJack",description=f"Vous avez un total de {calculate_hand_value(player_hand)} et le croupier de {calculate_hand_value(dealer_hand)}\nBlackJack! Vous avez gagné {amount} coins !")
                    embed.set_footer(text=self.bot.config['footer'])
                    check=self.bot.bdd.check_user(ctx.author.id)[0]
                    self.bot.bdd.set_coins(check["coins"]+amount*2,ctx.author.id)
                    await ctx.reply(embed=embed)
                    return
                if is_bust(player_hand):
                    isbj.remove(ctx.author.id)
                    embed=interactions.Embed(title="BlackJack",description=f"Vous avez un total de {calculate_hand_value(player_hand)} et le croupier de {calculate_hand_value(dealer_hand)}\nVous avez perdu!")
                    embed.set_footer(text=self.bot.config['footer'])
                    await ctx.reply(embed=embed)
                    return
            elif response.ctx.custom_id == "stand":
                break

        # Dealer's turn
        while calculate_hand_value(dealer_hand) < 17:
            dealer_hand.append(deck.pop())

        # Compare hands
        player_value = calculate_hand_value(player_hand)
        dealer_value = calculate_hand_value(dealer_hand)
        check=self.bot.bdd.check_user(ctx.author.id)[0]
        if is_bust(dealer_hand):
            isbj.remove(ctx.author.id)
            embed=interactions.Embed(title="BlackJack",description=f"Vous avez un total de {calculate_hand_value(player_hand)} et le croupier de {calculate_hand_value(dealer_hand)}\nVous avez gagné {amount} coins!")
            embed.set_footer(text=self.bot.config['footer'])
            self.bot.bdd.set_coins(check["coins"]+amount*2,ctx.author.id)
            await ctx.reply(embed=embed)
        elif player_value > dealer_value:
            isbj.remove(ctx.author.id)
            embed=interactions.Embed(title="BlackJack",description=f"Vous avez un total de {calculate_hand_value(player_hand)} et le croupier de {calculate_hand_value(dealer_hand)}\nVous avez gagné {amount} coins !")
            embed.set_footer(text=self.bot.config['footer'])
            self.bot.bdd.set_coins(check["coins"]+amount*2,ctx.author.id)
            await ctx.reply(embed=embed)
        elif player_value < dealer_value:
            isbj.remove(ctx.author.id)
            embed=interactions.Embed(title="BlackJack",description=f"Vous avez un total de {calculate_hand_value(player_hand)} et le croupier de {calculate_hand_value(dealer_hand)}\nVous avez perdu!")
            embed.set_footer(text=self.bot.config['footer'])
            await ctx.reply(embed=embed)
        else:
            isbj.remove(ctx.author.id)
            embed=interactions.Embed(title="BlackJack",description=f"Vous avez un total de {calculate_hand_value(player_hand)} et le croupier de {calculate_hand_value(dealer_hand)}\nÉgalité ! Vous avez été remboursé de {amount} coins!")
            embed.set_footer(text=self.bot.config['footer'])
            self.bot.bdd.set_coins(check["coins"]+amount,ctx.author.id)
            await ctx.reply(embed=embed)
