import time,os,subprocess
from telebot import TeleBot
from requests import get
from num2words import num2words
from pydub import AudioSegment
from telebot.types import InlineKeyboardButton as bt, InlineKeyboardMarkup as kp
from kvsqlite.sync import Client
ids = os.environ.get("API_ID")
db = Client("amo.sqlite")
bot = TeleBot("TG_BOT_TOKEN")
  
if not db.exists("myNums"):
    aa = db.set("myNums", 124)
aa = db.set("status", False)
idch = os.environ.get("ID")
a = bot.get_chat(idch)
print(a)
def get_ayah(num: int) -> str:
    num = int(num)
    url = 'https://cdn.islamic.network/quran/audio/128/ar.alafasy/'
    if (num) >=1 and (num)<=6236:
        url = url+f'{(num)}.mp3'
    x = get(url)
    with open(f"sura{num}.mp3", "wb") as f:
        f.write(x.content)
    filename = os.path.splitext(f'sura{num}.mp3')[0]
    audio_path_ogg = filename + '.ogg'
    subprocess.run(["ffmpeg", '-i', f'sura{num}.mp3', '-vn', '-acodec', 'libopus', '-b:a', '16k', audio_path_ogg, '-y'], stderr=subprocess.PIPE, encoding='utf-8')
    with open(audio_path_ogg, 'rb') as f:
        data = f.read()
    os.remove(f"sura{num}.mp3")
    return audio_path_ogg
def en_ar_nums(text):
    arabic_numbers = {'0': '٠', '1': '١', '2': '٢', '3': '٣', '4': '٤', '5': '٥', '6': '٦', '7': '٧', '8': '٨', '9': '٩'}
    result = ''
    for char in str(text):
        if char.isdigit():
            result += arabic_numbers[char]
        else:
            result += char
    return result
@bot.message_handler(commands=['start'])
def Get(message):
    try:
            
        if ids == message.from_user.id:
            if db.get("status") != False:
                bot.send_message(message.chat.id, "القُرآن مشتغل من قبل.")
            else:
                db.set("status", True)
                a = bot.get_chat(idch)
                bot.send_message(
                    message.chat.id,
                    "بدأ تشغيل القُرآن .\n بلقناه : {} \n رابط القناه : {} \n ايدي القناه : {}".format(
                        a.title, a.invite_link,a.id
                    ),
                )
                xx= int(db.get("myNums"))
                #while xx <= 6236:
                for i in range(xx,6236):
                    xx += 1
                    db.set("myNums", int(xx))
                    print(xx)
                    x = get(f"http://api.alquran.cloud/v1/ayah/{xx}/ar.asad")
                    if x.json():
                        print(x.json())
                        ayah = x.json()["data"]["text"]
                        surah_name = x.json()["data"]["surah"]["name"]
                        as_audio = get_ayah(xx)
                        print(as_audio)
                        voice_file = open(as_audio, "rb")
                        message = ("{} ﴿{}﴾" '\n\n - {} " الجُزء {}، صفحه {}"').format(
                            ayah,
                            en_ar_nums(x.json()['data']['numberInSurah']),
                            surah_name,
                            num2words(x.json()["data"]["juz"], lang="ar", to="year"),
                            num2words(x.json()["data"]["page"], lang="ar", to="year"),
                        )
                        a = bot.get_chat(idch)
                        keyboard = kp()
                        keyboard.add(bt(a.title, url=a.invite_link))
                        bot.send_voice(
                            idch,
                            voice_file,
                            caption=message,
                            reply_markup=keyboard
                        )
                        try:
                            
                            os.remove(as_audio)
                            os.remove(f"sura{xx}.ogg")
                            os.remove(f"sura{xx}.mp3")
                        except:pass
                        time.sleep(86400)
    except:pass
bot.infinity_polling()
