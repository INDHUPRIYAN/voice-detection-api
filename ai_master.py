import asyncio
import edge_tts
import os
import random

OUTPUT_DIR = "dataset/ai_master"
os.makedirs(OUTPUT_DIR, exist_ok=True)

VOICE_MAP = {
    "en": [
        "en-US-GuyNeural","en-US-JennyNeural","en-US-AriaNeural",
        "en-US-DavisNeural","en-US-AmberNeural","en-US-BrandonNeural",
        "en-US-ChristopherNeural","en-US-CoraNeural","en-US-ElizabethNeural",
        "en-US-EricNeural","en-GB-RyanNeural","en-GB-SoniaNeural",
        "en-GB-LibbyNeural","en-GB-MaisieNeural"
    ],
    "ta": ["ta-IN-PallaviNeural","ta-IN-ValluvarNeural"],
    "hi": ["hi-IN-MadhurNeural","hi-IN-SwaraNeural"],
    "ml": ["ml-IN-SobhanaNeural","ml-IN-MidhunNeural"],
    "te": ["te-IN-ShrutiNeural","te-IN-MohanNeural"]
}

TEXTS = {
    "en": [
        """Life is a journey filled with emotions and experiences.
        Every challenge teaches us something valuable.
        Spending time with loved ones brings happiness and peace.
        These moments shape our memories forever.""",

        """Sometimes we feel excited about the future.
        Other times we reflect on past decisions.
        Growth happens when we accept both success and failure.
        That balance helps us become stronger.""",

        """Listening to music can change our mood instantly.
        Conversations with friends bring comfort.
        Even simple walks in nature refresh the mind.
        Peace often comes from small daily moments."""
    ],

    "ta": [
        """வாழ்க்கை உணர்ச்சிகளால் நிரம்பிய ஒரு பயணம்.
        ஒவ்வொரு அனுபவமும் நமக்கு ஒரு பாடம் கற்பிக்கிறது.
        அன்பானவர்களுடன் செலவிடும் நேரம் மகிழ்ச்சியை தருகிறது.
        இவை எல்லாம் இனிய நினைவுகளாக மாறுகின்றன.""",

        """சில நேரங்களில் எதிர்காலம் உற்சாகமாக தெரிகிறது.
        சில நேரங்களில் பழைய நினைவுகள் மனதில் வருகிறது.
        வெற்றி தோல்வி இரண்டிலும் வளர்ச்சி உள்ளது.
        அதுவே மனிதனை வலுவாக்குகிறது.""",

        """இசை கேட்பது மனதை அமைதியாக்குகிறது.
        நண்பர்களுடன் உரையாடல் நிம்மதி தருகிறது.
        இயற்கையில் நடைபயிற்சி புத்துணர்ச்சி அளிக்கிறது.
        சிறிய விஷயங்களில் அமைதி கிடைக்கிறது."""
    ],

    "hi": [
        """ज़िंदगी भावनाओं से भरी एक यात्रा है।
        हर अनुभव हमें कुछ नया सिखाता है।
        अपनों के साथ बिताया समय खुशी देता है।
        यही यादें जीवन को खूबसूरत बनाती हैं.""",

        """कभी भविष्य को लेकर उत्साह होता है।
        कभी अतीत की बातें याद आती हैं।
        सफलता और असफलता दोनों से सीख मिलती है।
        यही संतुलन हमें मजबूत बनाता है.""",

        """संगीत सुनने से मन शांत हो जाता है।
        दोस्तों से बात करना सुकून देता है।
        प्रकृति के बीच समय बिताना अच्छा लगता है।
        छोटी चीज़ों में खुशी छिपी होती है."""
    ],

    "ml": [
        """ജീവിതം വികാരങ്ങളാൽ നിറഞ്ഞ ഒരു യാത്രയാണ്.
        ഓരോ അനുഭവവും ഒരു പാഠമാണ്.
        പ്രിയപ്പെട്ടവരോടൊപ്പം സമയം ചെലവിടുന്നത് സന്തോഷം നൽകുന്നു.
        ഈ നിമിഷങ്ങൾ ഓർമ്മകളായി മാറുന്നു.""",

        """ഭാവിയെക്കുറിച്ച് ചിന്തിക്കുമ്പോൾ ഉത്സാഹം തോന്നും.
        ചിലപ്പോൾ പഴയ ഓർമ്മകൾ മനസ്സിൽ വരും.
        വിജയവും പരാജയവും നമ്മെ വളർത്തുന്നു.
        അതാണ് നമ്മെ ശക്തരാക്കുന്നത്.""",

        """സംഗീതം കേൾക്കുന്നത് മനസ്സിനെ ശാന്തമാക്കുന്നു.
        സുഹൃത്തുകളോട് സംസാരിക്കുന്നത് സന്തോഷം നൽകുന്നു.
        പ്രകൃതിയിൽ നടക്കുന്നത് മനസിന് ആശ്വാസമാണ്.
        ചെറിയ കാര്യങ്ങളിൽ സന്തോഷം ഒളിഞ്ഞിരിക്കുന്നു."""
    ],

    "te": [
        """జీవితం అనుభవాలతో నిండిన ఒక ప్రయాణం.
        ప్రతి సంఘటన మనకు ఒక పాఠం నేర్పుతుంది.
        మనకు ఇష్టమైన వారితో గడిపే సమయం ఆనందాన్ని ఇస్తుంది.
        ఇవే మన జ్ఞాపకాలుగా మిగులుతాయి.""",

        """భవిష్యత్తు గురించి ఆలోచించినప్పుడు ఉత్సాహం కలుగుతుంది.
        కొన్ని సార్లు గతాన్ని గుర్తు చేసుకుంటాము.
        విజయం మరియు అపజయం రెండూ మనకు పాఠాలు నేర్పుతాయి.
        అదే మనల్ని బలంగా మారుస్తుంది.""",

        """సంగీతం వినడం మనసుకు ప్రశాంతత ఇస్తుంది.
        స్నేహితులతో మాట్లాడటం సంతోషం ఇస్తుంది.
        ప్రకృతిలో నడక మనసును తేలిక చేస్తుంది.
        చిన్న విషయాల్లోనే ఆనందం ఉంటుంది."""
    ]
}

async def generate():
    for lang, voices in VOICE_MAP.items():
        for i in range(20):
            success = False

            while not success:
                try:
                    voice = random.choice(voices)
                    text = random.choice(TEXTS[lang])

                    filename = f"{OUTPUT_DIR}/{lang}_master_{i+1}.mp3"

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
                    print("Retrying due to:", e)
                    await asyncio.sleep(1)

asyncio.run(generate())
print("✅ MASTER DATASET GENERATED SUCCESSFULLY")
