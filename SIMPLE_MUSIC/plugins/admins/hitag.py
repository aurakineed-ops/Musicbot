# -----------------------------------------------
# 🔸 AALIYA MUSIC BOT Project
# 🔹 Developed & Maintained by: Aaliya Music Bot ()
# 📅 Copyright © 2026 – All Rights Reserved
#
# 📖 License:
# This source code is open for educational and non-commercial use ONLY.
# You are required to retain this credit in all copies or substantial portions of this file.
# Commercial use, redistribution, or removal of this notice is strictly prohibited
# without prior written permission from the author.
#
# ❤️ Made with dedication and love by Aaliya Music Bot
# -----------------------------------------------
from SIMPLE_MUSIC import app 
import asyncio
from html import escape
import random
from pyrogram import Client, filters
from pyrogram.enums import ChatType, ChatMemberStatus, ParseMode
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

TAGMES = [ " <b>❅ बेबी कहा हो। <emoji id='5210905596273905344'>🤗</emoji></b> ",
           " <b>❅ ओए सो गए क्या, ऑनलाइन आओ ।<emoji id='5370738629486319646'>😊</emoji></b> ",
           " <b>❅ ओए वीसी आओ बात करते हैं । 😃</b> ",
           " <b>❅ खाना खाया कि नही। 🥲</b> ",
           " <b>❅ घर में सब कैसे हैं। <emoji id='6093779241143374561'>🥺</emoji></b> ",
           " <b>❅ पता है बहुत याद आ रही आपकी। 🤭</b> ",
           " <b>❅ और बताओ कैसे हो।..?? 🤨</b> ",
           " <b>❅ मेरी भी सैटिंग करवा दो प्लीज..?? <emoji id='6082408856393099293'>🙂</emoji></b> ",
           " <b>❅ आपका नाम क्या है।..?? 🥲</b> ",
           " <b>❅ नाश्ता हो गया..?? 😋</b> ",
           " <b>❅ मुझे अपने ग्रूप में ऐड कर लो। <emoji id='5449442513616121857'>😍</emoji></b> ",
           " <b>❅ आपका दोस्त आपको बुला रहा है। <emoji id='5415816441561619011'>😅</emoji></b> ",
           " <b>❅ मुझसे शादी करोगे ..?? <emoji id='5467538555158943525'>🤔</emoji></b> ",
           " <b>❅ सोने चले गए क्या <emoji id='5303299516861005906'>🙄</emoji></b> ",
           " <b>❅ अरे यार कोई AC चला दो 😕</b> ",
           " <b>❅ आप कहा से हो..?? <emoji id='5381884327317478231'>🙃</emoji></b> ",
           " <b>❅ हेलो जी नमस्ते 😛</b> ",
           " <b>❅ BABY क्या कर रही हो..? <emoji id='5467538555158943525'>🤔</emoji></b> ",
           " <b>❅ क्या आप मुझे जानते हो .? <emoji id='5371037748188683677'>☺</emoji>️</b> ",
           " <b>❅ आओ baby Ludo खेलते है .<emoji id='5210905596273905344'>🤗</emoji></b> ",
           " <b>❅ चलती है क्या 9 से 12... <emoji id='5366573864123903238'>😇</emoji></b> ",
           " <b>❅ आपके पापा क्या करते है 🤭</b> ",
           " <b>❅ आओ baby बाजार चलते है गोलगप्पे खाने। <emoji id='6093779241143374561'>🥺</emoji></b> ",
           " <b>❅ अकेली ना बाजार जाया करो, नज़र लग जायेगी। 😶</b> ",
           " <b>❅ और बताओ BF कैसा है ..?? <emoji id='5467538555158943525'>🤔</emoji></b> ",
           " <b>❅ गुड मॉर्निंग <emoji id='5427255159241590813'>😜</emoji></b> ",
           " <b>❅ मेरा एक काम करोगे। <emoji id='6082408856393099293'>🙂</emoji></b> ",
           " <b>❅ DJ वाले बाबू मेरा गाना चला दो। <emoji id='5371009319800150304'>😪</emoji></b> ",
           " <b>❅ आप से मिलकर अच्छा लगा।<emoji id='5371037748188683677'>☺</emoji></b> ",
           " <b>❅ मेरे बाबू ने थाना थाया।..? <emoji id='5467550297599516219'>🙊</emoji></b> ",
           " <b>❅ पढ़ाई कैसी चल रही हैं ? 😺</b> ",
           " <b>❅ हम को प्यार हुआ। 🥲</b> ",
           " <b>❅ Nykaa कौन है...? <emoji id='5415816441561619011'>😅</emoji></b> ",
           " <b>❅ तू खींच मेरी फ़ोटो ..? <emoji id='5415816441561619011'>😅</emoji></b> ",
           " <b>❅ Phone काट मम्मी आ गई क्या। <emoji id='6053086169770493395'>😆</emoji></b> ",
           " <b>❅ और भाबी से कब मिल वा रहे हो । <emoji id='5458394638505223612'>😉</emoji></b> ",
           " <b>❅ क्या आप मुझसे प्यार करते हो <emoji id='5280723695579438810'>💚</emoji></b> ",
           " <b>❅ मैं तुम से बहुत प्यार करती हूं..? <emoji id='5208841018379612211'>👀</emoji></b> ",
           " <b>❅ बेबी एक kiss दो ना..?? 🙉</b> ",
           " <b>❅ एक जॉक सुनाऊं..? 😹</b> ",
           " <b>❅ vc पर आओ कुछ दिखाती हूं  <emoji id='5362081079224180363'>😻</emoji></b> ",
           " <b>❅ क्या तुम instagram चलते हो..?? <emoji id='5381884327317478231'>🙃</emoji></b> ",
           " <b>❅ whatsapp नंबर दो ना अपना..? 😕</b> ",
           " <b>❅ आप की दोस्त से मेरी सेटिंग करा दो ..? <emoji id='5381884327317478231'>🙃</emoji></b> ",
           " <b>❅ सारा काम हो गया हो तो ऑनलाइन आ जाओ।..? <emoji id='5381884327317478231'>🙃</emoji></b> ",
           " <b>❅ कहा से हो आप <emoji id='5370738629486319646'>😊</emoji></b> ",
           " <b>❅ जा तुझे आज़ाद कर दिया मैंने मेरे दिल से। <emoji id='6093779241143374561'>🥺</emoji></b> ",
           " <b>❅ मेरा एक काम करोगे, ग्रूप मे कुछ मेंबर ऐड कर दो ..? ♥️</b> ",
           " <b>❅ मैं तुमसे नाराज़ हूं <emoji id='5337199783922641650'>😠</emoji></b> ",
           " <b>❅ आपकी फैमिली कैसी है..? ❤</b> ",
           " <b>❅ क्या हुआ..? <emoji id='5467538555158943525'>🤔</emoji></b> ",
           " <b>❅ बहुत याद आ रही है आपकी <emoji id='6111657897211469042'>😒</emoji></b> ",
           " <b>❅ भूल गए मुझे <emoji id='5458394638505223612'>😏</emoji></b> ",
           " <b>❅ झूठ क्यों बोला आपने मुझसे <emoji id='5321012601939838274'>🤐</emoji></b> ",
           " <b>❅ इतना भाव मत खाया करो, रोटी खाया करो कम से कम मोटी तो हो जाओगी <emoji id='6111657897211469042'>😒</emoji></b> ",
           " <b>❅ ये attitude किसे दिखा रहे हो <emoji id='5318803056014408611'>😮</emoji></b> ",
           " <b>❅ हेमलो कहा busy ho <emoji id='5208841018379612211'>👀</emoji></b> ",
           " <b>❅ आपके जैसा दोस्त पाकर मे बहुत खुश हूं। <emoji id='5467370583282950466'>🙈</emoji></b> ",
           " <b>❅ आज मन बहुत उदास है <emoji id='6111767908503788860'>☹</emoji>️</b> ",
           " <b>❅ मुझसे भी बात कर लो ना <emoji id='6093779241143374561'>🥺</emoji></b> ",
           " <b>❅ आज खाने में क्या बनाया है <emoji id='5208841018379612211'>👀</emoji></b> ",
           " <b>❅ क्या चल रहा है <emoji id='6082408856393099293'>🙂</emoji></b> ",
           " <b>❅ message क्यों नहीं करती हो..<emoji id='6093779241143374561'>🥺</emoji></b> ",
           " <b>❅ मैं मासूम हूं ना <emoji id='6093779241143374561'>🥺</emoji></b> ",
           " <b>❅ कल मज़ा आया था ना <emoji id='5415816441561619011'>😅</emoji></b> ",
           " <b>❅ कल कहा busy थे 😕</b> ",
           " <b>❅ आप relationship में हो क्या..? <emoji id='5208841018379612211'>👀</emoji></b> ",
           " <b>❅ कितने शांत रहते हो यार आप 😼</b> ",
           " <b>❅ आपको गाना, गाना आता है..? <emoji id='5262617535093690646'>😸</emoji></b> ",
           " <b>❅ घूमने चलोगे मेरे साथ..?? <emoji id='5467370583282950466'>🙈</emoji></b> ",
           " <b>❅ हमेशा हैप्पी रहा करो यार <emoji id='5427078438517218023'>🤞</emoji></b> ",
           " <b>❅ क्या हम दोस्त बन सकते है...? <emoji id='5422369870165584898'>🥰</emoji></b> ",
           " <b>❅ आप का विवाह हो गया क्या.. <emoji id='6093779241143374561'>🥺</emoji></b> ",
           " <b>❅ कहा busy the इतने दिनों से 🥲</b> ",
           " <b>❅ single हो या mingle <emoji id='5458394638505223612'>😉</emoji></b> ",
           " <b>❅ आओ पार्टी करते है <emoji id='5317026657540780588'>🥳</emoji></b> ",
           " <b>❅ Bio में link हैं join कर लो <emoji id='5316996360841474316'>🧐</emoji></b> ",
           " <b>❅ मैं तुमसे प्यार नहीं करती, <emoji id='6093779241143374561'>🥺</emoji></b> ",
           " <b>❅ यहां आ जाओ ना ( @music_Bot_Adda ) मस्ती करेंगे 🤭</b> ",
           " <b>❅ भूल जाओ मुझे,..? <emoji id='5370738629486319646'>😊</emoji></b> ",
           " <b>❅ अपना बना ले पिया, अपना बना ले <emoji id='6093779241143374561'>🥺</emoji></b> ",
           " <b>❅ मेरा ग्रुप भी join कर लो ना <emoji id='5210905596273905344'>🤗</emoji></b> ",
           " <b>❅ मैने तेरा नाम Dil rakh diya 😗</b> ",
           " <b>❅ तुमारे सारे दोस्त कहा गए <emoji id='6093779241143374561'>🥺</emoji></b> ",
           " <b>❅ my cute owner @The_LuckyX <emoji id='5422369870165584898'>🥰</emoji></b> ",
           " <b>❅ किसकी याद मे खोए हो जान <emoji id='5427255159241590813'>😜</emoji></b> ",
           " <b>❅ गुड नाईट जी बहुत रात हो गई <emoji id='5422369870165584898'>🥰</emoji></b> ",
           ]

VC_TAG = [ "<b>❅ ɪғ ʏᴏᴜ ᴅᴏ ɴᴏᴛ sᴛᴇᴘ ғᴏʀᴡᴀʀᴅ ʏᴏᴜ ᴡɪʟʟ ʀᴇᴍᴀɪɴ ɪɴ ᴛʜᴇ sᴀᴍᴇ ᴘʟᴀᴄᴇ.</b>",
         "<b>❅ ʟɪғᴇ ɪs ʜᴀʀᴅ ʙᴜᴛ ɴᴏᴛ ɪᴍᴘᴏssɪʙʟᴇ.</b>",
         "<b>❅ ʟɪғᴇ’s ᴛᴏᴏ sʜᴏʀᴛ ᴛᴏ ᴀʀɢᴜᴇ ᴀɴᴅ ғɪɢʜᴛ.</b>",
         "<b>❅ ᴅᴏɴ’ᴛ ᴡᴀɪᴛ ғᴏʀ ᴛʜᴇ ᴘᴇʀғᴇᴄᴛ ᴍᴏᴍᴇɴᴛ ᴛᴀᴋᴇ ᴍᴏᴍᴇɴᴛ ᴀɴᴅ ᴍᴀᴋᴇ ɪᴛ ᴘᴇʀғᴇᴄᴛ.</b>",
         "<b>❅ sɪʟᴇɴᴄᴇ ɪs ᴛʜᴇ ʙᴇsᴛ ᴀɴsᴡᴇʀ ᴛᴏ sᴏᴍᴇᴏɴᴇ ᴡʜᴏ ᴅᴏᴇsɴ’ᴛ ᴠᴀʟᴜᴇ ʏᴏᴜʀ ᴡᴏʀᴅs.</b>",
         "<b>❅ ᴇᴠᴇʀʏ ɴᴇᴡ ᴅᴀʏ ɪs ᴀ ᴄʜᴀɴᴄᴇ ᴛᴏ ᴄʜᴀɴɢᴇ ʏᴏᴜʀ ʟɪғᴇ.</b>",
         "<b>❅ ᴛᴏ ᴄʜᴀɴɢᴇ ʏᴏᴜʀ ʟɪғᴇ, ʏᴏᴜ ɴᴇᴇᴅ ᴛᴏ ᴄʜᴀɴɢᴇ ʏᴏᴜʀ ᴘʀɪᴏʀɪᴛɪᴇs.</b>",
         "<b>❅ ʟɪғᴇ ɪs ᴀ ᴊᴏᴜʀɴᴇʏ, ɴᴏᴛ ᴀ ʀᴀᴄᴇ..</b>",
         "<b>❅ sᴍɪʟᴇ ᴀɴᴅ ᴅᴏɴ’ᴛ ᴡᴏʀʀʏ, ʟɪғᴇ ɪs ᴀᴡᴇsᴏᴍᴇ.</b>",
         "<b>❅ ᴅᴏ ɴᴏᴛ ᴄᴏᴍᴘᴀʀᴇ ʏᴏᴜʀsᴇʟғ ᴛᴏ ᴏᴛʜᴇʀs ɪғ ʏᴏᴜ ᴅᴏ sᴏ ʏᴏᴜ ᴀʀᴇ ɪɴsᴜʟᴛɪɴɢ ʏᴏᴜʀsᴇʟғ.</b>",
         "<b>❅ ɪ ᴀᴍ ɪɴ ᴛʜᴇ ᴘʀᴏᴄᴇss ᴏғ ʙᴇᴄᴏᴍɪɴɢ ᴛʜᴇ ʙᴇsᴛ ᴠᴇʀsɪᴏɴ ᴏғ ᴍʏsᴇʟғ.</b>",
         "<b>❅ ʟɪғᴇ ɪs ʟɪᴋᴇ ɪᴄᴇ ᴇɴᴊᴏʏ ɪᴛ ʙᴇғᴏʀᴇ ɪᴛ ᴍᴇʟᴛs.</b>",
         "<b>❅ ʙᴇ ғʀᴇᴇ ʟɪᴋᴇ ᴀ ʙɪʀᴅ.</b>",
         "<b>❅ ɴᴏ ᴏɴᴇ ɪs ᴄᴏᴍɪɴɢ ᴛᴏ sᴀᴠᴇ ʏᴏᴜ. ᴛʜɪs ʟɪғᴇ ᴏғ ʏᴏᴜʀ ɪs 100% ʏᴏᴜʀ ʀᴇsᴘᴏɴsɪʙɪʟɪᴛʏ..</b>",
         "<b>❅ ʟɪғᴇ ᴀʟᴡᴀʏs ᴏғғᴇʀs ʏᴏᴜ ᴀ sᴇᴄᴏɴᴅ ᴄʜᴀɴᴄᴇ. ɪᴛ’s ᴄᴀʟʟᴇᴅ ᴛᴏᴍᴏʀʀᴏᴡ.</b>",
         "<b>❅ ʟɪғᴇ ʙᴇɢɪɴs ᴀᴛ ᴛʜᴇ ᴇɴᴅ ᴏғ ʏᴏᴜʀ ᴄᴏᴍғᴏʀᴛ ᴢᴏɴᴇ.</b>",
         "<b>❅ ᴀʟʟ ᴛʜᴇ ᴛʜɪɴɢs ᴛʜᴀᴛ ʜᴜʀᴛ ʏᴏᴜ, ᴀᴄᴛᴜᴀʟʟʏ ᴛᴇᴀᴄʜ ʏᴏᴜ.</b>",
         "<b>❅ ʟɪғᴇ ɪs ʟɪᴋᴇ ᴀ ᴄᴀᴍᴇʀᴀ. sᴏ ғᴀᴄᴇ ɪᴛ ᴡɪᴛʜ ᴀ sᴍɪʟᴇ.</b>",
         "<b>❅ ʟɪғᴇ ɪs 10% ᴏғ ᴡʜᴀᴛ ʜᴀᴘᴘᴇɴs ᴛᴏ ʏᴏᴜ ᴀɴᴅ 90% ᴏғ ʜᴏᴡ ʏᴏᴜ ʀᴇsᴘᴏɴᴅ ᴛᴏ ɪᴛ.</b>",
         "<b>❅ ʟɪғᴇ ᴀʟᴡᴀʏs ᴏғғᴇʀs ʏᴏᴜ ᴀ sᴇᴄᴏɴᴅ ᴄʜᴀɴᴄᴇ. ɪᴛ’s ᴄᴀʟʟᴇᴅ ᴛᴏᴍᴏʀʀᴏᴡ.</b>",
         "<b>❅ ɴᴏ ᴏɴᴇ ɪs ᴄᴏᴍɪɴɢ ᴛᴏ sᴀᴠᴇ ʏᴏᴜ. ᴛʜɪs ʟɪғᴇ ᴏғ ʏᴏᴜʀ ɪs 100% ʏᴏᴜʀ ʀᴇsᴘᴏɴsɪʙɪʟɪᴛʏ..</b>",
         "<b>❅ ʟɪғᴇ ɪs ɴᴏᴛ ᴀɴ ᴇᴀsʏ ᴛᴀsᴋ.</b>",
         "<b>❅ ʟɪғᴇ ɪs ᴀ ᴡᴏɴᴅᴇʀғᴜʟ ᴀᴅᴠᴇɴᴛᴜʀᴇ.</b>",
         "<b>❅ ʟɪғᴇ ʙᴇɢɪɴs ᴏɴ ᴛʜᴇ ᴏᴛʜᴇʀ sɪᴅᴇ ᴏғ ᴅᴇsᴘᴀɪʀ.</b>",
         "<b>❅ ʟɪғᴇ ɪs ɴᴏᴛ ᴀ ᴘʀᴏʙʟᴇᴍ ᴛᴏ ʙᴇ sᴏʟᴠᴇᴅ ʙᴜᴛ ᴀ ʀᴇᴀʟɪᴛʏ ᴛᴏ ʙᴇ ᴇxᴘᴇʀɪᴇɴᴄᴇᴅ.</b>",
         "<b>❅ ʟɪғᴇ ᴅᴏᴇs ɴᴏᴛ ʜᴀᴠᴇ ᴀ ʀᴇᴍᴏᴛᴇ; ɢᴇᴛ ᴜᴘ ᴀɴᴅ ᴄʜᴀɴɢᴇ ɪᴛ ʏᴏᴜʀsᴇʟғ.</b>",
         "<b>❅ sᴛᴀʀᴛ ᴛʀᴜsᴛɪɴɢ ʏᴏᴜʀsᴇʟғ, ᴀɴᴅ ʏᴏᴜ’ʟʟ ᴋɴᴏᴡ ʜᴏᴡ ᴛᴏ ʟɪᴠᴇ.</b>",
         "<b>❅ ʜᴇᴀʟᴛʜ ɪs ᴛʜᴇ ᴍᴏsᴛ ɪᴍᴘᴏʀᴛᴀɴᴛ ɢᴏᴏᴅ ᴏғ ʟɪғᴇ.</b>",
         "<b>❅ ᴛɪᴍᴇ ᴄʜᴀɴɢᴇ ᴘʀɪᴏʀɪᴛʏ ᴄʜᴀɴɢᴇs.</b>",
         "<b>❅ ᴛᴏ sᴇᴇ ᴀɴᴅ ᴛᴏ ғᴇᴇʟ ᴍᴇᴀɴs ᴛᴏ ʙᴇ, ᴛʜɪɴᴋ ᴀɴᴅ ʟɪᴠᴇ.</b>",
         "<b>❅ ʙᴇ ᴡɪᴛʜ sᴏᴍᴇᴏɴᴇ ᴡʜᴏ ʙʀɪɴɢs ᴏᴜᴛ ᴛʜᴇ ʙᴇsᴛ ᴏғ ʏᴏᴜ.</b>",
         "<b>❅ ʏᴏᴜʀ ᴛʜᴏᴜɢʜᴛs ᴀʀᴇ ʏᴏᴜʀ ʟɪғᴇ.</b>",
         "<b>❅ ᴘᴇᴏᴘʟᴇ ᴄʜᴀɴɢᴇ, ᴍᴇᴍᴏʀɪᴇs ᴅᴏɴ’ᴛ.</b>",
         "<b>❅ ᴏᴜʀ ʟɪғᴇ ɪs ᴡʜᴀᴛ ᴡᴇ ᴛʜɪɴᴋ ɪᴛ ɪs.</b>",
         "<b>❅ ʟɪɢʜᴛ ʜᴇᴀʀᴛ ʟɪᴠᴇs ʟᴏɴɢᴇʀ.</b>",
         "<b>❅ ᴅᴇᴘʀᴇssɪᴏɴ ᴇᴠᴇɴᴛᴜᴀʟʟʏ ʙᴇᴄᴏᴍᴇs ᴀ ʜᴀʙɪᴛ.</b>",
         "<b>❅ ʟɪғᴇ ɪs ᴀ ɢɪғᴛ. ᴛʀᴇᴀᴛ ɪᴛ ᴡᴇʟʟ.</b>",
         "<b>❅ ʟɪғᴇ ɪs ᴡʜᴀᴛ ᴏᴜʀ ғᴇᴇʟɪɴɢs ᴅᴏ ᴡɪᴛʜ ᴜs.</b>",
         "<b>❅ ᴡʀɪɴᴋʟᴇs ᴀʀᴇ ᴛʜᴇ ʟɪɴᴇs ᴏғ ʟɪғᴇ ᴏɴ ᴛʜᴇ ғᴀᴄᴇ.</b>",
         "<b>❅ ʟɪғᴇ ɪs ᴍᴀᴅᴇ ᴜᴘ ᴏғ sᴏʙs, sɴɪғғʟᴇs, ᴀɴᴅ sᴍɪʟᴇs.</b>",
         "<b>❅ ɴᴏᴛ ʟɪғᴇ, ʙᴜᴛ ɢᴏᴏᴅ ʟɪғᴇ, ɪs ᴛᴏ ʙᴇ ᴄʜɪᴇғʟʏ ᴠᴀʟᴜᴇᴅ.</b>",
         "**❅ ʏᴏᴜ ᴄʜᴀɴɢᴇ ʏᴏᴜʀ ʟɪғᴇ ʙʏ ᴄʜᴀɴɢɪɴɢ ʏᴏᴜʀ ʜᴇᴀʀᴛ.",
         "<b>❅ ʟɪғᴇ ɪs ɴᴏᴛʜɪɴɢ ᴡɪᴛʜᴏᴜᴛ ᴛʀᴜᴇ ғʀɪᴇɴᴅsʜɪᴘ.</b>",
         "<b>❅ ɪғ ʏᴏᴜ ᴀʀᴇ ʙʀᴀᴠᴇ ᴛᴏ sᴀʏ ɢᴏᴏᴅ ʙʏᴇ, ʟɪғᴇ ᴡɪʟʟ ʀᴇᴡᴀʀᴅ ʏᴏᴜ ᴡɪᴛʜ ᴀ ɴᴇᴡ ʜᴇʟʟᴏ.</b>",
         "<b>❅ ᴛʜᴇʀᴇ ɪs ɴᴏᴛʜɪɴɢ ᴍᴏʀᴇ ᴇxᴄɪᴛɪɴɢ ɪɴ ᴛʜᴇ ᴡᴏʀʟᴅ, ʙᴜᴛ ᴘᴇᴏᴘʟᴇ.</b>",
         "<b>❅ ʏᴏᴜ ᴄᴀɴ ᴅᴏ ᴀɴʏᴛʜɪɴɢ, ʙᴜᴛ ɴᴏᴛ ᴇᴠᴇʀʏᴛʜɪɴɢ.</b>",
         "<b>❅ ʟɪғᴇ ʙᴇᴄᴏᴍᴇ ᴇᴀsʏ ᴡʜᴇɴ ʏᴏᴜ ʙᴇᴄᴏᴍᴇ sᴛʀᴏɴɢ.</b>",
         "<b>❅ ᴍʏ ʟɪғᴇ ɪsɴ’ᴛ ᴘᴇʀғᴇᴄᴛ ʙᴜᴛ ɪᴛ ᴅᴏᴇs ʜᴀᴠᴇ ᴘᴇʀғᴇᴄᴛ ᴍᴏᴍᴇɴᴛs.</b>",
         "<b>❅ ʟɪғᴇ ɪs ɢᴏᴅ’s ɴᴏᴠᴇʟ. ʟᴇᴛ ʜɪᴍ ᴡʀɪᴛᴇ ɪᴛ.</b>",
         "<b>❅ ᴏᴜʀ ʟɪғᴇ ɪs ᴀ ʀᴇsᴜʟᴛ ᴏғ ᴏᴜʀ ᴅᴏᴍɪɴᴀɴᴛ ᴛʜᴏᴜɢʜᴛs.</b>",
         "<b>❅ ʟɪғᴇ ɪs ᴀ ᴍᴏᴛɪᴏɴ ғʀᴏᴍ ᴀ ᴅᴇsɪʀᴇ ᴛᴏ ᴀɴᴏᴛʜᴇʀ ᴅᴇsɪʀᴇ.</b>",
         "<b>❅ ᴛᴏ ʟɪᴠᴇ ᴍᴇᴀɴs ᴛᴏ ғɪɢʜᴛ.</b>",
         "<b>❅ ʟɪғᴇ ɪs ʟɪᴋᴇ ᴀ ᴍᴏᴜɴᴛᴀɪɴ, ɴᴏᴛ ᴀ ʙᴇᴀᴄʜ.</b>",
         "<b>❅ ᴛʜᴇ ᴡᴏʀsᴛ ᴛʜɪɴɢ ɪɴ ʟɪғᴇ ɪs ᴛʜᴀᴛ ɪᴛ ᴘᴀssᴇs.</b>",
         "<b>❅ ʟɪғᴇ ɪs sɪᴍᴘʟᴇ ɪғ ᴡᴇ ᴀʀᴇ sɪᴍᴘʟᴇ.</b>",
         "<b>❅ ᴀʟᴡᴀʏs ᴛʜɪɴᴋ ᴛᴡɪᴄᴇ, sᴘᴇᴀᴋ ᴏɴᴄᴇ.</b>",
         "<b>❅ ʟɪғᴇ ɪs sɪᴍᴘʟᴇ, ᴡᴇ ᴍᴀᴋᴇ ɪᴛ ᴄᴏᴍᴘʟɪᴄᴀᴛᴇᴅ.</b>",
         "<b>❅ ʟɪғᴇ ɪs ɴᴏᴛ ᴍᴜᴄʜ ᴏʟᴅᴇʀ ᴛʜᴀɴ ᴛʜᴇ ᴅᴇᴀᴛʜ.</b>",
         "<b>❅ ᴛʜᴇ sᴇᴄʀᴇᴛ ᴏғ ʟɪғᴇ ɪs ʟᴏᴡ ᴇxᴘᴇᴄᴛᴀᴛɪᴏɴs!</b>",
         "<b>❅ ʟɪғᴇ ɪs ᴀ ᴛᴇᴀᴄʜᴇʀ..,ᴛʜᴇ ᴍᴏʀᴇ ᴡᴇ ʟɪᴠᴇ, ᴛʜᴇ ᴍᴏʀᴇ ᴡᴇ ʟᴇᴀʀɴ.</b>",
         "<b>❅ ʜᴜᴍᴀɴ ʟɪғᴇ ɪs ɴᴏᴛʜɪɴɢ ʙᴜᴛ ᴀɴ ᴇᴛᴇʀɴᴀʟ ɪʟʟᴜsɪᴏɴ.</b>",
         "<b>❅ ᴛʜᴇ ʜᴀᴘᴘɪᴇʀ ᴛʜᴇ ᴛɪᴍᴇ, ᴛʜᴇ sʜᴏʀᴛᴇʀ ɪᴛ ɪs.</b>",
         "<b>❅ ʟɪғᴇ ɪs ʙᴇᴀᴜᴛɪғᴜʟ ɪғ ʏᴏᴜ  ᴋɴᴏᴡ ᴡʜᴇʀᴇ ᴛᴏ ʟᴏᴏᴋ.</b>",
         "<b>❅ ʟɪғᴇ ɪs ᴀᴡᴇsᴏᴍᴇ ᴡɪᴛʜ ʏᴏᴜ ʙʏ ᴍʏ sɪᴅᴇ.</b>",
         "<b>❅ ʟɪғᴇ – ʟᴏᴠᴇ = ᴢᴇʀᴏ</b>",
         "<b>❅ ʟɪғᴇ ɪs ғᴜʟʟ ᴏғ sᴛʀᴜɢɢʟᴇs.</b>",
         "<b>❅ ɪ ɢᴏᴛ ʟᴇss ʙᴜᴛ ɪ ɢᴏᴛ ʙᴇsᴛ </b>",
         "<b>❅ ʟɪғᴇ ɪs 10% ᴡʜᴀᴛ ʏᴏᴜ ᴍᴀᴋᴇ ɪᴛ, ᴀɴᴅ 90% ʜᴏᴡ ʏᴏᴜ ᴛᴀᴋᴇ ɪᴛ.</b>",
         "<b>❅ ᴛʜᴇʀᴇ ɪs sᴛɪʟʟ sᴏ ᴍᴜᴄʜ ᴛᴏ sᴇᴇ</b>",
         "<b>❅ ʟɪғᴇ ᴅᴏᴇsɴ’ᴛ ɢᴇᴛ ᴇᴀsɪᴇʀ ʏᴏᴜ ɢᴇᴛ sᴛʀᴏɴɢᴇʀ.</b>",
         "<b>❅ ʟɪғᴇ ɪs ᴀʙᴏᴜᴛ ʟᴀᴜɢʜɪɴɢ & ʟɪᴠɪɴɢ.</b>",
         "<b>❅ ᴇᴀᴄʜ ᴘᴇʀsᴏɴ ᴅɪᴇs ᴡʜᴇɴ ʜɪs ᴛɪᴍᴇ ᴄᴏᴍᴇs.</b>",
        ]


async def _tag_members(client, message, reply_message, templates):
    chat_id = message.chat.id
    spam_chats.append(chat_id)
    try:
        async for usr in client.get_chat_members(chat_id):
            if chat_id not in spam_chats:
                break
            user = usr.user
            if not user or user.is_bot or user.is_deleted:
                continue
            name = escape(user.first_name or "User")
            mention = f"<a href='tg://user?id={user.id}'>{name}</a>"
            if reply_message:
                await reply_message.reply(
                    f"{mention} {random.choice(templates)}",
                    parse_mode=ParseMode.HTML,
                )
            else:
                await client.send_message(
                    chat_id,
                    f"{mention} {random.choice(templates)}",
                    parse_mode=ParseMode.HTML,
                )
            await asyncio.sleep(4)
    finally:
        if chat_id in spam_chats:
            spam_chats.remove(chat_id)


@app.on_message(filters.command(["hitag" ], prefixes=["/", "@", "#"]))
async def mentionall(client, message):
    chat_id = message.chat.id
    if message.chat.type == ChatType.PRIVATE:
        return await message.reply("๏ ᴛʜɪs ᴄᴏᴍᴍᴀɴᴅ ᴏɴʟʏ ғᴏʀ ɢʀᴏᴜᴘs.")
    if not message.from_user:
        return

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
        return await message.reply("๏ ʏᴏᴜ ᴀʀᴇ ɴᴏᴛ ᴀᴅᴍɪɴ ʙᴀʙʏ, ᴏɴʟʏ ᴀᴅᴍɪɴs ᴄᴀɴ ᴛᴀɢ ᴍᴇᴍʙᴇʀs. ")

    if message.reply_to_message:
        mode = "text_on_reply"
        msg = message.reply_to_message
    elif len(message.command) > 1:
        mode = "text_on_cmd"
        msg = message.text
    else:
        return await message.reply("/hitag ɢᴏᴏᴅ ᴍᴏʀɴɪɴɢ ᴛʏᴘᴇ ʟɪᴋᴇ ᴛʜɪs / ʀᴇᴘʟʏ ᴀɴʏ ᴍᴇssᴀɢᴇ ɴᴇxᴛ ᴛɪᴍᴇ ʙᴏᴛ ᴛᴀɢɢɪɴɢ...")
    if chat_id in spam_chats:
        return await message.reply("๏ ᴘʟᴇᴀsᴇ ᴀᴛ ғɪʀsᴛ sᴛᴏᴘ ʀᴜɴɴɪɴɢ ᴍᴇɴᴛɪᴏɴ ᴘʀᴏᴄᴇss...")
    await _tag_members(
        client,
        message,
        msg if mode == "text_on_reply" else None,
        EMOJI if mode == "text_on_reply" else TAGMES,
    )


@app.on_message(filters.command(["lifetag"], prefixes=["/", "@", "#"]))
async def mention_allvc(client, message):
    chat_id = message.chat.id
    if message.chat.type == ChatType.PRIVATE:
        return await message.reply("๏ ᴛʜɪs ᴄᴏᴍᴍᴀɴᴅ ᴏɴʟʏ ғᴏʀ ɢʀᴏᴜᴘs.")
    if not message.from_user:
        return

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
        return await message.reply("๏ ʏᴏᴜ ᴀʀᴇ ɴᴏᴛ ᴀᴅᴍɪɴ ʙᴀʙʏ, ᴏɴʟʏ ᴀᴅᴍɪɴs ᴄᴀɴ ᴛᴀɢ ᴍᴇᴍʙᴇʀs. ")
    if chat_id in spam_chats:
        return await message.reply("๏ ᴘʟᴇᴀsᴇ ᴀᴛ ғɪʀsᴛ sᴛᴏᴘ ʀᴜɴɴɪɴɢ ᴍᴇɴᴛɪᴏɴ ᴘʀᴏᴄᴇss...")
    await _tag_members(client, message, None, VC_TAG)



@app.on_message(filters.command(["histop", "lifestop", "hicancel"]) & filters.group)
async def cancel_spam(client, message):
    if not message.from_user:
        return
    if not message.chat.id in spam_chats:
        return await message.reply("๏ ᴄᴜʀʀᴇɴᴛʟʏ ɪ'ᴍ ɴᴏᴛ ᴛᴀɢɢɪɴɢ ʙᴀʙʏ.")
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
        return await message.reply("๏ ʏᴏᴜ ᴀʀᴇ ɴᴏᴛ ᴀᴅᴍɪɴ ʙᴀʙʏ, ᴏɴʟʏ ᴀᴅᴍɪɴs ᴄᴀɴ ᴛᴀɢ ᴍᴇᴍʙᴇʀs.")
    else:
        try:
            spam_chats.remove(message.chat.id)
        except:
            pass
        return await message.reply("๏ ᴍᴇɴᴛɪᴏɴ ᴘʀᴏᴄᴇss sᴛᴏᴘᴘᴇᴅ ๏")
