# -----------------------------------------------
# 🔸 YORU MUSIC BOT Project
# 🔹 Developed & Maintained by: Yoru Music Bot ()
# 📅 Copyright © 2026 – All Rights Reserved
#
# 📖 License:
# This source code is open for educational and non-commercial use ONLY.
# You are required to retain this credit in all copies or substantial portions of this file.
# Commercial use, redistribution, or removal of this notice is strictly prohibited
# without prior written permission from the author.
#
# ❤️ Made with dedication and love by Yoru Music Bot
# -----------------------------------------------
from SIMPLE_MUSIC import app 
import asyncio
import random
from pyrogram import Client, filters
from pyrogram.enums import ChatType, ChatMemberStatus
from pyrogram.errors import UserNotParticipant
from pyrogram.types import ChatPermissions

spam_chats = []

EMOJI = [ "<emoji id='5316558987141852841'>🦋</emoji><emoji id='5316558987141852841'>🦋</emoji><emoji id='5316558987141852841'>🦋</emoji><emoji id='5316558987141852841'>🦋</emoji><emoji id='5316558987141852841'>🦋</emoji>",
          "<emoji id='5454136337345037322'>🧚</emoji><emoji id='5222044641200720562'>🌸</emoji><emoji id='5474268541278493225'>🧋</emoji><emoji id='5404573776253825754'>🍬</emoji>🫖",
          "<emoji id='5208923808169222461'>🥀</emoji><emoji id='5404835520150773707'>🌷</emoji><emoji id='6102617459204822706'>🌹</emoji><emoji id='5440748683765227563'>🌺</emoji><emoji id='5192959294470895031'>💐</emoji>",
          "<emoji id='5222044641200720562'>🌸</emoji>🌿💮🌱🌵",
          "❤️<emoji id='5280723695579438810'>💚</emoji><emoji id='5283006736985234502'>💙</emoji><emoji id='5283077114319347060'>💜</emoji><emoji id='5370986599423156302'>🖤</emoji>",
          "<emoji id='5258509003738066969'>💓</emoji><emoji id='5219862119209520083'>💕</emoji><emoji id='5219862119209520083'>💞</emoji><emoji id='5364201435858744869'>💗</emoji><emoji id='5431429648409969727'>💖</emoji>",
          "<emoji id='5222044641200720562'>🌸</emoji><emoji id='5192959294470895031'>💐</emoji><emoji id='5440748683765227563'>🌺</emoji><emoji id='6102617459204822706'>🌹</emoji><emoji id='5316558987141852841'>🦋</emoji>",
          "<emoji id='5364137887522628949'>🍔</emoji>🦪🍛🍲🥗",
          "🍎<emoji id='5418365569076304689'>🍓</emoji><emoji id='5415722218569089767'>🍒</emoji><emoji id='5852518588686011408'>🍑</emoji>🌶️",
          "<emoji id='5474268541278493225'>🧋</emoji>🥤<emoji id='5474268541278493225'>🧋</emoji><emoji id='5413704369918978673'>🥛</emoji><emoji id='5361964771509808811'>🍷</emoji>",
          "<emoji id='5404573776253825754'>🍬</emoji><emoji id='5287295223175604777'>🍭</emoji><emoji id='5420462646988123921'>🧁</emoji><emoji id='6334379727062566543'>🎂</emoji>🍡",
          "🍨🧉<emoji id='5363978187753670318'>🍺</emoji><emoji id='5463051955012122780'>☕</emoji>🍻",
          "🥪🥧<emoji id='5258378333653056711'>🍦</emoji>🍥🍚",
          "🫖<emoji id='5463051955012122780'>☕</emoji>🍹<emoji id='5361964771509808811'>🍷</emoji><emoji id='5413704369918978673'>🥛</emoji>",
          "<emoji id='5463051955012122780'>☕</emoji><emoji id='5303548912726982102'>🧃</emoji><emoji id='5213249338452485580'>🍩</emoji><emoji id='5258378333653056711'>🍦</emoji>🍙",
          "🍁🌾💮🍂🌿",
          "🌨️🌥️⛈️🌩️🌧️",
          "<emoji id='5404835520150773707'>🌷</emoji>🏵️<emoji id='5222044641200720562'>🌸</emoji><emoji id='5440748683765227563'>🌺</emoji><emoji id='5192959294470895031'>💐</emoji>",
          "💮🌼🌻🍀🍁",
          "<emoji id='5190680981824085932'>🧟</emoji>🦸🦹🧙<emoji id='5936271765218006741'>👸</emoji>",
          "🧅🍠<emoji id='5318752353925471388'>🥕</emoji>🌽<emoji id='5431469278073207884'>🥦</emoji>",
          "<emoji id='5357233044694508227'>🐷</emoji><emoji id='5305787660135063955'>🐹</emoji><emoji id='6111671507962829973'>🐭</emoji>🐨<emoji id='5206642759628241872'>🐻</emoji>‍❄️",
          "<emoji id='5316558987141852841'>🦋</emoji><emoji id='5278653070371206372'>🐇</emoji>🐀🐈🐈‍⬛",
          "🌼🌳🌲🌴🌵",
          "🥩🍋<emoji id='5456419915621742790'>🍐</emoji><emoji id='5438195085189595667'>🍈</emoji><emoji id='6273709899507568922'>🍇</emoji>",
          "<emoji id='6093451264555750089'>🍴</emoji><emoji id='5424978787920021797'>🍽</emoji>️<emoji id='5371042017386176566'>🔪</emoji>🍶🥃",
          "🕌<emoji id='5330116450843636190'>🏰</emoji>🏩⛩️🏩",
          "🎉<emoji id='5404573776253825754'>🎊</emoji><emoji id='5278651867780377852'>🎈</emoji><emoji id='6334379727062566543'>🎂</emoji><emoji id='5363882032025849098'>🎀</emoji>",
          "🪴🌵🌴🌳🌲",
          "🎄🎋🎍🎑🎎",
          "🦅🦜🕊️🦤🦢",
          "🦤🦩🦚🦃<emoji id='5368684320858843385'>🦆</emoji>",
          "<emoji id='5362063083311214432'>🐬</emoji><emoji id='5420642954010175242'>🦭</emoji>🦈<emoji id='6282818902372128272'>🐋</emoji><emoji id='5400362079783770689'>🐳</emoji>",
          "<emoji id='5283202076392827429'>🐔</emoji><emoji id='5384574037701696503'>🐟</emoji><emoji id='5397842858126353661'>🐠</emoji>🐡<emoji id='5361600498153564481'>🦐</emoji>",
          "🦩<emoji id='5222474515887435551'>🦀</emoji><emoji id='5474140796066210842'>🦑</emoji><emoji id='5352815688010441881'>🐙</emoji>🦪",
          "🐦<emoji id='5380003148821712039'>🦂</emoji><emoji id='6282555152725447369'>🕷</emoji>️<emoji id='5913384919584741274'>🕸</emoji>️<emoji id='5192907136388059100'>🐚</emoji>",
          "🥪🍰🥧🍨🍨",
          " 🥬<emoji id='5305336095863485125'>🍉</emoji><emoji id='5420462646988123921'>🧁</emoji>🧇",
        ]
        ####
        
SHAYRI = [ " <emoji id='5440748683765227563'>🌺</emoji><b>बहुत अच्छा लगता है तुझे सताना और फिर प्यार से तुझे मनाना।</b><emoji id='5440748683765227563'>🌺</emoji> \n\n<b><emoji id='5208923808169222461'>🥀</emoji>Bahut aacha lagta hai tujhe satana Aur fir pyar se tujhe manana.<emoji id='5208923808169222461'>🥀</emoji></b> ",
           " <emoji id='5440748683765227563'>🌺</emoji><b>मेरी जिंदगी मेरी जान हो तुम मेरे सुकून का दुसरा नाम हो तुम।</b><emoji id='5440748683765227563'>🌺</emoji> \n\n<b><emoji id='5208923808169222461'>🥀</emoji>Meri zindagi Meri jaan ho tum Mere sukoon ka Dusra naam ho tum.<emoji id='5208923808169222461'>🥀</emoji></b> ",
           " <emoji id='5440748683765227563'>🌺</emoji><b>तुम मेरी वो खुशी हो जिसके बिना, मेरी सारी खुशी अधूरी लगती है।</b><emoji id='5440748683765227563'>🌺</emoji> \n\n<b><emoji id='5208923808169222461'>🥀</emoji></b>Tum Meri Wo Khushi Ho Jiske Bina, Meri Saari Khushi Adhuri Lagti Ha.<emoji id='5208923808169222461'>🥀</emoji>** ",
           " <emoji id='5440748683765227563'>🌺</emoji><b>काश वो दिन जल्दी आए,जब तू मेरे साथ सात फेरो में बन्ध जाए।</b><emoji id='5440748683765227563'>🌺</emoji> \n\n<b><emoji id='5208923808169222461'>🥀</emoji>Kash woh din jldi aaye Jb tu mere sath 7 feron me bndh jaye.<emoji id='5208923808169222461'>🥀</emoji></b> ",
           " <emoji id='5440748683765227563'>🌺</emoji><b>अपना हाथ मेरे दिल पर रख दो और अपना दिल मेरे नाम कर दो।</b><emoji id='5440748683765227563'>🌺</emoji> \n\n<b><emoji id='5208923808169222461'>🥀</emoji>apna hath mere dil pr rakh do aur apna dil mere naam kar do.<emoji id='5208923808169222461'>🥀</emoji></b> ",
           " <emoji id='5440748683765227563'>🌺</emoji><b>महादेव ना कोई गाड़ी ना कोई बंगला चाहिए सलामत रहे मेरा प्यार बस यही दुआ चाहिए।</b><emoji id='5440748683765227563'>🌺</emoji> \n\n<b><emoji id='5208923808169222461'>🥀</emoji>Mahadev na koi gadi na koi bangla chahiye salamat rhe mera pyar bas yahi dua chahiye.<emoji id='5208923808169222461'>🥀</emoji></b> ",
           " <emoji id='5440748683765227563'>🌺</emoji><b>फिक्र तो होगी ना तुम्हारी इकलौती मोहब्बत हो तुम मेरी।</b><emoji id='5440748683765227563'>🌺</emoji> \n\n<b><emoji id='5208923808169222461'>🥀</emoji>Fikr to hogi na tumhari ikloti mohabbat ho tum meri.<emoji id='5208923808169222461'>🥀</emoji></b> ",
           " <emoji id='5440748683765227563'>🌺</emoji><b>सुनो जानू आप सिर्फ किचन संभाल लेना आप को संभालने के लिए मैं हूं ना।</b><emoji id='5440748683765227563'>🌺</emoji> \n\n<b><emoji id='5208923808169222461'>🥀</emoji>suno jaanu aap sirf kitchen sambhal lena ap ko sambhlne ke liye me hun naa.<emoji id='5208923808169222461'>🥀</emoji></b> ",
           " <emoji id='5440748683765227563'>🌺</emoji><b>सौ बात की एक बात मुझे चाहिए बस तेरा साथ।</b><emoji id='5440748683765227563'>🌺</emoji> \n\n<b><emoji id='5208923808169222461'>🥀</emoji>So bat ki ek bat mujhe chahiye bas tera sath.<emoji id='5208923808169222461'>🥀</emoji></b> ",
           " <emoji id='5440748683765227563'>🌺</emoji><b>बहुत मुश्किलों से पाया हैं तुम्हें, अब खोना नहीं चाहते,कि तुम्हारे थे तुम्हारे हैं अब किसी और के होना नहीं चाहते।</b><emoji id='5440748683765227563'>🌺</emoji> \n\n<b><emoji id='5208923808169222461'>🥀</emoji>Bahut muskilon se paya hai tumhe Ab khona ni chahte ki tumhare they tumhare hai ab kisi or k hona nhi chahte.<emoji id='5208923808169222461'>🥀</emoji></b> ",
           " <emoji id='5440748683765227563'>🌺</emoji><b>बेबी बातें तो रोज करते है चलो आज रोमांस करते है।</b><emoji id='5440748683765227563'>🌺</emoji> \n\n<b><emoji id='5208923808169222461'>🥀</emoji>Baby baten to roj karte haichalo aaj romance karte hai..<emoji id='5208923808169222461'>🥀</emoji></b> ",
           " <emoji id='5440748683765227563'>🌺</emoji><b>सुबह शाम तुझे याद करते है हम और क्या बताएं की तुमसे कितना प्यार करते है हम।</b><emoji id='5440748683765227563'>🌺</emoji> \n\n<b><emoji id='5208923808169222461'>🥀</emoji>subha sham tujhe yad karte hai hum aur kya batayen ki tumse kitna pyar karte hai hum.<emoji id='5208923808169222461'>🥀</emoji></b> ",
           " <emoji id='5440748683765227563'>🌺</emoji><b>किसी से दिल लग जाने को मोहब्बत नहीं कहते जिसके बिना दिल न लगे उसे मोहब्बत कहते हैं।</b><emoji id='5440748683765227563'>🌺</emoji> \n\n<b><emoji id='5208923808169222461'>🥀</emoji>Kisi se dil lag jane ko mohabbat nahi kehte jiske nina dil na lage use mohabbat kehte hai.<emoji id='5208923808169222461'>🥀</emoji></b> ",
           " <emoji id='5440748683765227563'>🌺</emoji><b>मेरे दिल के लॉक की चाबी हो तुम क्या बताएं जान मेरे जीने की एकलौती वजह हो तुम।</b><emoji id='5440748683765227563'>🌺</emoji> \n\n<b><emoji id='5208923808169222461'>🥀</emoji>mere dil ke lock ki chabi ho tum kya batayen jaan mere jeene ki eklauti wajah ho tum..<emoji id='5208923808169222461'>🥀</emoji></b> ",
           " <emoji id='5440748683765227563'>🌺</emoji><b>हम आपकी हर चीज़ से प्यार कर लेंगे, आपकी हर बात पर ऐतबार कर लेंगे, बस एक बार कह दो कि तुम सिर्फ मेरे हो, हम ज़िन्दगी भर आपका इंतज़ार कर लेंगे।</b><emoji id='5440748683765227563'>🌺</emoji> \n\n<b><emoji id='5208923808169222461'>🥀</emoji>Hum apki har cheez se pyar kar lenge apki har baat par etvar kar lenge bas ek bar keh do ki tum sirf mere ho hum zindagi bhar apka intzaar kar lenge..<emoji id='5208923808169222461'>🥀</emoji></b> ",
           " <emoji id='5440748683765227563'>🌺</emoji><b>मोहब्बत कभी स्पेशल लोगो से नहीं होती जिससे होती है वही स्पेशल बन जाता है।</b><emoji id='5440748683765227563'>🌺</emoji> \n\n<b><emoji id='5208923808169222461'>🥀</emoji>Mohabbat kabhi special logo se nahi hoti jisse bhi hoti hai wahi special ban jate hai,.<emoji id='5208923808169222461'>🥀</emoji></b>",
           " <emoji id='5440748683765227563'>🌺</emoji><b>तू मेरी जान है इसमें कोई शक नहीं तेरे अलावा मुझ पर किसी और का हक़ नहीं।</b><emoji id='5440748683765227563'>🌺</emoji> \n\n<b><emoji id='5208923808169222461'>🥀</emoji>Tu meri jaan hai isme koi shak nahi tere alawa mujhe par kisi aur ka hak nhi..<emoji id='5208923808169222461'>🥀</emoji></b> ",
           " <emoji id='5440748683765227563'>🌺</emoji><b>पहली मोहब्बत मेरी हम जान न सके, प्यार क्या होता है हम पहचान न सके, हमने उन्हें दिल में बसा लिया इस कदर कि, जब चाहा उन्हें दिल से निकाल न सके।</b><emoji id='5440748683765227563'>🌺</emoji> \n\n<b><emoji id='5208923808169222461'>🥀</emoji>Pehli mohabbat meri hum jaan na sake pyar kya hota hai hum pehchan na sake humne unhe dil me basa liya is kadar ki jab chaha unhe dil se nikal na sake.<emoji id='5208923808169222461'>🥀</emoji></b> ",
           " <emoji id='5440748683765227563'>🌺</emoji><b>खुद नहीं जानती वो कितनी प्यारी हैं , जान है हमारी पर जान से प्यारी हैं, दूरियों के होने से कोई फर्क नहीं पड़ता वो कल भी हमारी थी और आज भी हमारी है.</b><emoji id='5440748683765227563'>🌺</emoji> \n\n<b><emoji id='5208923808169222461'>🥀</emoji>khud nahi janti vo kitni pyari hai jan hai hamari par jan se jyda payari hai duriya ke hone se frak nahi pdta vo kal bhe hamari the or aaj bhe hamari hai.<emoji id='5208923808169222461'>🥀</emoji></b> ",
           " <emoji id='5440748683765227563'>🌺</emoji><b>चुपके से आकर इस दिल में उतर जाते हो, सांसों में मेरी खुशबु बनके बिखर जाते हो, कुछ यूँ चला है तेरे इश्क का जादू, सोते-जागते तुम ही तुम नज़र आते हो।</b><emoji id='5440748683765227563'>🌺</emoji> \n\n<b><emoji id='5208923808169222461'>🥀</emoji>Chupke Se Aakar Iss Dil Mein Utar Jate Ho, Saanso Mein Meri Khushbu BanKe Bikhar Jate Ho,Kuchh Yun Chala Hai Tere Ishq Ka Jadoo, Sote-Jagte Tum Hi Tum Najar Aate Ho..<emoji id='5208923808169222461'>🥀</emoji></b> ",
           " <emoji id='5440748683765227563'>🌺</emoji><b>प्यार करना सिखा है नफरतो का कोई ठौर नही, बस तु ही तु है इस दिल मे दूसरा कोई और नही.</b><emoji id='5440748683765227563'>🌺</emoji> \n\n<b><emoji id='5208923808169222461'>🥀</emoji>Pyar karna sikha hai naftaro ka koi thor nahi bas tu hi tu hai is dil me dusra koi aur nahi hai.<emoji id='5208923808169222461'>🥀</emoji></b> ",
           " <emoji id='5440748683765227563'>🌺</emoji><b>रब से आपकी खुशीयां मांगते है, दुआओं में आपकी हंसी मांगते है, सोचते है आपसे क्या मांगे,चलो आपसे उम्र भर की मोहब्बत मांगते है।</b><emoji id='5440748683765227563'>🌺</emoji>\n\n<b><emoji id='5208923808169222461'>🥀</emoji>Rab se apki khushiyan mangte hai duao me apki hansi mangte hai sochte hai apse kya mange chalo apse umar bhar ki mohabbat mangte hai..<emoji id='5208923808169222461'>🥀</emoji></b> ",
           " <emoji id='5440748683765227563'>🌺</emoji><b>काश मेरे होंठ तेरे होंठों को छू जाए देखूं जहा बस तेरा ही चेहरा नज़र आए हो जाए हमारा रिश्ता कुछ ऐसा होंठों के साथ हमारे दिल भी जुड़ जाए.</b><emoji id='5440748683765227563'>🌺</emoji>\n\n<b><emoji id='5208923808169222461'>🥀</emoji>kash mere hoth tere hontho ko chu jayen dekhun jaha bas teri hi chehra nazar aaye ho jayen humara rishta kuch easa hothon ke sath humare dil bhi jud jaye.<emoji id='5208923808169222461'>🥀</emoji></b> ",
           " <emoji id='5440748683765227563'>🌺</emoji><b>आज मुझे ये बताने की इजाज़त दे दो, आज मुझे ये शाम सजाने की इजाज़त दे दो, अपने इश्क़ मे मुझे क़ैद कर लो,आज जान तुम पर लूटाने की इजाज़त दे दो.</b><emoji id='5440748683765227563'>🌺</emoji>\n\n<b><emoji id='5208923808169222461'>🥀</emoji>Aaj mujhe ye batane ki izazat de do, aaj mujhe ye sham sajane ki izazat de do, apne ishq me mujhe ked kr lo aaj jaan tum par lutane ki izazat de do..<emoji id='5208923808169222461'>🥀</emoji></b> ",
           " <emoji id='5440748683765227563'>🌺</emoji><b>जाने लोग मोहब्बत को क्या क्या नाम देते है, हम तो तेरे नाम को ही मोहब्बत कहते है.</b><emoji id='5440748683765227563'>🌺</emoji>\n\n<b><emoji id='5208923808169222461'>🥀</emoji>Jane log mohabbat ko kya kya naam dete hai hum to tere naam ko hi mohabbat kehte hai..<emoji id='5208923808169222461'>🥀</emoji></b> ",
           " <emoji id='5440748683765227563'>🌺</emoji><b>देख के हमें वो सिर झुकाते हैं। बुला के महफिल में नजर चुराते हैं। नफरत हैं हमसे तो भी कोई बात नहीं। पर गैरो से मिल के दिल क्यों जलाते हो।</b><emoji id='5440748683765227563'>🌺</emoji>\n\n<b><emoji id='5208923808169222461'>🥀</emoji>Dekh Ke Hame Wo Sir Jhukate Hai Bula Ke Mahfhil Me Najar Churate Hai Nafrat Hai Hamse To Bhi Koei Bat Nhi Par Gairo Se Mil Ke Dil Kyo Jalate Ho.<emoji id='5208923808169222461'>🥀</emoji></b> ",
           " <emoji id='5440748683765227563'>🌺</emoji><b>तेरे बिना टूट कर बिखर जायेंगे,तुम मिल गए तो गुलशन की तरह खिल जायेंगे, तुम ना मिले तो जीते जी ही मर जायेंगे, तुम्हें जो पा लिया तो मर कर भी जी जायेंगे।</b><emoji id='5440748683765227563'>🌺</emoji>\n\n<b><emoji id='5208923808169222461'>🥀</emoji>Tere bina tut kar bikhar jeynge tum mil gaye to gulshan ki tarha khil jayenge tum na mile to jite ji hi mar jayenge tumhe jo pa liya to mar kar bhi ji jayenge..<emoji id='5208923808169222461'>🥀</emoji></b> ",
           " <emoji id='5440748683765227563'>🌺</emoji><b>सनम तेरी कसम जेसे मै जरूरी हूँ तेरी ख़ुशी के लिये, तू जरूरी है मेरी जिंदगी के लिये.</b><emoji id='5440748683765227563'>🌺</emoji>\n\n<b><emoji id='5208923808169222461'>🥀</emoji>Sanam teri kasam jese me zaruri hun teri khushi ke liye tu zaruri hai meri zindagi ke liye.<emoji id='5208923808169222461'>🥀</emoji></b> ",
           " <emoji id='5440748683765227563'>🌺</emoji><b>तुम्हारे गुस्से पर मुझे बड़ा प्यार आया हैं इस बेदर्द दुनिया में कोई तो हैं जिसने मुझे पुरे हक्क से धमकाया हैं.</b><emoji id='5440748683765227563'>🌺</emoji>\n\n<b><emoji id='5208923808169222461'>🥀</emoji>Tumharfe gusse par mujhe pyar aaya hai is bedard duniya me koi to hai jisne mujhe pure hakk se dhamkaya hai.<emoji id='5208923808169222461'>🥀</emoji></b> ",
           " <emoji id='5440748683765227563'>🌺</emoji><b>पलको से आँखो की हिफाजत होती है धडकन दिल की अमानत होती है ये रिश्ता भी बडा प्यारा होता है कभी चाहत तो कभी शिकायत होती है.</b><emoji id='5440748683765227563'>🌺</emoji>\n\n<b><emoji id='5208923808169222461'>🥀</emoji>Palkon se Aankho ki hifajat hoti hai dhakad dil ki Aamanat hoti hai, ye rishta bhi bada pyara hota hai, kabhi chahat to kabhi shikayat hoti hai.<emoji id='5208923808169222461'>🥀</emoji></b> ",
           " <emoji id='5440748683765227563'>🌺</emoji><b>मुहब्बत को जब लोग खुदा मानते हैं प्यार करने वाले को क्यों बुरा मानते हैं। जब जमाना ही पत्थर दिल हैं। फिर पत्थर से लोग क्यों दुआ मांगते है।</b><emoji id='5440748683765227563'>🌺</emoji>\n\n<b><emoji id='5208923808169222461'>🥀</emoji>Muhabbt Ko Hab Log Khuda Mante Hai, Payar Karne Walo Ko Kyu Bura Mante Hai,Jab Jamana Hi Patthr Dil Hai,Fhir Patthr Se Log Kyu Duaa Magte Hai.<emoji id='5208923808169222461'>🥀</emoji></b> ",
           " <emoji id='5440748683765227563'>🌺</emoji><b>हुआ जब इश्क़ का एहसास उन्हें आकर वो पास हमारे सारा दिन रोते रहे हम भी निकले खुदगर्ज़ इतने यारो कि ओढ़ कर कफ़न, आँखें बंद करके सोते रहे।</b><emoji id='5440748683765227563'>🌺</emoji>\n\n<b><emoji id='5208923808169222461'>🥀</emoji>Hua jab ishq ka ehsaas unhe akar wo pass humare sara din rate rahe, hum bhi nikale khudgarj itne yaro ki ood kar kafan ankhe band krke sote rhe.<emoji id='5208923808169222461'>🥀</emoji></b> ",
           " <emoji id='5440748683765227563'>🌺</emoji><b>दिल के कोने से एक आवाज़ आती हैं। हमें हर पल उनकी याद आती हैं। दिल पुछता हैं बार -बार हमसे के जितना हम याद करते हैं उन्हें क्या उन्हें भी हमारी याद आती हैं।</b><emoji id='5440748683765227563'>🌺</emoji>\n\n<b><emoji id='5208923808169222461'>🥀</emoji>Dil Ke Kone Se Ek Aawaj Aati Hai, Hame Har Pal Uaski Yad Aati Hai, Dil Puchhta Hai Bar Bar Hamse Ke, Jitna Ham Yad Karte Hai Uanhe, Kya Uanhe Bhi Hamari Yad Aati Hai,<emoji id='5208923808169222461'>🥀</emoji></b> ",
           " <emoji id='5440748683765227563'>🌺</emoji><b>कभी लफ्ज़ भूल जाऊं कभी बात भूल जाऊं, तूझे इस कदर चाहूँ कि अपनी जात भूल जाऊं, कभी उठ के तेरे पास से जो मैं चल दूँ, जाते हुए खुद को तेरे पास भूल जाऊं।</b><emoji id='5440748683765227563'>🌺</emoji>\n\n<b><emoji id='5208923808169222461'>🥀</emoji>Kabhi Lafz Bhool Jaaun Kabhi Baat Bhool Jaaun, Tujhe Iss Kadar Chahun Ki Apni Jaat Bhool Jaaun, Kabhi Uthh Ke Tere Paas Se Jo Main Chal Dun, Jaate Huye Khud Ko Tere Paas Bhool Jaaun..<emoji id='5208923808169222461'>🥀</emoji></b> ",
           " <emoji id='5440748683765227563'>🌺</emoji><b>आईना देखोगे तो मेरी याद आएगी साथ गुज़री वो मुलाकात याद आएगी पल भर क लिए वक़्त ठहर जाएगा, जब आपको मेरी कोई बात याद आएगी.</b><emoji id='5440748683765227563'>🌺</emoji>\n\n<b><emoji id='5208923808169222461'>🥀</emoji>Aaina dekhoge to meri yad ayegi sath guzari wo mulakat yad ayegi pal bhar ke waqt thahar jayega jab apko meri koi bat yad ayegi.<emoji id='5208923808169222461'>🥀</emoji></b> ",
           " <emoji id='5440748683765227563'>🌺</emoji><b>प्यार किया तो उनकी मोहब्बत नज़र आई दर्द हुआ तो पलके उनकी भर आई दो दिलों की धड़कन में एक बात नज़र आई दिल तो उनका धड़का पर आवाज़ इस दिल की आई.</b><emoji id='5440748683765227563'>🌺</emoji>\n\n<b><emoji id='5208923808169222461'>🥀</emoji>Pyar kiya to unki mohabbat nazar aai dard hua to palke unki bhar aai do dilon ki dhadkan me ek baat nazar aai dil to unka dhadka par awaz dil ki aai.<emoji id='5208923808169222461'>🥀</emoji></b> ",
           " <emoji id='5440748683765227563'>🌺</emoji><b>कई चेहरे लेकर लोग यहाँ जिया करते हैं हम तो बस एक ही चेहरे से प्यार करते हैं ना छुपाया करो तुम इस चेहरे को,क्योंकि हम इसे देख के ही जिया करते हैं.</b><emoji id='5440748683765227563'>🌺</emoji>\n\n<b><emoji id='5208923808169222461'>🥀</emoji>Kai chehre lekar log yahn jiya karte hai hum to bas ek hi chehre se pyar karte hai na chupaya karo tum is chehre ko kyuki hum ise dekh ke hi jiya karte hai.<emoji id='5208923808169222461'>🥀</emoji></b> ",
           " <emoji id='5440748683765227563'>🌺</emoji><b>सबके bf को अपनी gf से बात करके नींद आजाती है और मेरे वाले को मुझसे लड़े बिना नींद नहीं आती।</b><emoji id='5440748683765227563'>🌺</emoji>\n\n<b><emoji id='5208923808169222461'>🥀</emoji>Sabke bf ko apni gf se baat karke nind aajati hai aur mere wale ko mujhse lade bina nind nhi aati.<emoji id='5208923808169222461'>🥀</emoji></b> ",
           " <emoji id='5440748683765227563'>🌺</emoji><b>सच्चा प्यार कहा किसी के नसीब में होता है. एसा प्यार कहा इस दुनिया में किसी को नसीब होता है.</b><emoji id='5440748683765227563'>🌺</emoji>\n\n<b><emoji id='5208923808169222461'>🥀</emoji>Sacha pyar kaha kisi ke nasib me hota hai esa pyar kahan is duniya me kisi ko nasib hota hai.<emoji id='5208923808169222461'>🥀</emoji></b> " ]

# Command
    


@app.on_message(filters.command(["shayari" ], prefixes=["/", "@", "#"]))
async def mentionall(client, message):
    chat_id = message.chat.id
    if message.chat.type == ChatType.PRIVATE:
        return await message.reply("𝐓𝐡𝐢𝐬 𝐂𝐨𝐦𝐦𝐚𝐧𝐝 𝐎𝐧𝐥𝐲 𝐅𝐨𝐫 𝐆𝐫𝐨𝐮𝐩𝐬.")

    is_admin = False
    try:
        participant = await client.get_chat_member(chat_id, message.from_user.id)
    except UserNotParticipant:
        is_admin = False
    else:
        if participant.status in (
            ChatMemberStatus.ADMINISTRATOR,
            ChatMemberStatus.OWNER
        ):
            is_admin = True
    if not is_admin:
        return await message.reply("𝐘𝐨𝐮 𝐀𝐫𝐞 𝐍𝐨𝐭 𝐀𝐝𝐦𝐢𝐧 𝐁𝐚𝐛𝐲, 𝐎𝐧𝐥𝐲 𝐀𝐝𝐦𝐢𝐧𝐬 𝐂𝐚𝐧 . ")

    if message.reply_to_message and message.text:
        return await message.reply("/shayaril  𝐓𝐲𝐩𝐞 𝐋𝐢𝐤𝐞 𝐓𝐡𝐢𝐬 / 𝐑𝐞𝐩𝐥𝐲 𝐀𝐧𝐲 𝐌𝐞𝐬𝐬𝐚𝐠𝐞 𝐍𝐞𝐱𝐭 𝐓𝐢𝐦𝐞 ")
    elif message.text:
        mode = "text_on_cmd"
        msg = message.text
    elif message.reply_to_message:
        mode = "text_on_reply"
        msg = message.reply_to_message
        if not msg:
            return await message.reply("/shayari  𝐓𝐲𝐩𝐞 𝐋𝐢𝐤𝐞 𝐓𝐡𝐢𝐬 / 𝐑𝐞𝐩𝐥𝐲 𝐀𝐧𝐲 𝐌𝐞𝐬𝐬𝐚𝐠𝐞 𝐍𝐞𝐱𝐭 𝐓𝐢𝐦𝐞 ...")
    else:
        return await message.reply("/shayari  𝐓𝐲𝐩𝐞 𝐋𝐢𝐤𝐞 𝐓𝐡𝐢𝐬 / 𝐑𝐞𝐩𝐥𝐲 𝐀𝐧𝐲 𝐌𝐞𝐬𝐬𝐚𝐠𝐞 𝐍𝐞𝐱𝐭 𝐓𝐢𝐦𝐞 ..")
    if chat_id in spam_chats:
        return await message.reply("𝐏𝐥𝐞𝐚𝐬𝐞 𝐀𝐭 𝐅𝐢𝐫𝐬𝐭 𝐒𝐭𝐨𝐩 𝐑𝐮𝐧𝐧𝐢𝐧𝐠 𝐏𝐫𝐨𝐜𝐞𝐬𝐬 ...")
    spam_chats.append(chat_id)
    usrnum = 0
    usrtxt = ""
    async for usr in client.get_chat_members(chat_id):
        if not chat_id in spam_chats:
            break
        if usr.user.is_bot:
            continue
        usrnum += 1
        usrtxt += f"<a href='tg://user?id={usr.user.id}'>{usr.user.first_name}</a> "

        if usrnum == 1:
            if mode == "text_on_cmd":
                txt = f"{usrtxt} {random.choice(SHAYRI)}"
                await client.send_message(chat_id, txt)
            elif mode == "text_on_reply":
                await msg.reply(f"<a href='tg://user?id={usr.user.id}'>{random.choice(EMOJI)}</a>")
            await asyncio.sleep(4)
            usrnum = 0
            usrtxt = ""
    try:
        spam_chats.remove(chat_id)
    except:
        pass


#

@app.on_message(filters.command(["shstop", "shayarioff"]))
async def cancel_spam(client, message):
    if not message.chat.id in spam_chats:
        return await message.reply("𝐂𝐮𝐫𝐫𝐞𝐧𝐭𝐥𝐲 𝐈'𝐦 𝐍𝐨𝐭 ..")
    is_admin = False
    try:
        participant = await client.get_chat_member(message.chat.id, message.from_user.id)
    except UserNotParticipant:
        is_admin = False
    else:
        if participant.status in (
            ChatMemberStatus.ADMINISTRATOR,
            ChatMemberStatus.OWNER
        ):
            is_admin = True
    if not is_admin:
        return await message.reply("𝐘𝐨𝐮 𝐀𝐫𝐞 𝐍𝐨𝐭 𝐀𝐝𝐦𝐢𝐧 𝐁𝐚𝐛𝐲, 𝐎𝐧𝐥𝐲 𝐀𝐝𝐦𝐢𝐧𝐬 𝐂𝐚𝐧 𝐓𝐚𝐠 𝐌𝐞𝐦𝐛𝐞𝐫𝐬.")
    else:
        try:
            spam_chats.remove(message.chat.id)
        except:
            pass
        return await message.reply("<emoji id='5314382594068984646'>♦</emoji> OFFFFFFFFF<emoji id='5314382594068984646'>♦</emoji>")
