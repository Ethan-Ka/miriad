import lightbulb
import threading
#import keep_alive
import hikari
import random
from datetime import datetime, timedelta

import os
import json
import schedule
import re
import ailibrary
#os.system("pip install --force-reinstall --no-cache-dir git+https://github.com/thesadru/hikari@3338f586a70f35c8edb7e556ba2faba17fa5b8fe")
#os.system("") 
#os.system("")
import miru
import cache

#os.system("miru")
openAI = ailibrary.AILibrary()

cache = cache.Cache(
    immediate_push=True,
    use_file=True#,
    #auto_execute_on_run=False
)

class embedColors:
  green = "#57F287"
  blue = "#3498DB"
  orange = "#E67E22"
  red = "#ED4245"


class color:

  red = "\033[1;31m"
  green = "\033[1;;32m"
  blue = "\033[4;;34m"


#format date and time for uptime commands
print(datetime.now())
dtstr = "2022-09-06 14:27:47"
global dt_formatted
dt_formatted = datetime.fromisoformat(dtstr)
global startTime
startTime = datetime.now(dt_formatted.tzinfo)

# global variables #
global version
version = "1.4.5"

global lines
lines = str(1090 + 173)  #str([main.py] + [ccDatabase.py])

global statusSTR
statusSTR = "/seecoins | Version " + version + " | " + lines + " lines of code"



# SET IF MAKING CHANGES
global developing
developing = False


def consoleLog(type, message):
  if type == color.red:

      #print(type + " - " + message + " ✗" + "\033[0m")
      print(" - " + message + " ✗")
  if type == color.green:
      #print(type + " - " + message + " ✓" + "\033[0m")
      print( " - " + message + " ✓")
  else:
      #print("\033[1m" + type + " * " + message + "\033[0m")
      print(" * " + message)


global myViewUser
myViewUser = ""
global myViewGuild
myViewGuild = ""



class MakeConvo(miru.Modal):
  name = miru.TextInput(label="Reply", placeholder="Message to reply with", required=True)
 
  async def callback(self, ctx: miru.ModalContext) -> None:
        guild = ctx.guild_id
        author = ctx.user.id
        myViewUser = ctx.user.id
        myViewGuild = ctx.guild_id
        job = cache.fetch_job(self.custom_id)
        splitted = job.split("=-=")
        existing = splitted[0]
        model = splitted[1]
        
        #print(model)
        
        if not "AI: " in existing:
          self.prompt = "The following is a conversation with an AI assistant. The assistant is helpful, creative, clever, and very friendly."+f"AI: {existing.strip()} Human:"
        else:
          self.prompt = "The following is a conversation with an AI assistant. The assistant is helpful, creative, clever, and very friendly."+f"{existing.strip()}\n Human:"
          
        #await modal.send(ctx.interaction)
        content = [value for value in ctx.values.values()][0]
        print(content)
        #await modal.start()
        if content=="":
          return
        content = list(self.values.values())[0]
        punct = ['.', '?', '!']
        if not any(word in content for word in punct):
            content = content+"."
        prompt = self.prompt+content
        #respond before sending request because it times out
        msgs = await ctx.respond("Responding...", flags = hikari.MessageFlag.EPHEMERAL)
        interaction = openAI.text(prompt, model)
        reason = interaction[2]
        await msgs.edit("Responded!")
        #await ctx.respond("Interaction complete")
        print(len(interaction[0]))
        if len(interaction[0]) < 256:
          if len(prompt) > 255:
            print(len(prompt))
            promptDisplay = prompt.rsplit(':', 1)[1]
            promptDisplay = "Human: "+promptDisplay
          else:
            promptDisplay = prompt
          if reason == "stop":
            
            reason = "Finished Successfully"
    
            embed = hikari.Embed(title="Response", color=embedColors.blue, description=f"**Finish Reason**: {reason}\n**Model**: {model}")
            embed.add_field("Prompt: "+promptDisplay, interaction[0])
            embed.set_author(
                      name=ctx.author.username, icon=ctx.author.display_avatar_url)
            
          
          # Add the button to the action row. This **must** be called after you have finished building every
            view = AICommand(timeout=120)
            message = await bot.rest.create_message(channel=ctx.channel_id, content=embed, components=view.build())
            #cache.delete_job(author+guild)
            cache.add_job((prompt).strip().rstrip()+interaction[0].rstrip()+"=-="+model, id=str(message.id))
            await msgs.edit(f"Complete. See message {message.make_link(await bot.rest.fetch_guild(guild))}")
            await view.start(message)  # Start listening for interactions
            await view.wait()
        if len(interaction[0]) > 255:
          view = AICommand(timeout=120)
          await ctx.respond("**Finished**\n*Exceeded maximum embed length*\n**Response:**\n"+interaction[0], components=view.build())
          await view.start(message)  # Start listening for interactions
          await view.wait()
          cache.delete_job(author+guild)
            
#    @miru.button(emoji=chr(9209), style=hikari.ButtonStyle.DANGER, row=2)
#   async def stop_button(self, button: miru.Button, ctx: miru.Context):
        #self.stop()

class AICommand(miru.View):
    @miru.button(label="Make Conversation",  style=hikari.ButtonStyle.PRIMARY)
    async def make_convo(self, button: miru.Button, ctx: miru.Context) -> None:
        modal = MakeConvo("Reply", custom_id = str(ctx.message.id)) # Stop listening for interactions
        await ctx.respond_with_modal(modal)
        



bot = lightbulb.BotApp(
    token=os.environ["TOKEN"].strip(),
    banner=None,
    intents = hikari.Intents.ALL
    #default_enabled_guilds=(985315511728492616)
    #default enabled guilds: remove after testing.)
)
miru.load(bot)
#token = os.environ["TOKEN"].split("4")
#print("HI\n\n\n")
#print(token[0]+">>>"+token[1])
###############################
#        Miriad Bot           #
#       Version 1.4.5         #
# created by thedankboi_#2556 #
###############################

global rest
rest = hikari.RESTApp()

global rules
rules = {
    "1":
    "We run on a three strike policy. If you get three strikes you will be muted for 24 hours. If you are muted three times you will be banned from the server. If an admin believes an incident requires a higher level of punsihment you may be banned without a warning",
    "2":
    "Follow Discord TOS/Community Guidelines. If you are unsure about a rule, ask moderators before posting.",
    "3":
    "Do not make jokes aimed towards people based on their disability, race, gender, sexuality, etc. If someone makes a joke towards you report it to an <@&942477754056728655> and they will issue a sanction where neccessary.",
    "4":
    "Do not post ANY personal information such as names, addresses, phone numbers, emails, private usernames, passwords or any form of card and bank information. This goes for both your own and others. Exercise basic internet safety.",
    "5":
    "Deleting a message you know is against the rules of a server still counts as breaking the server rules. No matter how fast you delete it, the moderators will still see it.",
    "6":
    "No difficult to ping names such as fancy font(ex. 𝐔ᔕᗴℝᑎⒶ𝓜€, 🅄🅂🄴🅁🄽🄰🄼🄴, υʂҽɾɳαɱҽ) until discord fixes different font character pings.",
    "6.1":
    "The staff have the right to change your nickname(this will only affect this server) without warning. This is to enable you to be pinged where neccessary",
    "7":
    "Self promotion will only happen in <#1009555289936236665>. If you self promote anywhere else you will get a warning."
}

#for rules commands
global rulesLength
rulesLength = []

# -- Paths to files -- #
global config
config = r"config.txt"

global doneList
doneList = r"doneRoles.txt"




# -- Create functions -- #



def getSetting():
  consoleLog(color.blue, "Do setting")
  setFile = open(config, 'r')
  content = setFile.read()
  global channelID
  channelID = 0
  global hasIntro
  hasIntro = 0
  global roleToAdd
  roleToAdd = 0
  exec(content)
  consoleLog(color.green, "Setting done")


#log message in channel #transactions
async def logMessage(content):
  await bot.rest.create_message(998700348086681720, content=content)


async def log(content):
  log_channel = 998700348086681720
  await bot.rest.create_message(log_channel, content=content)


def randomColor():
  colors = [
      "57F287", "3498DB", "9B59B6", "F1C40F", "E67E22", "34495E", "FFFF00",
      "1ABC9C", "5865F2", "EB459E"
  ]
  col = random.randint(0, 6)
  return "#" + colors[col]


#push settings to config.txt
def pushSettings(channelID, hasIntro, roleToAdd):
  consoleLog(color.blue, "Do config")
  setFile = open(r"config.txt", 'w')
  setFile.write("global channelID \nchannelID=" + str(channelID) +
                "\nglobal hasIntro \nhasIntro=" + str(hasIntro) +
                "\nglobal roleToAdd\nroleToAdd=" + str(roleToAdd))
  consoleLog(color.green, "Push Setting Complete")
  setFile.close()


#check if author.id is in doneList
def checkForAuthor(authorID):
  doneRoles = open(doneList, 'r')
  content = doneRoles.read()
  if authorID in content:
      return True
  else:
      return False


#write to doneRoles.txt
#weird name but it works
def writeToDoneRoles(authorID):
    doneRoles = open(doneList, "a")
    doneRoles.write(authorID)


# -- Leaderboard Commands -- #


#create leaderboard embed


    #RETURN EMBED WITH RULES
def getRules():
    consoleLog(color.blue, "Get rules")
    randC = "#3498DB"
    embed = hikari.Embed(title="Rules",
                         description="Server Rules",
                         color=embedColors.blue)
    for key in rules:
        embed.add_field(str(key), rules[key])
        rulesLength.append(key)
        consoleLog(color.green, "done rule" + key)
    embed.set_footer("/rule [rule] | color: " + randC)
    consoleLog(color.green, "Rules fetched")
    return embed

  


# -- Load Events -- #
@bot.listen(hikari.MemberCreateEvent) # on member join
async def member_join(event):
  member = event.member # get member object
  guild = event.guild_id # get guild id
  member_name = member.username # get member name from object
  member_id = member.id # get member id from object
  


@bot.listen(hikari.StartedEvent)
async def bot_started(event):
    #set now for start message in #1015726410175889489
    
    randC = randomColor()
    now = datetime.now()
    # Send bot has started
    embed = hikari.Embed(title="Bot has started",
                         description="Bot has started at " + str(now.hour) +
                         ":" + str(now.minute) + ":" + str(now.second),
                         color=randC)
    embed.set_thumbnail("miriad.png")
    embed.set_footer("color: " + randC)
    if not developing:
        #send if updates are not in progress
        # PROBABLY NOT NEEDED BECAUSE GITHUB HOSTING
        await bot.rest.create_message(1015726410175889489, content=embed)

    # Update rules
    await bot.rest.edit_message(channel=942477754287411241,
                                message=1020010746433785967,
                                content=getRules())

    getSetting()


    if developing == True:
        hikariStatus = hikari.Status.DO_NOT_DISTURB
        consoleLog(color.green, "developing == True")
    else:
        hikariStatus = hikari.Status.ONLINE
        consoleLog(color.green, "developing == False")
    
    #set discord presence
    await bot.update_presence(status=hikariStatus,
                              activity=hikari.Activity(
                                  name=statusSTR,
                                  type=hikari.ActivityType.PLAYING,
                              ))
    consoleLog(color.green, "set status")

# Message Create Event


# -- Load Commands -- #

event = threading.Event()

@bot.command
@lightbulb.option("prompt",
                  "prompt to send",
                  type=hikari.OptionType.STRING,
                  modifier=lightbulb.OptionModifier.CONSUME_REST,
                  required=True,
                  
)
@lightbulb.option("model",
                  "AI to use",
                  type=hikari.OptionType.STRING,
                  modifier=lightbulb.OptionModifier.CONSUME_REST,
                  required=True,
                  choices=(
                  "text-davinci-002",
                  "text-curie-001",
                  "text-babbage-001",
                  "text-ada-001"
                  )
)
@lightbulb.command("prompt", "send AI a prompt", auto_defer=True, ephemeral=True)
@lightbulb.implements(lightbulb.SlashCommand)
async def text(ctx):
    view = AICommand(timeout=120)
    channel = ctx.channel_id
    prompt = ctx.options.prompt
    model = ctx.options.model
    author = ctx.author.id
    guild = ctx.guild_id
    #print(model)
    msgs= await ctx.respond("Sending AI your prompt...")
    interaction = openAI.text(prompt, model)
    await msgs.edit("Done.")
    reason = interaction[2]
    if len(interaction[0]) < 1024:
      
      if reason == "stop":
        reason = "Finished Successfully"

        embed = hikari.Embed(title="Response", color=embedColors.blue, description=f"**Finish Reason**: {reason}\n**Model**: {model}")
        embed.add_field("Prompt: "+prompt, interaction[0])
        embed.set_author(
                  name=ctx.author.username, icon=ctx.author.display_avatar_url)
      
      
      # Add the button to the action row. This **must** be called after you have finished building every    
        message = await bot.rest.create_message(channel=ctx.channel_id, content=embed, components=view.build())
        cache.add_job("Human: "+prompt.rstrip()+" AI:"+interaction[0]+"=-="+model, id=str(message.id))
      # individual component.
        await view.start(message)  # Start listening for interactions
        await view.wait()
        #await ctx.respond("Request Completed!")


    if len(interaction[0]) > 1024:
      await ctx.respond("**Finished**\n*Exceeded maximum embed length*\n**Response:**\n"+interaction[0])
    


@bot.command
@lightbulb.add_checks(lightbulb.checks.has_role_permissions(32))
@lightbulb.option("seconds",
                  "time to run the poll for(seconds)",
                  type=hikari.OptionType.INTEGER,
                  modifier=lightbulb.OptionModifier.CONSUME_REST,
                  required=True)
@lightbulb.option("minutes",
                  "time to run the poll for(minutes)",
                  type=hikari.OptionType.INTEGER,
                  modifier=lightbulb.OptionModifier.CONSUME_REST,
                  required=True)
@lightbulb.option("hours",
                  "time to run the poll for(hours)",
                  type=hikari.OptionType.INTEGER,
                  modifier=lightbulb.OptionModifier.CONSUME_REST,
                  required=True)
@lightbulb.option("option_2",
                  "option 2",
                  type=hikari.OptionType.STRING,
                  modifier=lightbulb.OptionModifier.CONSUME_REST)
@lightbulb.option("option_1",
                  "option 1",
                  type=hikari.OptionType.STRING,
                  modifier=lightbulb.OptionModifier.CONSUME_REST)
@lightbulb.command("poll", "make a poll", auto_defer=True)
@lightbulb.implements(lightbulb.SlashCommand)
async def poll(ctx):
  #initialize variables
  channel = ctx.channel_id
  guild = str(ctx.guild_id)
  emoji_1 = ":one:"
  emoji_2 = ":two:"
  option_1 = str(ctx.options.option_1)
  option_2 = str(ctx.options.option_2)
  roles = await ctx.author.fetch_roles()
  permissions = hikari.Permissions.NONE
  for role in roles:
      permissions |= role.permissions
  #check if not admin
  if not (permissions & hikari.Permissions.ADMINISTRATOR) == hikari.Permissions.ADMINISTRATOR:
      embed = hikari.Embed(
          title="No perms",
          description=
          "Sorry - you don't have admin perms in the database. We do this to save processing power",
          color=embedColors.red)
      ctx.respond(embed)
      return
  #time variables
  minutes = (ctx.options.minutes) * 60

  hours = (ctx.options.hours) * 3600

  seconds = ctx.options.seconds

  time = seconds + minutes + hours
  #get embed
  embed = (hikari.Embed(
      title="Poll",
      description=f"{option_1}({emoji_1}) or {option_2}({emoji_2})",
      color=embedColors.blue)).set_author(name=ctx.author.username,
                                          icon=ctx.author.display_avatar_url)
  embed.add_field(
      "Open For:",
      f"{ctx.options.hours}:{ctx.options.minutes}:{ctx.options.seconds}")
  #send embed and store in a variable
  rp = await ctx.respond(embed)
  msg = await rp.message()
  one = await msg.add_reaction("1️⃣")
  two = await msg.add_reaction("2️⃣")
  #event.wait(time) #unused wait
  #get message id
  msg_id = msg.id
  
  timeToWait = time
  timeWaited = 0
  Seconds = ctx.options.seconds
  Minutes = ctx.options.minutes
  Hours = ctx.options.hours
  #while loop to let poll responses happen
  while (timeToWait > timeWaited):
      if Seconds <= 0 and Minutes > 0:
          Minutes -= 1
          Seconds = 59
      if Minutes <= 0 and Hours > 0:
          Hours -= 1
          Minutes = 59
      if Hours <= 0 and Minutes <= 0 and Seconds <= 0:
          #when poll is complete
          embed = (hikari.Embed(
          title="Poll",
          color=embedColors.blue,
          description=f"{option_1}({emoji_1}) or {option_2}({emoji_2})")).set_author(
              name=ctx.author.username, icon=ctx.author.display_avatar_url)
          
          embed.add_field("Poll Complete:", f"Results are below")
          await ctx.bot.rest.edit_message(channel=channel,
                                      message=msg_id,
                                      content=embed)
          break #break loop
      #reinitialize embed
      embed = (hikari.Embed(
          title="Poll",
          color=embedColors.blue,
          description=f"{option_1}({emoji_1}) or {option_2}({emoji_2})")).set_author(
              name=ctx.author.username, icon=ctx.author.display_avatar_url)
      embed.add_field("Open For:", f"{Hours}:{Minutes}:{Seconds}")
      embed.set_footer("**Adding other reactions will mess up the poll**")
      #edit message to update count
      await ctx.bot.rest.edit_message(channel=channel,
                                      message=msg_id,
                                      content=embed)
      Seconds = Seconds - 1
      event.wait(1)
  #fetch message object
  msg = await ctx.bot.rest.fetch_message(channel, msg)
  #get reactions list
  reaction = msg.reactions
  #get reaction counts
  oneCount = (reaction[0].count)-1
  twoCount = (reaction[1].count)-1

  #determine which one is greater
  if oneCount > twoCount:
      embed2 = hikari.Embed(title="Poll results",
                            color=embedColors.green,
                            description=f"{option_1} won!")
      embed2.add_field("Standings:", f"{oneCount} - {twoCount}")
      await bot.rest.create_message(channel, content=embed2)
  if oneCount < twoCount:
      embed = hikari.Embed(title="Poll results",
                           color=embedColors.green,
                           description=f"{option_2} won!")
      embed.add_field("Standings:", f"{oneCount} - {twoCount}")
      await bot.rest.create_message(channel, content=embed)
  #if tie  
  if oneCount == twoCount:
      embed = hikari.Embed(title="Poll Results",
                           color=embedColors.orange,
                           description=f"It's a tie!")
      embed.add_field("Standings:", f"{oneCount} - {twoCount}")
      await bot.rest.create_message(channel, content=embed)
  else: #uh oh

    embed = hikari.Embed(title="Error", color=embedColors.red, description="Something happened when retrieving the results")
    embed.add_field("Standings", f"{option_1}: {oneCount}\n{option_2}: {twoCount}")
    await bot.rest.create_message(channel, content=embed)

    
#basic ping command
@bot.command
@lightbulb.command("ping", "says pong", auto_defer=True)
@lightbulb.implements(lightbulb.SlashCommand)
async def ping(ctx):
    await ctx.respond("Pong!")

    
    

#uptime command
@bot.command
@lightbulb.command("uptime", "uptime", auto_defer=True)
@lightbulb.implements(lightbulb.SlashCommand)
async def uptime(ctx):
    #get now
    now = datetime.now()
    #calculate uptime
    uptime = now - startTime
    #make embed and send
    randC = randomColor()
    embed = hikari.Embed(title="Uptime",
                         description="Bot has been up for " + str(uptime),
                         color=randC)
    embed.set_footer("requested by " + str(ctx.author) + " | color: " +
                     randC)
    downIn = (startTime + timedelta(hours=6)) - now
    embed.add_field("Down in", f"The bot will go down in {downIn}")
    await ctx.respond(embed)


@bot.command
@lightbulb.option("rule",
                  "rule",
                  type=hikari.OptionType.STRING,
                  modifier=lightbulb.OptionModifier.CONSUME_REST)
@lightbulb.command("rule", "get a rule", auto_defer=True)
@lightbulb.implements(lightbulb.SlashCommand)
async def rule(ctx):
    #get now
    rule = ctx.options.rule
    #make embed and send
    embed = hikari.Embed(title="Rule #" + rule,
                         description="Quoting rule #" + rule +
                         " in <#942477754287411241>",
                         color=randomColor())
    try:
        embed.add_field("Rule " + rule, rules[rule])
    except Exception as e:
        embed.add_field("Rule not found.", "please enter a valid rule")
        embed.add_field("Error: ", e)
    embed.set_footer("requested by  <@" + str(ctx.author.id) + ">")
    await ctx.respond(embed)


#admin command for printing in this channel

##################### LOAD INTRODUCTION COMMANDS #####################


@bot.command
# if user can MANAGE CHANNELS then allow
@lightbulb.add_checks(lightbulb.checks.has_role_permissions(16))
#MANAGE_CHANNELS = 16
@lightbulb.option("channel",
                  "channel",
                  type=hikari.OptionType.CHANNEL,
                  modifier=lightbulb.OptionModifier.CONSUME_REST)
@lightbulb.command("setintrochannel",
                   "set the introduction channel",
                   ephemeral=True, auto_defer=True)
@lightbulb.implements(lightbulb.SlashCommand)
async def setintrochannel(ctx):
    channelID = ctx.options.channel.id
    #do something here
    embed = hikari.Embed(title="Introductions Channel",
                         description="Introductions Channel Set:")
    embed.add_field("Channel ID:", channelID)

    embed.set_footer("If this is wrong, run the command again")
    pushSettings(channelID, hasIntro, roleToAdd)
    await ctx.respond(embed)


@bot.command
@lightbulb.command("about", "show information about the bot", auto_defer=True)
@lightbulb.implements(lightbulb.SlashCommand)
async def about(ctx):
    randC = randomColor()
    embed = hikari.Embed(
        title="Miriad Bot",
        description="Miriad Bot is a bot created by  https://thedankboi.tk/ ",
        color=randC)
    embed.add_field("Version:", version)
    embed.set_footer("Requested by " + ctx.author.mention + " color: " + randC)
    await ctx.respond(embed)


@bot.command
@lightbulb.add_checks(lightbulb.checks.has_role_permissions(16))
@lightbulb.option("nointrorole",
                  "role for people who HAVE NOT done and introduction",
                  type=hikari.OptionType.ROLE,
                  modifier=lightbulb.OptionModifier.CONSUME_REST)
@lightbulb.option("introrole",
                  "role for people who HAVE done and introduction",
                  type=hikari.OptionType.ROLE,
                  modifier=lightbulb.OptionModifier.CONSUME_REST)
@lightbulb.command("setintrorole",
                   "the role for people who haven't done an intro",
                   ephemeral=True, auto_defer=True)
@lightbulb.implements(lightbulb.SlashCommand)
async def setintrorole(ctx):
    hasIntro = ctx.options.nointrorole.id
    roleToAdd = ctx.options.introrole.id
    hasIntroStr = str(hasIntro)
    embed = hikari.Embed(title="Set Role",
                         description="**successfully added roles**: *" +
                         hasIntroStr + "* and *" + str(roleToAdd) + '*')
    embed.add_field("Have Done An Introduction", ctx.options.introrole.mention)
    embed.add_field("Have *Not* Done An Introduction",
                    ctx.options.nointrorole.mention)
    embed.set_footer("If this is wrong, run the command again")
    pushSettings(channelID, hasIntro, roleToAdd)
    await ctx.respond(embed)
    #hikari.MessageFlag.EPHEMERAL)


@bot.command
#@lightbulb.add_checks.has_role(hasIntro)#if/ role has been added
#, lightbulb.checks.human_only
@lightbulb.add_checks(lightbulb.checks.human_only)
@lightbulb.option("description", "your intro description", required=True)
@lightbulb.option("name", "Your Name", required=True)
@lightbulb.option("age", "Your Age", required=False)
@lightbulb.option("sexuality", "Your Sexuality", required=False)
@lightbulb.option("pronouns", "Your Pronouns", required=True)
@lightbulb.option("likes", "Your Likes", required=False)
@lightbulb.option("dislikes", "Your Dislikes", required=False)
@lightbulb.option("randomfact", "A Random Fact", required=False)
@lightbulb.option("socials", "Your Socials", required=False)
@lightbulb.command(
    "makeintro",
    "make your introduction - leave blank if you dont want to have them",
    ephemeral=True, auto_defer=True)
@lightbulb.implements(lightbulb.SlashCommand)
async def makeIntro(ctx):
    user = ctx.author
    randC = randomColor()
    if not checkForAuthor(str(user.id)):
        embed = hikari.Embed(title="Introduction",
                             description=ctx.options.description,
                             color=embedColors.blue)
        embed.add_field("Name:", ctx.options.name)
        if not ctx.options.age == None:
            embed.add_field("Age:", ctx.options.age)
        if not ctx.options.sexuality == None:
            embed.add_field("Sexuality:", ctx.options.sexuality)
        if not ctx.options.pronouns == None:
            embed.add_field("Pronouns", ctx.options.pronouns)
        if not ctx.options.likes == None:
            embed.add_field("Likes", ctx.options.likes)
        if not ctx.options.dislikes == None:
            embed.add_field("Dislikes", ctx.options.dislikes)
        if not ctx.options.randomfact == None:
            embed.add_field("Random Fact", ctx.options.randomfact)
        if not ctx.options.socials == None:
            embed.add_field("Socials", ctx.options.socials)
        embed.set_author(
                name=ctx.author.username, icon=ctx.author.display_avatar_url)
        embed.set_footer("Run by " + str(ctx.author))

        try:
            await bot.rest.add_role_to_member(user=ctx.author,
                                              guild=ctx.guild_id,
                                              role=roleToAdd)
            await bot.rest.create_message(channelID, content=embed)
            embed = hikari.Embed(
                title="Success!",
                color = embedColors.blue,
                description="Successfully created message in channel " +
                str(channelID) + ".")
            writeToDoneRoles(str(user.id))
            await ctx.respond(embed)
        except Exception as e:
            embed = hikari.Embed(title="Error",
                                 color=embedColors.red,
                                 description="Error occured adding roles")
            embed.add_field(
                "Role Error",
                "Make sure I am **above** the desired role to add")
            #global globalErrorException
            globalErrorException = e
            row = bot.rest.build_action_row()
            button = row.add_button(hikari.ButtonStyle.PRIMARY, "seeerror")
            button.set_label("See Error Message")
            button.add_to_container()
            await ctx.respond(embed)
    else:
        embed = hikari.Embed(
            title="You've already done an introduction!",
            color=embedColors.red,
            description="Silly goose! You can't do one twice!")
        embed.set_footer("if you think this is a mistake, contact the admin")
        await ctx.respond(embed)


#####################   END INTRODUCTION COMMANDS  #####################
# me when when me when me when me when I when me #
##################### LOAD CREAMCOIN COMMANDS #####################

## ADMIN COMMANDS


# -- Run Bot -- #

#start web server
#keep_alive.keep_alive()
#try:
#  bot.run()
bot.run()
#except:
#  os.system("python main.py")
