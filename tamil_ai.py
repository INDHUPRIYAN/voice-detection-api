import asyncio
import edge_tts
import os
import random

OUTPUT_DIR = "dataset/ai_tamil_colloquial"
os.makedirs(OUTPUT_DIR, exist_ok=True)

VOICES = ["ta-IN-PallaviNeural", "ta-IN-ValluvarNeural"]

TEXTS = [
"""இன்று ரொம்ப tired ஆகிட்டேன் டா.
office ல வேலை ரொம்ப ஜாஸ்தி.
home வந்ததும் straight ah தூங்கணும் போல இருக்கு.
weekend எப்போ வரும் தெரியல.""",

"""சாப்பிடலையா இன்னும்?
நான் already order பண்ணிட்டேன்.
delivery வரத்தான் late ஆகுது.
ரொம்ப பசிக்குது டா honestly.""",

"""நேத்து படம் பாத்தியா?
climax செம்ம twist இருந்துச்சு.
எல்லாரும் theatre ல shock ஆயிட்டாங்க.
நான் expect கூட பண்ணல.""",

"""மழை வர மாதிரி இருக்கு போல.
clothes எல்லாம் வெளியே தான் இருக்கு.
போய் எடுத்து வைக்கணும் இல்லனா நனைஞ்சிடும்.
weather ரொம்ப unpredictable ஆயிடுச்சு.""",

"""childhood நினைச்சா ரொம்ப feel ஆகுது.
friends கூட சின்ன சின்ன விஷயத்துக்கு laugh பண்ணுவோம்.
இப்போ எல்லாரும் busy ஆயிட்டாங்க.
time ரொம்ப fast ah போகுது.""",

"""என்னடா plan இன்றைக்கு?
movie போவோமா இல்ல வெளியே சாப்பிடலாமா?
எனக்கு change வேணும் போல இருக்கு.
full week work பண்ணி bore ஆயிட்டேன்.""",

"""morning லே alarm கேட்டே கேக்கல.
last minute ல தான் எழுந்தேன்.
office க்கு almost late ஆயிட்டேன்.
traffic வேற செம problem.""",

"""phone battery எப்போமே low தான்.
charger எடுத்துட்டு போக மறந்துட்டேன்.
power bank கூட இல்ல.
ippo full tension ah இருக்கு.""",

"""இந்த song கேட்கும் போது memories வருது.
college days ரொம்ப miss பண்றேன்.
friends கூட spent பண்ணின time priceless.
life simple ah இருந்துச்சு அப்போ.""",

"""weekend வந்தா தான் relief feel ஆகுது.
late ah தூங்கலாம்.
family கூட time spend பண்ணலாம்.
அதுவே biggest happiness.""",

"""travel பண்ணணும் போல இருக்கு டா.
same routine bore அடிக்குது.
new place போனா mind fresh ஆகும்.
budget set பண்ணணும் first.""",

"""meeting ல boss semma serious ah இருந்தார்.
எல்லாரும் silent ஆகிட்டாங்க.
ஒரு joke கூட crack பண்ண முடியல.
atmosphere romba tight.""",

"""gym போகணும் நினைச்சு தான் இருக்கேன்.
ஆனா motivation வரவே இல்ல.
daily tomorrow tomorrow nu postpone ஆகுது.
fitness important nu தெரியும்.""",

"""internet slow ஆ இருந்தா patience போயிடுது.
video buffer ஆகிட்டு தான் இருக்கு.
work complete பண்ண முடியல.
frustration level high.""",

"""old photos பாத்தா memories flood ஆகுது.
அந்த days திரும்ப வந்தா நல்லா இருக்கும்.
stress இல்லாம happy ah இருந்தோம்.
life simple ah இருந்துச்சு.""",

"""friends sudden ah surprise பண்ணினாங்க.
cake வாங்கி வந்திருந்தாங்க.
expect கூட பண்ணல honestly.
romba emotional ஆயிட்டேன்.""",

"""late night drive போனா mind relax ஆகுது.
songs கேட்டு peaceful ah feel ஆகும்.
traffic இல்லாம road calm ah இருக்கும்.
அந்த vibe வேற level.""",

"""shopping போனா budget exceed ஆயிடுது.
offer பாத்தா control போயிடுது.
later தான் regret வரும்.
ஆனா வாங்கும் போது happy.""",

"""work pressure அதிகமா இருந்தாலும்,
சின்ன achievements motivate பண்ணுது.
step by step progress important.
confidence slowly build ஆகுது.""",

"""future பற்றி யோசிச்சா கொஞ்சம் பயமா இருக்கு.
ஆனா hope இருந்தா everything possible.
effort போடுறதுக்கு ready தான்.
life எதுக்கு கொண்டு போகுது பார்ப்போம்."""
]

async def generate():
    for i in range(20):
        success = False
        while not success:
            try:
                voice = random.choice(VOICES)
                text = random.choice(TEXTS)

                filename = f"{OUTPUT_DIR}/ta_colloquial_{i+1}.mp3"

                communicate = edge_tts.Communicate(
                    text=text,
                    voice=voice,
                    rate=random.choice(["-5%", "+0%", "+5%"]),
                    pitch=random.choice(["-5Hz", "+0Hz", "+5Hz"])
                )

                await communicate.save(filename)
                print("Saved:", filename)
                success = True

            except Exception as e:
                print("Retrying:", e)
                await asyncio.sleep(1)

asyncio.run(generate())
print("✅ Colloquial Tamil dataset ready!")
