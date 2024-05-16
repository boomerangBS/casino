import interactions, random, asyncio
from interactions import Extension
from interactions.ext.prefixed_commands import prefixed_command
isbj=[]
class Bj(Extension):
    def __init__(self, bot):
        self.bot = bot
    
    @prefixed_command(aliases=["bj"])
    async def blackjack(self, ctx,amount=None):
        e=interactions.Embed(title="BlackJack",description="aa",color=0x34c924)
        # await ctx.send(embed=e)
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
        if amount > 50000 and amount != 34567 or amount < 500:
            await ctx.reply("La mise doit etre comprise entre 500 et 50,000 coins !")
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
        
        #if there is two same card on the player hand
        def duplicate(hand):
            return hand[0][:-1] == hand[1][:-1]
        while True:
            if is_blackjack(player_hand):
                isbj.remove(ctx.author.id)
                embed=interactions.Embed(title="🎲 BlackJack",description=f"Vous avez un total de {calculate_hand_value(player_hand)} et le croupier de {calculate_hand_value(dealer_hand)}\nVictoire! Vous avez gagné {amount} coins !")
                embed.set_footer(text=self.bot.config['footer'])
                check=self.bot.bdd.check_user(ctx.author.id)[0]
                coins=self.bot.bdd.check_user(ctx.author.id)[0]["coins"]
                self.bot.bdd.set_coins(coins+amount*2,ctx.author.id)
                await ctx.reply(embed=embed)
                return
            embed = interactions.Embed(title="🎲 BlackJack")
            embed.add_field(name="Votre main",value=f"Cartes: {' '.join(['`'+player_hand[i]+'`' for i in range(len(player_hand))])} \nTotal: {calculate_hand_value(player_hand)}",inline=True)
            embed.add_field(name="Main du croupier",value=f"Cartes: `{dealer_hand[0]}` `?`\nTotal: ?",inline=True)
            embed.set_footer(text=self.bot.config['footer'])
            if calculate_hand_value(player_hand) == 9 or calculate_hand_value(player_hand) == 10 or calculate_hand_value(player_hand) == 11:
                buttons=[interactions.Button(label="Hit",style=interactions.ButtonStyle.BLUE,custom_id="hit"),interactions.Button(label="Double Hit",style=interactions.ButtonStyle.BLUE,custom_id="double"),interactions.Button(label="Stand",style=interactions.ButtonStyle.BLUE,custom_id="stand"),interactions.Button(label="Annuler",style=interactions.ButtonStyle.RED,custom_id="cancel")]
            elif duplicate(player_hand):
                buttons=[interactions.Button(label="Hit",style=interactions.ButtonStyle.BLUE,custom_id="hit"),interactions.Button(label="Stand",style=interactions.ButtonStyle.BLUE,custom_id="stand"),interactions.Button(label="Split",style=interactions.ButtonStyle.BLUE,custom_id="split"),interactions.Button(label="Annuler",style=interactions.ButtonStyle.RED,custom_id="cancel")]
            else:
                buttons=[interactions.Button(label="Hit",style=interactions.ButtonStyle.BLUE,custom_id="hit"),interactions.Button(label="Stand",style=interactions.ButtonStyle.BLUE,custom_id="stand"),interactions.Button(label="Annuler",style=interactions.ButtonStyle.RED,custom_id="cancel")]
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
            # Pre process the response
            coins=self.bot.bdd.check_user(ctx.author.id)[0]["coins"]
            if response.ctx.custom_id == "double":
                if coins < amount:
                    await ctx.reply("Vous n'avez pas assez de coins pour doubler la mise ! Voulez-vous hit ou stand ?")
                    buttons=[interactions.Button(label="Hit",style=interactions.ButtonStyle.BLUE,custom_id="hit"),interactions.Button(label="Stand",style=interactions.ButtonStyle.BLUE,custom_id="stand"),interactions.Button(label="Annuler",style=interactions.ButtonStyle.RED,custom_id="cancel")]
                    msg=await ctx.reply(embed=embed,components=[buttons])
                    try:
                        response2 = await self.bot.wait_for_component(components=buttons, timeout=100,check=lambda i: i.ctx.author == ctx.author and i.ctx.message == msg)
                        await response2.ctx.defer(edit_origin=True)
                    except asyncio.TimeoutError:
                        isbj.remove(ctx.author.id)
                        await ctx.reply("Temps écoulé! Vous avez perdu!")
                        await msg.edit(components=[])
                        return
                    if response2.ctx.custom_id == "hit":
                        response.ctx.custom_id = "hit"
                    elif response2.ctx.custom_id == "stand":
                        response.ctx.custom_id = "stand"
                    else:
                        response.ctx.custom_id = "cancel"
                    await response2.ctx.edit(components=[])
            if response.ctx.custom_id == "split":
                if coins < amount:
                    await ctx.reply("Vous n'avez pas assez de coins pour doubler la mise ! Voulez-vous hit ou stand ?")
                    buttons=[interactions.Button(label="Hit",style=interactions.ButtonStyle.BLUE,custom_id="hit"),interactions.Button(label="Stand",style=interactions.ButtonStyle.BLUE,custom_id="stand"),interactions.Button(label="Annuler",style=interactions.ButtonStyle.RED,custom_id="cancel")]
                    msg=await ctx.reply(embed=embed,components=[buttons])
                    try:
                        response2 = await self.bot.wait_for_component(components=buttons, timeout=100,check=lambda i: i.ctx.author == ctx.author and i.ctx.message == msg)
                        await response2.ctx.defer(edit_origin=True)
                    except asyncio.TimeoutError:
                        isbj.remove(ctx.author.id)
                        await ctx.reply("Temps écoulé! Vous avez perdu!")
                        await msg.edit(components=[])
                        return
                    if response2.ctx.custom_id == "hit":
                        response.ctx.custom_id = "hit"
                    elif response2.ctx.custom_id == "stand":
                        response.ctx.custom_id = "stand"
                    else:
                        response.ctx.custom_id = "cancel"
                    await response2.ctx.edit(components=[])
                else:
                    coins = coins - amount
                    self.bot.bdd.set_coins(coins,ctx.author.id)

            # Double hit 
            if response.ctx.custom_id == "double":
                player_hand.append(deck.pop())
                if is_blackjack(player_hand):
                    isbj.remove(ctx.author.id)
                    embed=interactions.Embed(title="🎲 BlackJack",description=f"Vous avez un total de {calculate_hand_value(player_hand)} et le croupier de {calculate_hand_value(dealer_hand)}\n Double Victoire ! Vous avez gagné {amount*2} coins !")
                    embed.set_footer(text=self.bot.config['footer'])
                    coins=self.bot.bdd.check_user(ctx.author.id)[0]["coins"]
                    self.bot.bdd.set_coins(coins+amount*3,ctx.author.id)
                    await ctx.reply(embed=embed)
                    return
                while calculate_hand_value(dealer_hand) < 17:
                    dealer_hand.append(deck.pop())
                player_value = calculate_hand_value(player_hand)
                dealer_value = calculate_hand_value(dealer_hand)
                if is_bust(dealer_hand):
                    isbj.remove(ctx.author.id)
                    embed=interactions.Embed(title="🎲 BlackJack",description=f"Vous avez un total de {calculate_hand_value(player_hand)} et le croupier de {calculate_hand_value(dealer_hand)}\nDouble victoire ! Vous avez gagné {amount*2} coins !")
                    embed.set_footer(text=self.bot.config['footer'])
                    coins=self.bot.bdd.check_user(ctx.author.id)[0]["coins"]
                    self.bot.bdd.set_coins(coins+amount*3,ctx.author.id)
                    await ctx.reply(embed=embed)
                elif player_value > dealer_value:
                    isbj.remove(ctx.author.id)
                    embed=interactions.Embed(title="🎲 BlackJack",description=f"Vous avez un total de {calculate_hand_value(player_hand)} et le croupier de {calculate_hand_value(dealer_hand)}\nDouble victoire ! Vous avez gagné {amount*2} coins !")
                    embed.set_footer(text=self.bot.config['footer'])
                    coins=self.bot.bdd.check_user(ctx.author.id)[0]["coins"]
                    self.bot.bdd.set_coins(coins+amount*3,ctx.author.id)
                    await ctx.reply(embed=embed)
                elif player_value < dealer_value:
                    isbj.remove(ctx.author.id)
                    embed=interactions.Embed(title="🎲BlackJack",description=f"Vous avez un total de {calculate_hand_value(player_hand)} et le croupier de {calculate_hand_value(dealer_hand)}\n Double défaite ! Vous avez perdu {amount*2} coins !")
                    coins=self.bot.bdd.check_user(ctx.author.id)[0]["coins"]
                    self.bot.bdd.set_coins(coins-amount,ctx.author.id)
                    embed.set_footer(text=self.bot.config['footer'])
                    await ctx.reply(embed=embed)
                else:
                    isbj.remove(ctx.author.id)
                    embed=interactions.Embed(title="🎲 BlackJack",description=f"Vous avez un total de {calculate_hand_value(player_hand)} et le croupier de {calculate_hand_value(dealer_hand)}\nÉgalité ! Vous avez été remboursé de {amount} coins!")
                    embed.set_footer(text=self.bot.config['footer'])
                    coins=self.bot.bdd.check_user(ctx.author.id)[0]["coins"]
                    self.bot.bdd.set_coins(coins+amount,ctx.author.id)
                    await ctx.reply(embed=embed)
                return
            
            #! split START HERE
            if response.ctx.custom_id == "split":
                player_hand1 = [player_hand[0], deck.pop()]
                player_hand2 = [player_hand[1], deck.pop()]
                h1=0
                h2=0
                while True:
                    if is_blackjack(player_hand1):
                        embed=interactions.Embed(title="🎲 BlackJack : Split 1",description=f"Vous avez un total de {calculate_hand_value(player_hand1)} et le croupier de {calculate_hand_value(dealer_hand)}\nVictoire! Vous avez gagné {amount} coins !")
                        embed.set_footer(text=self.bot.config['footer'])
                        check=self.bot.bdd.check_user(ctx.author.id)[0]
                        coins=self.bot.bdd.check_user(ctx.author.id)[0]["coins"]
                        self.bot.bdd.set_coins(coins+amount*2,ctx.author.id)
                        await ctx.reply(embed=embed)
                        h1=1
                        break
                    embed = interactions.Embed(title="🎲 BlackJack : Split 1")
                    embed.add_field(name="Votre main",value=f"Cartes: {' '.join(['`'+player_hand1[i]+'`' for i in range(len(player_hand1))])} \nTotal: {calculate_hand_value(player_hand1)}",inline=True)
                    embed.add_field(name="Main du croupier",value=f"Cartes: `{dealer_hand[0]}` `?`\nTotal: ?",inline=True)
                    embed.set_footer(text=self.bot.config['footer'])
                    buttons=[interactions.Button(label="Hit",style=interactions.ButtonStyle.BLUE,custom_id="hit"),interactions.Button(label="Stand",style=interactions.ButtonStyle.BLUE,custom_id="stand"),interactions.Button(label="Annuler",style=interactions.ButtonStyle.RED,custom_id="cancel")]
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
                        player_hand1.append(deck.pop())
                        if int(calculate_hand_value(player_hand1)) == 21:
                            embed=interactions.Embed(title="🎲 BlackJack : Split 1",description=f"Vous avez un total de {calculate_hand_value(player_hand1)} et le croupier de {calculate_hand_value(dealer_hand)}\nVictoire! Vous avez gagné {amount} coins !")
                            embed.set_footer(text=self.bot.config['footer'])
                            check=self.bot.bdd.check_user(ctx.author.id)[0]
                            coins=self.bot.bdd.check_user(ctx.author.id)[0]["coins"]
                            self.bot.bdd.set_coins(coins+amount*2,ctx.author.id)
                            await ctx.reply(embed=embed)
                            h1=1
                            break
                        if is_bust(player_hand1):
                            embed=interactions.Embed(title="🎲 BlackJack : Split 1",description=f"Vous avez un total de {calculate_hand_value(player_hand1)} et le croupier de {calculate_hand_value(dealer_hand)}\nVous avez perdu {amount} coins !")
                            embed.set_footer(text=self.bot.config['footer'])
                            await ctx.reply(embed=embed)
                            h1=1
                            break
                    elif response.ctx.custom_id == "stand":
                        break
                    elif response.ctx.custom_id == "cancel":
                        # arrondi au nombre inferieur
                        am=amount/2
                        am=int(am-am%1)
                        coins=self.bot.bdd.check_user(ctx.author.id)[0]["coins"]
                        self.bot.bdd.set_coins(int(coins+am),ctx.author.id)
                        await ctx.reply("Partie annulée !")
                        h1=1
                        break
                while True:
                    if is_blackjack(player_hand2):
                        embed=interactions.Embed(title="🎲 BlackJack : Split 2",description=f"Vous avez un total de {calculate_hand_value(player_hand2)} et le croupier de {calculate_hand_value(dealer_hand)}\nVictoire! Vous avez gagné {amount} coins !")
                        embed.set_footer(text=self.bot.config['footer'])
                        check=self.bot.bdd.check_user(ctx.author.id)[0]
                        coins=self.bot.bdd.check_user(ctx.author.id)[0]["coins"]
                        self.bot.bdd.set_coins(coins+amount*2,ctx.author.id)
                        await ctx.reply(embed=embed)
                        h2=1
                        break
                    embed = interactions.Embed(title="🎲 BlackJack : Split 2")
                    embed.add_field(name="Votre main",value=f"Cartes: {' '.join(['`'+player_hand2[i]+'`' for i in range(len(player_hand2))])} \nTotal: {calculate_hand_value(player_hand2)}",inline=True)
                    embed.add_field(name="Main du croupier",value=f"Cartes: `{dealer_hand[0]}` `?`\nTotal: ?",inline=True)
                    embed.set_footer(text=self.bot.config['footer'])
                    buttons=[interactions.Button(label="Hit",style=interactions.ButtonStyle.BLUE,custom_id="hit"),interactions.Button(label="Stand",style=interactions.ButtonStyle.BLUE,custom_id="stand"),interactions.Button(label="Annuler",style=interactions.ButtonStyle.RED,custom_id="cancel")]
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
                        player_hand2.append(deck.pop())
                        if int(calculate_hand_value(player_hand2)) == 21:
                            embed=interactions.Embed(title="🎲 BlackJack : Split 2",description=f"Vous avez un total de {calculate_hand_value(player_hand2)} et le croupier de {calculate_hand_value(dealer_hand)}\nVictoire! Vous avez gagné {amount} coins !")
                            embed.set_footer(text=self.bot.config['footer'])
                            check=self.bot.bdd.check_user(ctx.author.id)[0]
                            coins=self.bot.bdd.check_user(ctx.author.id)[0]["coins"]
                            self.bot.bdd.set_coins(coins+amount*2,ctx.author.id)
                            await ctx.reply(embed=embed)
                            h2=1
                            break
                        if is_bust(player_hand2):
                            embed=interactions.Embed(title="🎲 BlackJack : Split 2",description=f"Vous avez un total de {calculate_hand_value(player_hand2)} et le croupier de {calculate_hand_value(dealer_hand)}\nVous avez perdu {amount} coins !")
                            embed.set_footer(text=self.bot.config['footer'])
                            await ctx.reply(embed=embed)
                            h2=1
                            break
                    elif response.ctx.custom_id == "stand":
                        break
                    elif response.ctx.custom_id == "cancel":
                        # arrondi au nombre inferieur
                        am=amount/2
                        am=int(am-am%1)
                        coins=self.bot.bdd.check_user(ctx.author.id)[0]["coins"]
                        self.bot.bdd.set_coins(int(coins+am),ctx.author.id)
                        await ctx.reply("Partie annulée !")
                        h2=1
                        break
                # Dealer's turn (split)
                while calculate_hand_value(dealer_hand) < 17:
                    dealer_hand.append(deck.pop())
                # Compare hands 
                player_value1 = calculate_hand_value(player_hand1)
                player_value2 = calculate_hand_value(player_hand2)
                dealer_value = calculate_hand_value(dealer_hand)
                check=self.bot.bdd.check_user(ctx.author.id)[0]
                # SPLIT 1
                if h1 != 1:
                    if is_bust(dealer_hand):
                        embed=interactions.Embed(title="🎲 BlackJack : Split 1",description=f"Vous avez un total de {calculate_hand_value(player_hand1)} et le croupier de {calculate_hand_value(dealer_hand)}\nVous avez gagné {amount} coins!")
                        embed.set_footer(text=self.bot.config['footer'])
                        coins=self.bot.bdd.check_user(ctx.author.id)[0]["coins"]
                        self.bot.bdd.set_coins(coins+amount*2,ctx.author.id)
                        await ctx.reply(embed=embed)
                    elif player_value1 > dealer_value:
                        embed=interactions.Embed(title="🎲 BlackJack : Split 1",description=f"Vous avez un total de {calculate_hand_value(player_hand1)} et le croupier de {calculate_hand_value(dealer_hand)}\nVous avez gagné {amount} coins !")
                        embed.set_footer(text=self.bot.config['footer'])
                        coins=self.bot.bdd.check_user(ctx.author.id)[0]["coins"]
                        self.bot.bdd.set_coins(coins+amount*2,ctx.author.id)
                        await ctx.reply(embed=embed)
                    elif player_value1 < dealer_value:
                        embed=interactions.Embed(title="🎲 BlackJack : Split 1",description=f"Vous avez un total de {calculate_hand_value(player_hand1)} et le croupier de {calculate_hand_value(dealer_hand)}\nVous avez perdu {amount} coins !")
                        embed.set_footer(text=self.bot.config['footer'])
                        await ctx.reply(embed=embed)
                    else:
                        embed=interactions.Embed(title="🎲 BlackJack : Split 1",description=f"Vous avez un total de {calculate_hand_value(player_hand1)} et le croupier de {calculate_hand_value(dealer_hand)}\nÉgalité ! Vous avez été remboursé de {amount} coins!")
                        embed.set_footer(text=self.bot.config['footer'])
                        coins=self.bot.bdd.check_user(ctx.author.id)[0]["coins"]
                        self.bot.bdd.set_coins(coins+amount,ctx.author.id)
                        await ctx.reply(embed=embed)
                # SPLIT 2
                if h2 != 1:
                    if is_bust(dealer_hand):
                        embed=interactions.Embed(title="🎲 BlackJack : Split 2",description=f"Vous avez un total de {calculate_hand_value(player_hand2)} et le croupier de {calculate_hand_value(dealer_hand)}\nVous avez gagné {amount} coins!")
                        embed.set_footer(text=self.bot.config['footer'])
                        coins=self.bot.bdd.check_user(ctx.author.id)[0]["coins"]
                        self.bot.bdd.set_coins(coins+amount*2,ctx.author.id)
                        await ctx.reply(embed=embed)
                    elif player_value2 > dealer_value:
                        embed=interactions.Embed(title="🎲 BlackJack : Split 2",description=f"Vous avez un total de {calculate_hand_value(player_hand2)} et le croupier de {calculate_hand_value(dealer_hand)}\nVous avez gagné {amount} coins !")
                        embed.set_footer(text=self.bot.config['footer'])
                        coins=self.bot.bdd.check_user(ctx.author.id)[0]["coins"]
                        self.bot.bdd.set_coins(coins+amount*2,ctx.author.id)
                        await ctx.reply(embed=embed)
                    elif player_value2 < dealer_value:
                        embed=interactions.Embed(title="🎲 BlackJack : Split 2",description=f"Vous avez un total de {calculate_hand_value(player_hand2)} et le croupier de {calculate_hand_value(dealer_hand)}\nVous avez perdu {amount} coins !")
                        embed.set_footer(text=self.bot.config['footer'])
                        await ctx.reply(embed=embed)
                    else:
                        embed=interactions.Embed(title="🎲 BlackJack : Split 2",description=f"Vous avez un total de {calculate_hand_value(player_hand2)} et le croupier de {calculate_hand_value(dealer_hand)}\nÉgalité ! Vous avez été remboursé de {amount} coins!")
                        embed.set_footer(text=self.bot.config['footer'])
                        coins=self.bot.bdd.check_user(ctx.author.id)[0]["coins"]
                        self.bot.bdd.set_coins(coins+amount,ctx.author.id)
                        await ctx.reply(embed=embed)
                isbj.remove(ctx.author.id)

            #! split END HERE
            #simple hit
            if response.ctx.custom_id == "hit":
                player_hand.append(deck.pop())
                if int(calculate_hand_value(player_hand)) == 21:
                    isbj.remove(ctx.author.id)
                    embed=interactions.Embed(title="🎲 BlackJack",description=f"Vous avez un total de {calculate_hand_value(player_hand)} et le croupier de {calculate_hand_value(dealer_hand)}\nVictoire! Vous avez gagné {amount} coins !")
                    embed.set_footer(text=self.bot.config['footer'])
                    check=self.bot.bdd.check_user(ctx.author.id)[0]
                    coins=self.bot.bdd.check_user(ctx.author.id)[0]["coins"]
                    self.bot.bdd.set_coins(coins+amount*2,ctx.author.id)
                    await ctx.reply(embed=embed)
                    return
                if is_bust(player_hand):
                    isbj.remove(ctx.author.id)
                    embed=interactions.Embed(title="🎲 BlackJack",description=f"Vous avez un total de {calculate_hand_value(player_hand)} et le croupier de {calculate_hand_value(dealer_hand)}\nVous avez perdu {amount} coins !")
                    embed.set_footer(text=self.bot.config['footer'])
                    await ctx.reply(embed=embed)
                    return
            #stand
            elif response.ctx.custom_id == "stand":
                break
            elif response.ctx.custom_id == "cancel":
                # arrondi au nombre inferieur
                isbj.remove(ctx.author.id)
                am=amount/2
                am=int(am-am%1)
                coins=self.bot.bdd.check_user(ctx.author.id)[0]["coins"]
                self.bot.bdd.set_coins(int(coins+am),ctx.author.id)
                await ctx.reply("Partie annulée !")
                return

        # Dealer's turn
        while calculate_hand_value(dealer_hand) < 17:
            dealer_hand.append(deck.pop())

        # Compare hands
        player_value = calculate_hand_value(player_hand)
        dealer_value = calculate_hand_value(dealer_hand)
        check=self.bot.bdd.check_user(ctx.author.id)[0]
        if is_bust(dealer_hand):
            isbj.remove(ctx.author.id)
            embed=interactions.Embed(title="🎲 BlackJack",description=f"Vous avez un total de {calculate_hand_value(player_hand)} et le croupier de {calculate_hand_value(dealer_hand)}\nVous avez gagné {amount} coins!")
            embed.set_footer(text=self.bot.config['footer'])
            coins=self.bot.bdd.check_user(ctx.author.id)[0]["coins"]
            self.bot.bdd.set_coins(coins+amount*2,ctx.author.id)
            await ctx.reply(embed=embed)
        elif player_value > dealer_value:
            isbj.remove(ctx.author.id)
            embed=interactions.Embed(title="🎲 BlackJack",description=f"Vous avez un total de {calculate_hand_value(player_hand)} et le croupier de {calculate_hand_value(dealer_hand)}\nVous avez gagné {amount} coins !")
            embed.set_footer(text=self.bot.config['footer'])
            coins=self.bot.bdd.check_user(ctx.author.id)[0]["coins"]
            self.bot.bdd.set_coins(coins+amount*2,ctx.author.id)
            await ctx.reply(embed=embed)
        elif player_value < dealer_value:
            isbj.remove(ctx.author.id)
            embed=interactions.Embed(title="🎲 BlackJack",description=f"Vous avez un total de {calculate_hand_value(player_hand)} et le croupier de {calculate_hand_value(dealer_hand)}\nVous avez perdu {amount} coins !")
            embed.set_footer(text=self.bot.config['footer'])
            await ctx.reply(embed=embed)
        else:
            isbj.remove(ctx.author.id)
            embed=interactions.Embed(title="🎲 BlackJack",description=f"Vous avez un total de {calculate_hand_value(player_hand)} et le croupier de {calculate_hand_value(dealer_hand)}\nÉgalité ! Vous avez été remboursé de {amount} coins!")
            embed.set_footer(text=self.bot.config['footer'])
            coins=self.bot.bdd.check_user(ctx.author.id)[0]["coins"]
            self.bot.bdd.set_coins(coins+amount,ctx.author.id)
            await ctx.reply(embed=embed)
