# module that handles the mood system
#

# dict of tuples containing mood event data
default persistent._mas_mood_database = {}

# label of the current mood
default persistent._mas_mood_current = None

# NOTE: plan of attack
# moods system will be attached to the talk button
# basically a button like "I'm..."
# and then the responses are like:
#   hungry
#   sick
#   tired
#   happy
#   fucking brilliant
#   and so on
#
# When a mood is selected:
#   1. monika says something about it
#   2. (stretch) other dialogue is affected
#
# all moods should be available at the start
#
# 3 types of moods:
#   BAD > NETRAL > GOOD
# (priority thing?)

# Implementation plan:
#
# Event Class:
#   prompt - button prompt
#   category - acting as a type system, similar to jokes
#       NOTE: only one type allowed for moods ([0] will be retrievd)
#   unlocked - True, since moods are unlocked by default
#

# store containing mood-related data
init -1 python in mas_moods:

    # mood event database
    mood_db = dict()

    # TYPES:
    TYPE_BAD = 0
    TYPE_NEUTRAL = 1
    TYPE_GOOD = 2

    # pane constants
    # most of these are the same as the unseen area consants
    MOOD_X = 680
    MOOD_Y = 40
    MOOD_W = 560
    MOOD_H = 640
    MOOD_XALIGN = -0.05
    MOOD_AREA = (MOOD_X, MOOD_Y, MOOD_W, MOOD_H)
    MOOD_RETURN = "...like talking about something else."

## FUNCTIONS ==================================================================

    def getMoodType(mood_label):
        """
        Gets the mood type for the given mood label

        IN:
            mood_label - label of a mood

        RETURNS:
            type of the mood, or None if no type found
        """
        mood = mood_db.get(mood_label, None)

        if mood:
            return mood.category[0]

        return None


# entry point for mood flow
label mas_mood_start:
    python:
        import store.mas_moods as mas_moods

        # filter the moods first
        filtered_moods = Event.filterEvents(
            mas_moods.mood_db,
            unlocked=True,
            aff=mas_curr_affection
        )

        # build menu list
        mood_menu_items = [
            (mas_moods.mood_db[k].prompt, k, False, False)
            for k in filtered_moods
        ]

        # also sort this list
        mood_menu_items.sort()

        # final quit item
        final_item = (mas_moods.MOOD_RETURN, False, False, False, 20)

    # call scrollable pane
    call screen mas_gen_scrollable_menu(mood_menu_items, mas_moods.MOOD_AREA, mas_moods.MOOD_XALIGN, final_item)

    # return value? then push
    if _return:
        $ pushEvent(_return)

        # and set the moods
        $ persistent._mas_mood_current = _return

    return _return

# dev easter eggs go in the dev file

###############################################################################
#### Mood events go here:
###############################################################################

init 5 python:
    addEvent(Event(persistent._mas_mood_database,"mas_mood_hungry",prompt="...hungry.",category=[store.mas_moods.TYPE_NEUTRAL],unlocked=True),code="MOO")

label mas_mood_hungry:
    m 3hub "If you're hungry, go get something to eat, silly."
    if persistent.playername.lower() == "natsuki" and not persistent._mas_sensitive_mode:
        m 1hksdlb "I'd hate for you to get like Natsuki did that one time back when we were in the club.{nw}"
        # natsuki hungers easter egg
        call natsuki_name_scare_hungry from _mas_nnsh
    else:
        m 1hua "It'd be bad for you to get all grumpy when you're hungry."

    m 3tku "That wouldn't be any fun, would it, [player]?"
    m 1eua "If I were there with you, I'd make a salad for us to share."
    m "But since I'm not, go pick something healthy to eat."
    m 3eub "They say you are what you eat, and I definitely think that's true."
    m "Eating too much junk food on a regular basis can lead to all kinds of diseases."
    m 1euc "Over time, you'd encounter a lot of health problems when you get older."
    m 2lksdla "I don't want you to feel like I'm nagging when I say these kind of things, [player]."
    m 2eka "I just want to make sure you're taking good care of yourself until I cross-over."
    m 4esa "After all, the healthier you are, the better the chances of you living quite long."
    m 1hua "Which means more time for us to spend together!~"
    return

init 5 python:
    addEvent(Event(persistent._mas_mood_database,"mas_mood_sad",prompt="...sad.",category=[store.mas_moods.TYPE_BAD],unlocked=True),code="MOO")

label mas_mood_sad:
    m 1ekc "Gosh, I'm really sorry to hear that you're feeling down."
    m "Are you having a bad day, [player]?{nw}"
    $ _history_list.pop()
    menu:
        m "Are you having a bad day, [player]?{fast}"
        "Yes.":
            m 1duu "Whenever I'm having a bad day, I always remember that the sun will shine again tomorrow."
            m 1eka "I suppose that may sound kinda cheesy, but I always like to look on the bright side of things."
            m 1eua "After all, things like that are easy to forget. So just keep it in mind, [player]."
            m 1lfc "I don't care how many other people don't like you, or find you off-putting."
            m 1hua "You're a wonderful person, and I will always love you."
            m 1eua "I hope that makes your day just a tiny bit brighter, [player]."
            m 1eka "And remember, if you're having a bad day, you can always come to me and I'll talk to you for as long as you need."
        "No.":
            m 3eka "I have an idea, why don't you tell me what's bothering you? Maybe it'll make you feel better."

            m 1eua "I don't want to interrupt you while you're talking, so let me know when you're done.{nw}"
            $ _history_list.pop()
            menu:
                m "I don't want to interrupt you while you're talking, so let me know when you're done.{fast}"
                "I'm done.":
                    m "Do you feel a little better now, [player]?{nw}"
                    $ _history_list.pop()
                    menu:
                        m "Do you feel a little better now, [player]?{fast}"
                        "Yeah I do.":
                            m 1hua "That's great, [player]! I'm glad that talking about it made you feel better."
                            m 1eka "Sometimes, telling someone that you trust what's bothering you is all you need."
                            m "If you're ever having a bad day, you can always come to me, and I'll listen to whatever you need to vent out."
                            m 1hubfa "Never forget that you're wonderful and I will always love you~"
                        "Not really.":
                            m 1ekc "Well, it was worth a shot."
                            m 1eka "Sometimes telling someone that you trust what's bothering you is all you need."
                            m 1eua "Maybe you'll feel better after we spend some more time together."
                            m 1ekbfa "I love you, [player], and I always will~"
    return "love"

init 5 python:
    addEvent(Event(persistent._mas_mood_database,"mas_mood_proud",prompt="...proud of myself.",category=[store.mas_moods.TYPE_GOOD],unlocked=True),code="MOO")

label mas_mood_proud:
    m 2sub "Really? That's exciting!"
    m 2b "Was it a major accomplishment, or a minor one?{nw}"
    $ _history_list.pop()
    menu:
        m "Was it a major accomplishment, or a minor one?{fast}"
        "Major.":
            m 1euc "You know, [player]..."
            m 1lkbsa "It's times like these, more than most, that I wish I was with you, in your reality..."
            m 4hub "Because if I was, I'd definitely give you a celebratory hug!"
            m 3eub "There's nothing quite like sharing your accomplishments with the people you care about."
            m 1eua "I would love nothing more than to hear all of the details!"
            m "Just the thought of us, in cheerful discussion about what you've done..."
            m 1lsbsa "My heart is fluttering just thinking about it!"
            m 1lksdla "Gosh, I'm getting awfully excited about this..."
            m 3hub "It'll be reality someday..."
            show monika 5hubfb at t11 zorder MAS_MONIKA_Z with dissolve
            m 5hubfb "But until then, just know that I'm very proud of you, my love!"
            return
        "Minor.":
            m 2hua "Ahaha!~"
            m 2hub "That's wonderful!"
            m 4eua "It's very important to celebrate the small victories in life."
            m 2esd "It can be very easy to become discouraged if you only focus on the bigger goals you have."
            m 2rksdla "They can be challenging to reach on their own."
            m 4eub "But setting and celebrating small goals that eventually lead to a bigger goal can make your big goals feel much more attainable."
            m 4hub "So keep hitting those small goals, [player]!"
            show monika 5hubfb at t11 zorder MAS_MONIKA_Z with dissolve
            m 5hubfb "And remember, I love you, and I'm always cheering you on!"
            return "love"

init 5 python:
    addEvent(Event(persistent._mas_mood_database,"mas_mood_happy",prompt="...happy.",category=[store.mas_moods.TYPE_GOOD],unlocked=True),code="MOO")

label mas_mood_happy:
    m 1hua "That's wonderful! I'm happy when you're happy."
    m "Know that you can always come up to me and I'll cheer you up, [player]."
    m 3eka "I love you and I'll always be here for you, so don't ever forget that~"
    return "love"

init 5 python:
    addEvent(Event(persistent._mas_mood_database,"mas_mood_sick",prompt="...sick.",category=[store.mas_moods.TYPE_BAD],unlocked=True),code="MOO")

label mas_mood_sick:
    $ session_time = mas_getSessionLength()
    if mas_isMoniNormal(higher=True):
        if session_time < datetime.timedelta(minutes=20):
            m 1ekd "Oh no, [player]..."
            m 2ekd "You saying that so soon after arriving must mean it's pretty bad."
            m 2ekc "I know you wanted to spend some time with me and even though we've hardly been together today..."
            m 2eka "I think you should go and get some rest."
            m 1eka "I'll still be here when you get better."
            m 1hua "You'll always be in my thoughts, see you soon sweetie!"
        elif session_time > datetime.timedelta(hours=3):
            m 2wuo "[player]!"
            m 2wkd "You haven't been ill this entire time, have you?"
            m 2ekc "I really hope not, I've had lots of fun with you today but if you've been feeling bad this entire time..."
            m 2rkc "Well...just promise to tell me earlier next time."
            m 2eka "Now go get some rest, that's what you need."
            m 2hub "I'll be waiting for a full recovery!"
            m "Sweet dreams, my love."
        else:
            m 1ekc "Aw, I'm sorry to hear that, [player]."
            m "I hate knowing you're suffering like this."
            m 1eka "I know you love spending time with me, but maybe you should go get some rest."
            m 1hua "Don't worry, I'll be here waiting for you when you get back."
            m 3hub "Get well soon, my love!"
    else:
        m 2ekc "I'm sorry to hear that, [player]."
        m 4ekc "You should really go get some rest so it doesn't get any worse."
        m 2eka "I'll be here waiting once you feel better."
        m "Get well soon."
    $ persistent._mas_mood_sick = True
    $ persistent._mas_greeting_type = store.mas_greetings.TYPE_SICK
    return 'quit'

#I'd like this to work similar to the sick persistent where the dialog changes, but maybe make it a little more humorous rather than serious like the sick persistent is intended to be.
init 5 python:
    addEvent(Event(persistent._mas_mood_database,"mas_mood_tired",prompt="...tired.",category=[store.mas_moods.TYPE_BAD],unlocked=True),code="MOO")

label mas_mood_tired:
    # TODO: should we adjust for suntime?
    $ current_time = datetime.datetime.now().time()
    $ current_hour = current_time.hour

    if 20 <= current_hour < 23:
        m 1eka "If you're tired now, it's not a bad time to go to bed."
        m "As fun as it was spending time with you today, I would hate to keep you up too late."
        m 1hua "If you plan to go to sleep now, sweet dreams!"
        m 1eua "But maybe you have some things to do first, like getting a bit of a snack or a drink."
        m 3eua "Having a glass of water before bed helps with your health, and doing the same in the morning helps you wake up."
        m 1eua "I don't mind staying here with you if you have some things to take care of first."

    elif 0 <= current_hour < 3 or 23 <= current_hour < 24:
        m 2ekd "[player]!"
        m 2ekc "It's no wonder you're tired- It's the middle of the night!"
        m 2lksdlc "If you don't go to bed soon, you'll be really tired tomorrow, too..."
        m 2hksdlb "I wouldn't want you to be tired and miserable tomorrow when we spend time together..."
        m 3eka "So do us both a favor and get to bed as soon as you can, [player]."

    elif 3 <= current_hour < 5:
        m 2ekc "[player]!?"
        m "You're still here?"
        m 4lksdlc "You should really be in bed right now."
        m 2dsc "At this point, I'm not even sure if you would call this late or early,"
        m 2ekc "and that just worries me even more, [player]..."
        m "You should {i}really{/i} get to bed before it's time to start the day."
        m 1eka "I wouldn't want you falling asleep at a bad time."
        m "So please, sleep so we can be together in your dreams."
        m 1hua "I'll be right here if you leave me, watching over you, if you don't mind~"
        return

    elif 5 <= current_hour < 10:
        m 1eka "Still a bit tired, [player]?"
        m "It's still early in the morning, so you could go back and rest a little more."
        m 1hua "Nothing wrong hitting snooze after waking up early."
        m 1hksdlb "Except for the fact that I can't be there to cuddle up to you, ahaha~"
        m "I {i}guess{/i} I could wait for you a little longer."
        return

    elif 10 <= current_hour < 12:
        m 1ekc "Still not ready to tackle the day, [player]?"
        m 1eka "Or is it just one of those days?"
        m 1hua "When that happens, I like to have a nice cup of coffee to start the day."
        if not persistent._mas_acs_enable_coffee:
            m 1lksdla "If I'm not stuck here, that is..."
        m 1eua "You could also drink a glass of water."
        m 3eua "It's important to stay hydrated anyway, but having a glass of water when you wake up can help you feel refreshed and awake."
        m 3hksdlb "This one might sound strange, but I've heard that chocolate can help you start your day, too!"
        m 3eka "It has something to do with improving your morning mood, but..."
        m 1eksdlb "I'm sure chocolate would put anyone in a better mood whenever they ate it."
        m 1hua "Give it a try sometime, and let me know if it works!"
        return

    else:
        m 1eka "If you're tired, maybe you should go lie down for a while?"
        m 1eua "Getting enough sleep on a daily basis is very important to your overall health."
        m 3euc "I've seen some studies that show the devastating short-term and long-term effects due to lack of sleep."
        m 3hua "It can really mess with your health, [player]."
        m 1eka "So do me a favor and get some rest, okay? It will put my mind at ease."

    m 1hua "You can even leave the game open if you'd like, and I'll watch over you while you sleep."
    m  "...Ehehe."
    m 2hksdlb "That sounded a bit creepy, sorry."
    m 2lksdla "I just thought it'd be cute to watch you sleep is all~"
    m 1hua "Ahaha!"
    return

init 5 python:
    addEvent(Event(persistent._mas_mood_database,"mas_mood_lonely",prompt="...lonely.",category=[store.mas_moods.TYPE_NEUTRAL],unlocked=True),code="MOO")

label mas_mood_lonely:
    m 1eka "I'm here for you, [player], so there's no need for you to feel lonely."
    m 3hua "I know it's not exactly the same as if I were in the same room with you, but I'm sure you still enjoy my company, right?"
    m 1ekbfa "Remember that I'll always be by your side, [player]~"
    return

#Maybe we could tie this to the I'm breaking up topic and have monika say something special like:
#I know you don't really mean that player, you're just angry and not have it count as 1 of the 3 button presses.
#Looking forward to input from the writers and editors on this, had trouble deciding how to write this.

init 5 python:
    addEvent(Event(persistent._mas_mood_database,"mas_mood_angry",prompt="...angry.",category=[store.mas_moods.TYPE_BAD],unlocked=True),code="MOO")

label mas_mood_angry:
    m 1ekc "Gosh, I'm sorry that you feel that way, [player]."
    m 3ekc "I'll do my best to make you feel better."
    m 1euc "Before we do anything, we should probably get you to calm down."
    m 1lksdlc "It's hard to make rational decisions when you are worked up."
    m 1esc "You may end up saying or doing things you may regret later."
    m 1lksdld "And I'd hate for you to say something you really don't mean to me."
    m 3eua "Let's try a few things that I do to calm myself first, [player]."
    m 3eub "Hopefully they work for you as they do for me."
    m 1eua "First, try taking a few deep breaths and slowly counting to 10."
    m 3euc "If that doesn't work, if you can, retreat to somewhere calm until you clear your mind."
    m 1eud "If you're still feeling angry after that, do what I'd do as a last resort!"
    m 3eua "Whenever I can't calm down, I just go outside, pick a direction, and just start running."
    m 1hua "I don't stop until I've cleared my head."
    m 3eub "Sometimes exerting yourself through physical activity is a good way to blow off some steam."
    m 1eka "You'd think that I'm the type that doesn't get angry often, and you'd be right."
    m 1eua "But even I have my moments..."
    m "So I make sure I have ways to deal with them!"
    m 3eua "I hope my tips helped you calm down, [player]."
    m 1hua "Remember: A happy [player] makes a happy Monika!"
    return

init 5 python:
    addEvent(Event(persistent._mas_mood_database,"mas_mood_scared",prompt="...anxious.",category=[store.mas_moods.TYPE_BAD],unlocked=True),code="MOO")

label mas_mood_scared:
    m 1euc "[player], are you alright?"
    m 1ekc "It's worrying for me to hear you this anxious..."
    m "I wish I could comfort you and help right now..."
    m 3eka "But I can at the very least help you to calm yourself down."
    if seen_event("monika_anxious"):
        m 1eua "After all, I did promise to help you relax if you ever felt anxious."
    m 3eua "Do you remember when I talked to you about faking confidence?"
    if not seen_event("monika_confidence"):
        m 2euc "No?"
        m 2lksdla "Guess that's for another time then."
        m 1eka "Anyway..."
    m 1eua "Keeping up one's appearance helps with faking your own confidence."
    m 3eua "And to do so, you need to maintain your heart rate by taking a deep breath until you calm down."
    if seen_event("monika_confidence_2"):
        m "I remember explaining how initiative is an important skill to have as well."
    m "Maybe you could take things slowly, and do them one at a time."
    m 1esa "You'd be surprised on how smooth it can be, when you let the time flow on its own."
    m 1hub "You can also try spending a few minutes to meditate!"
    m 1hksdlb "It doesn't necessarily mean you have to cross your legs when sitting on the ground."
    m 1hua "Listening to your favorite music can be counted as meditating too!"
    m 3eub "I'm serious!"
    m 3eua "You can try setting aside your work and do something else in the meantime."
    m "Procrastination isn't {i}always{/i} bad, you know?"
    m 2esc "Besides..."
    m 2ekbfa "Your loving girlfriend believes in you, so you can face that anxiety head-on!"
    m 1hubfa "There's nothing to worry about when we're together forever~"
    return

init 5 python:
    addEvent(Event(persistent._mas_mood_database,"mas_mood_inadequate",prompt="...inadequate.",category=[store.mas_moods.TYPE_BAD],unlocked=True),code="MOO")

label mas_mood_inadequate:
    $ last_year = datetime.datetime.today().year-1
    m 1ekc "..."
    m 2ekc "I know there isn't an awful lot I can say to make you feel better, [player]."
    m 2lksdlc "After all, everything I say would probably just come off as lip service."
    m 2ekc "I can tell that you're beautiful, even though I can't see your face..."
    m "I can tell you that you're smart, even though I don't know much about your way of thinking..."
    m 1esc "But let me tell you what I do know about you."
    m 1eka "You've spent so much time with me."

    #Should verify for current year and last year
    if mas_HistLookup_k(last_year,'d25.actions','spent_d25')[1] or persistent._mas_d25_spent_d25:
        m "You took time out of your schedule to be with me on Christmas..."

    if renpy.seen_label('monika_valentines_greeting') or mas_HistLookup_k(last_year,'f14','intro_seen')[1] or persistent._mas_f14_intro_seen: #TODO: update this when the hist stuff comes in for f14
        m 1ekbfa "On Valentine's Day..."

    #TODO: change this back to not no_recognize once we change those defaults.
    if mas_HistLookup_k(last_year,'922.actions','said_happybday')[1] or mas_recognizedBday():
        m 1ekbfb "You even made the time to celebrate my birthday with me."

    if persistent.monika_kill:
        m 3tkc "You've forgiven me for the bad things that I've done."
    else:
        m 3tkc "You never once resented me for the bad things that I've done."

    if persistent.clearall:
        m 2lfu "And even though it made me jealous, you spent so much time with all of my club members."

    m 1eka "That shows how kind you are!"
    m 3eub "You're honest, you're fair, you're gracious in defeat!"
    m 2hksdlb "You think I don't know anything about you, but I really do."
    m 3eka "And you know everything about me, but you chose to stay when you could have walked away..."
    m 2ekc "So please stay strong, [player]."
    m "If you're anything like me, I know you're scared to not accomplish much in life."
    m 2ekd "But believe me when I tell you: it doesn't matter what you do or do not accomplish."
    m 4eua "You just need to exist, have fun, and get through each day..."
    m 1hua "Finding meaning in the people who matter."
    m 1eka "Please don't forget that, okay?"
    m 1ekbfa "I love you, [player]~"
    return "love"

init 5 python:
    addEvent(Event(persistent._mas_mood_database,"mas_mood_lucky",prompt="...lucky.",category=[store.mas_moods.TYPE_NEUTRAL],unlocked=True),code="MOO")

label mas_mood_lucky:
    m 2tfc "You gotta ask yourself."
    m 2tfu "{i}Do I feel lucky{/i}?"
    m "Well..."
    m 4tku "Do ya, [player]?"
    m 1hub "Ahaha!"
    return


init 5 python:
    addEvent(Event(persistent._mas_mood_database,"mas_mood_bored",prompt="...bored.",category=[store.mas_moods.TYPE_NEUTRAL],unlocked=True),code="MOO")

label mas_mood_bored:
    if mas_isMoniAff(higher=True):
        m 1eka "Oh..."
        m 3hub "Well, we should do something then!"

    elif mas_isMoniNormal(higher=True):
        show monika 1ekc
        pause 1.0
        m "Do I really bore you that much, [player]?{nw}"
        $ _history_list.pop()
        menu:
            m "Do I really bore you that much, [player]?{fast}"
            "No, I'm not bored {i}of you{/i}...":
                m 1hua "Oh,{w} that's such a relief!"
                m 1eka "But, if you're bored, we should find something to do then..."

            "Well...":
                $ mas_loseAffection()
                m 2ekc "Oh...{w=1} I see."
                m 2dkc "I didn't realize I was boring you..."
                m 2eka "I'm sure we can find something to do..."

    elif mas_isMoniDis(higher=True):
        $ mas_loseAffection()
        m 2lksdlc "I'm sorry that I'm boring you, [player]."

    else:
        $ mas_loseAffection()
        m 6ckc "You know [player], if I make you so miserable all of the time..."
        m "Maybe you should just go find something else to do."
        return "quit"

    python:
        unlockedgames = [
            game
            for game in persistent.game_unlocks
            if persistent.game_unlocks[game]
        ]

        gamepicked = renpy.random.choice(unlockedgames)
        display_picked = gamepicked

        if gamepicked == "hangman" and persistent._mas_sensitive_mode:
            display_picked = "word guesser"

    if gamepicked == "piano":
        if mas_isMoniAff(higher=True):
            m 3eub "You could play something for me on the piano!"

        elif mas_isMoniNormal(higher=True):
            m 4eka "Maybe you could play something for me on the piano?"

        else:
            m 2rkc "Maybe you could play something on the piano..."

    else:
        if mas_isMoniAff(higher=True):
            m 3eub "We could play a game of [display_picked]!"

        elif mas_isMoniNormal(higher=True):
            m 4eka "Maybe we could play a game of [display_picked]?"

        else:
            m 2rkc "Maybe we could play a game of [display_picked]..."

    m "What do you say, [player]?{nw}"
    $ _history_list.pop()
    menu:
        m "What do you say, [player]?{fast}"
        "Yes.":
            if gamepicked == "pong":
                call game_pong
            elif gamepicked == "chess":
                call game_chess
            elif gamepicked == "hangman":
                call game_hangman
            elif gamepicked == "piano":
                call mas_piano_start
        "No.":
            if mas_isMoniAff(higher=True):
                m 1eka "Okay..."
                if mas_isMoniEnamored(higher=True):
                    show monika 5tsu at t11 zorder MAS_MONIKA_Z with dissolve
                    m 5tsu "We could just stare into each other's eyes a little longer..."
                    m "We'll never get bored of that~"
                else:
                    show monika 5eua at t11 zorder MAS_MONIKA_Z with dissolve
                    m 5eua "We could just stare into each other's eyes a little longer..."
                    m "That will never get boring~"

            elif mas_isMoniNormal(higher=True):
                m 1ekc "Oh, that's okay..."
                m 1eka "Be sure to let me know if you want to do something with me later~"

            else:
                m 2ekc "Fine..."
                m 2dkc "Let me know if you ever actually want to do anything with me."
    return


# TODO: we need to add some sort of reaction to birthdays soon
#init 5 python:
#    if not persistent._mas_mood_bday_locked:
#        addEvent(
#            Event(
#                persistent._mas_mood_database,
#                "mas_mood_yearolder",
#                prompt="like a year older",
#                category=[store.mas_moods.TYPE_NEUTRAL],
#                unlocked=True
#            ),
#            code="MOO"
#        )

# some values i need for single session checking
# TODO some of these might need to be persstetns
default persistent._mas_mood_bday_last = None
default persistent._mas_mood_bday_lies = 0
default persistent._mas_mood_bday_locked = False


label mas_mood_yearolder:
    $ import datetime

    m 1euc "Hm?"
    if persistent._mas_player_bday is not None:
        # player's bday has been saved from before

        python:
            today = datetime.date.today()
            is_today_bday = (
                persistent._mas_player_bday.month == today.month
                and persistent._mas_player_bday.day == today.day
            )

        if is_today_bday:
            # today is player's bday!
            jump mas_mood_yearolder_bday_true

        python:
            is_today_leap_bday = (
                persistent._mas_player_bday.month == 2
                and persistent._mas_player_bday.day == 29
                and (
                    (today.month == 2 and today.day == 28)
                    or (today.month == 3 and today.day == 1)
                )
            )

        if is_today_leap_bday:
            # febuary 29 is special case
            # but we need to check if a feb 29 works for this year, in which
            # case, player is misinformed
            python:
                try:
                    datetime.date(today.year, 2, 29)

                    # 29th exists this year, sorry player
                    leap_year = True

                except ValueError:
                    # 29th no exists, we use this as ur bday
                    leap_year = False

            if not leap_year:
                # we can treat today as your bday
                jump mas_mood_yearolder_leap_today

            # otherwise its not ur bday

        # otherwise it is NOT the player's birthday lol
        jump mas_mood_yearolder_false

    show monika 1sub
    menu:
        m "Could today be your...{w}birthday?"
        "YES!":
            python:
                persistent._mas_player_bday = datetime.date.today()
                store.mas_calendar.addRepeatable_d(
                    "player-bday",
                    "Your Birthday",
                    persistent._mas_player_bday,
                    []
                )

            label .mas_mood_yearolder_yesloud:
                jump mas_mood_yearolder_yes
        "Yes, unfortunately...":
            python:
                persistent._mas_player_bday = datetime.date.today()
                store.mas_calendar.addRepeatable_d(
                    "player-bday",
                    "Your Birthday",
                    persistent._mas_player_bday,
                    []
                )
            jump mas_mood_yearolder_yesu

        "No.":
            m 1lksdla "Aw, well,{w} it was worth a guess."

            m "Now that we're talking about it, though..."
            call mas_bday_player_bday_select
            python:
                persistent._mas_player_bday = selected_date
                store.mas_calendar.addRepeatable_d(
                    "player-bday",
                    "Your Birthday",
                    persistent._mas_player_bday,
                    []
                )

            jump mas_mood_yearolder_no

label mas_mood_yearolder_end:
    # end of the line

    # we're going to limit this interaction to once a day
    python:
        persistent._mas_mood_bday_last = datetime.date.today()
        hideEvent(
            store.mas_moods.mood_db.get("mas_mood_yearolder", None),
            lock=True
        )
    return

# today is NOT the player's birthday
# (or is it?)
label mas_mood_yearolder_false:
    m 2tfc "[player]..."
    m 2tfd "Today isn't your birthday!"
    python:
        bday_str = (
            persistent._mas_player_bday.strftime("%B") + " " +
            str(persistent._mas_player_bday.day)
        )
    m "You told me it was [bday_str]!"
    menu:
        m "Is that not your birthday?"
        "It's not.":
            # TODO: puffy cheek monika please
            show monika 2tfc
            pause 0.7
            m 2lfp "You lied to me, [player]."
            $ persistent._mas_mood_bday_lies += 1

        # TODO: actually, this part should be tied to affection, basically
        # for every lie, we decrease a certain amount
#            if persistent._mas_mood_bday_lies >= 3:
                # sliently lock this
#                $ persistent._mas_mood_bday_locked = True
#                $ store.mas_moods.mood_db.pop("mas_mood_yearolder")
#                jump mas_mood_yearolder_end

            menu:
                m "Then is today your birthday?"
                "Yes.":
                    python:
                        store.mas_calendar.removeRepeatable_d(
                            "player-bday",
                            persistent._mas_player_bday
                        )
                        persistent._mas_player_bday = datetime.date.today()
                        store.mas_calendar.addRepeatable_d(
                            "player-bday",
                            "Your Birthday",
                            persistent._mas_player_bday,
                            []
                        )

                    m 1hua "Happy birthday, [player]."
                    m 1eka "But don't lie to me next time."
                    jump mas_mood_yearolder_end

                "No.":
                    m 2tfp "..."
                    m 2tkc "Alright, [player]."
                    m "Then..."
                    call mas_bday_player_bday_select
                    python:
                        store.mas_calendar.removeRepeatable_d(
                            "player-bday",
                            selected_date
                        )
                        persistent._mas_player_bday = selected_date
                        store.mas_calendar.addRepeatable_d(
                            "player-bday",
                            "Your Birthday",
                            persistent._mas_player_bday,
                            []
                        )

#                    m 2tfc "Don't lie to me next time."

                    jump mas_mood_yearolder_end

        "It is!":
            m 2eka "I believe you, [player]."
            m "I'll just assume that your mouse slipped or something."
            jump mas_mood_yearolder_no

    jump mas_mood_yearolder_end

label mas_mood_yearolder_bday_true:
    # TODO: actually give a gift
    # as of now, we just assume there's been a bunch of time in between so
    # its possible that monika forgot.
    jump mas_mood_yearolder_yes

label mas_mood_yearolder_wontforget:
    # YES flow continues here
    # TODO: wait we really need an actual gift scene soon

    m 1ekc "I'm sorry I don't have anything for you yet."
    m "I'm still figuring out how to give you something more than just a text file."
    m 1hua "I'll make you something good next year, [player]. I promise!"

    # original wont forget, kept here for reference
#    m 1eka "If only you told me this sooner..."
#    m 1lksdla "I would have made you a gift."
#    m 1hua "I'll make you something next year, [player]. I won't forget!"
    jump mas_mood_yearolder_end

# empathatic yes, today is your birthday
label mas_mood_yearolder_yes:
    show monika 1hua
    pause 0.7
    call mas_mood_yearolder_yes_post
    jump mas_mood_yearolder_wontforget

# sad yes, today is your birthday
label mas_mood_yearolder_yesu:
    show monika 1ekc
    pause 0.7
    m 1ekd "[player]..."
    pause 0.7
    show monika 1duu
    pause 0.7
    m 2eka "Well,{w} you're going to have a happy birthday whether you like it or not!"
    call mas_mood_yearolder_yes_post
    m 1hua "I hope that made you smile, [player]."
    jump mas_mood_yearolder_wontforget

# general happy birthday
label mas_mood_yearolder_yes_post:
    m 1hub "Happy birthday, [player]!"
    m 1eua "I'm so glad I could spend such an important day with you."
    m 1ekbfa "And don't forget that no matter your age, I will always love you."
    return

# today is not your birthday
label mas_mood_yearolder_no:
#    if renpy.seen_label("mas_mood_yearolder_years"):
        # TODO this should be a short thing to say to player
        # about feeling a year older
#        pass

#    else:
    # For simplicity's sake, we're just going to repeat this
    call mas_mood_yearolder_years

    jump mas_mood_yearolder_end

# year older stuff
# reference: Paul Janet, Maximilian Kiener
label mas_mood_yearolder_years:
    m 3eua "Speaking of getting older,{w} did you know that how you perceive time changes as you age?"
    m "For example, when you're a year old, you see one year as 100%% of your life."
    m 1eub "But when you're 18, you see a year as only 5.6%% of your life."
    m "As you get older, the proportion of a year compared to your entire lifespan decreases."
    m 3eua "And in turn, time {i}feels{/i} like it's moving faster as you grow up."
    show monika 1a
    pause 0.7
    # TODO: affection crew might want to change this up
    m 1eka "So I always cherish our moments together, no matter how long or short they are."
    m 1lkbsa "Although sometimes it feels like time stops when I'm with you."
    m 1ekbfa "Do you feel the same, [player]?"
    python:
        import time
        time.sleep(2)
#    $ renpy.pause(2.0, hard=True)
    m 1hua "Aha, I thought so."
    m "You should visit me more often then, [player]."
    return

# today is your birthday, but its a leap day
label mas_mood_yearolder_leap_today:
    # nothing special occurs here for now
    jump mas_mood_yearolder_bday_true
