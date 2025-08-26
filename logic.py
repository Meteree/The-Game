from discord import ui, ButtonStyle

class Question:
    def __init__(self, id, text, answer_id, options, next_questions, reward=None):
        self.id = id
        self.text = text
        self.answer_id = answer_id          # Basitlik için kullanılmıyor
        self.options = options
        self.next_questions = next_questions
        self.reward = reward

    def gen_buttons(self):
        buttons = []
        for i, option in enumerate(self.options):
            style = ButtonStyle.primary
            custom_id = f"{self.id}_{i}"
            buttons.append(ui.Button(label=option, style=style, custom_id=custom_id))
        return buttons


# ======================================
#         BORIS – HİKÂYE AKIŞI
# ======================================

quiz_questions = {
    # ----------------- BAŞLANGIÇ -----------------
    "start": Question(
        id="start",
        text=(
            "Bir zamanlar Boris adında bir şövalye varmış. Prens, babası olan kralı gizli bir suikastle öldürüp "
            "tahtı ele geçirmiş. Krallık karanlığa gömülmüş. Boris intikam yemini etti…\n\n"
            "Yol ayrımındasın. Nereye gideceksin?"
        ),
        answer_id=0,
        options=["🌲 Ormana gir", "🛒 Markete uğra", "🕳️ Bataklığa sap", "🏰 Kale yoluna çık"],
        next_questions=["orman", "market", "bataklik", "kale_yolu"]
    ),

    # ----------------- MARKET -----------------
    "market": Question(
        id="market",
        text="Pazar yeri gergin. Fısıltılar arasında üç dükkân açık kalmış.",
        answer_id=0,
        options=["⚒️ Demirciye git", "🌿 Şifacıya git", "💰 Tüccara git", "↩️ Geri dön"],
        next_questions=["demirci", "sifaci", "tuccar", "start"]
    ),

    # Demirci → seçim, ardından ödül düğümleri
    "demirci": Question(
        id="demirci",
        text="Demirci: “Prense karşı çıkıyorsan iyi bir silaha ihtiyacın var.”",
        answer_id=0,
        options=["🪓 ***Balta al***", "🛡️ ***Zırh al***", "🔱 ***Mızrak al***", "↩️ Geri dön"],
        next_questions=["balta_al", "zirh_al", "mizrak_al", "market"]
    ),
    "balta_al": Question(
        id="balta_al",
        text="Ağır ama yıkıcı bir balta aldın.",
        answer_id=0,
        options=["↩️ Başlangıca dön"],
        next_questions=["start"],
        reward="🪓 ***Balta***"
    ),
    "zirh_al": Question(
        id="zirh_al",
        text="Demirci sana sağlam bir göğüslük verdi.",
        answer_id=0,
        options=["↩️ Başlangıca dön"],
        next_questions=["start"],
        reward="🛡️ ***Zırh***"
    ),
    "mizrak_al": Question(
        id="mizrak_al",
        text="Uzun menzilli bir mızrak seçtin.",
        answer_id=0,
        options=["↩️ Başlangıca dön"],
        next_questions=["start"],
        reward="🔱 ***Mızrak***"
    ),

    # Şifacı
    "sifaci": Question(
        id="sifaci",
        text="Şifacı: “Yolun zor olacak. Bir iksir hayat kurtarır.”",
        answer_id=0,
        options=["🧪 Şifa iksiri al", "↩️ Geri dön"],
        next_questions=["sifa_iksiri_al", "market"]
    ),
    "sifa_iksiri_al": Question(
        id="sifa_iksiri_al",
        text="Şifa iksirini çantana attın.",
        answer_id=0,
        options=["↩️ Başlangıca dön"],
        next_questions=["start"],
        reward="🧪 Şifa İksiri"
    ),

    # Tüccar
    "tuccar": Question(
        id="tuccar",
        text="Tüccar fısıldıyor: “Prensin günleri sayılı… doğru eşyayla.”",
        answer_id=0,
        options=["🏹 ***Ok & yay al***", "💪 🧪 Kuvvet iksiri al", "💰 🧪 Ganimet iksiri al", "↩️ Geri dön"],
        next_questions=["okyay_al", "kuvvet_iksiri_al", "ganimet_iksiri_al", "market"]
    ),
    "okyay_al": Question(
        id="okyay_al",
        text="Keskin uçlu oklar ve sağlam bir yay aldın.",
        answer_id=0,
        options=["↩️ Başlangıca dön"],
        next_questions=["start"],
        reward="🏹 ***Ok & Yay***"
    ),
    "kuvvet_iksiri_al": Question(
        id="kuvvet_iksiri_al",
        text="Kuvvet iksiri kaslarını yakıyor.",
        answer_id=0,
        options=["↩️ Başlangıca dön"],
        next_questions=["start"],
        reward="💪 🧪 Kuvvet İksiri"
    ),
    "ganimet_iksiri_al": Question(
        id="ganimet_iksiri_al",
        text="Ganimet iksiri şansını arttıracak gibi.",
        answer_id=0,
        options=["↩️ Başlangıca dön"],
        next_questions=["start"],
        reward="💰 🧪 Ganimet İksiri"
    ),

    # ----------------- ORMAN -----------------
    "orman": Question(
        id="orman",
        text="Orman uğursuz. Dallar arasında tıkırtılar…",
        answer_id=0,
        options=["👹 Goblinlerle yüzleş", "⚔️ ***Kılıç ara***", "🪖 Devriye askerlerinden sakın", "↩️ Geri dön"],
        next_questions=["goblinler", "kilic_bul", "asker_devriyesi", "start"]
    ),
    "goblinler": Question(
        id="goblinler",
        text="Bir grup goblin yolunu kesti!",
        answer_id=0,
        options=["⚔️ Saldır", "🛡️ Savun ve geri püskürt", "🧪 İksiri kullan", "🏃 Kaç"],
        next_questions=["zindan_girisi", "zindan_girisi", "zindan_girisi", "start"]
    ),
    "kilic_bul": Question(
        id="kilic_bul",
        text="Yosunlar arasında eski ama dengeli bir kılıç buldun.",
        answer_id=0,
        options=["🏰 Kale yoluna çık", "↩️ Başlangıca dön"],
        next_questions=["kale_yolu", "start"],
        reward="⚔️ ***Kılıç***"
    ),
    "asker_devriyesi": Question(
        id="asker_devriyesi",
        text="Prensin askerleri ormanı devriye geziyor. Çatışmayı atlattın.",
        answer_id=0,
        options=["🛡️ Kale yoluna sız", "↩️ Başlangıca dön"],
        next_questions=["kale_yolu", "start"]
    ),

    # ----------------- BATAKLIK -----------------
    "bataklik": Question(
        id="bataklik",
        text="Bataklıkta sis çökmüş. Suların içinden bir yılan süzülüyor.",
        answer_id=0,
        options=["🐍 Yılanla karşılaş", "🛡️ ***Kalkan ara***", "↩️ Geri dön"],
        next_questions=["yilan", "kalkan_bul", "start"]
    ),
    "yilan": Question(
        id="yilan",
        text="Dev bataklık yılanı aniden saldırıyor!",
        answer_id=0,
        options=["⚔️ Saldır", "🛡️ Savun", "🧪 İksiri kullan"],
        next_questions=["kalkan_bul", "kalkan_bul", "kalkan_bul"]
    ),
    "kalkan_bul": Question(
        id="kalkan_bul",
        text="Batmış bir şövalyenin kalkanını çıkardın.",
        answer_id=0,
        options=["↩️ Başlangıca dön"],
        next_questions=["start"],
        reward="🛡️ ***Kalkan***"
    ),

    # ----------------- KALE YOLU / ZİNDAN / KUYU -----------------
    "kale_yolu": Question(
        id="kale_yolu",
        text="Kale göründü. Kapılar ağır, muhafız çok.",
        answer_id=0,
        options=["🕳️ Zindana sız", "💧 Kuyudan dolaş", "🏰 Doğrudan kaleye yaklaş", "↩️ Geri dön"],
        next_questions=["zindan_girisi", "kuyu", "kale_kapisi", "start"]
    ),
    "kuyu": Question(
        id="kuyu",
        text="Eski bir kuyu buldun. Derin ama altı koridor gibi.",
        answer_id=0,
        options=["🪢 İple in", "❌ Vazgeç"],
        next_questions=["zindan_ic", "kale_yolu"]
    ),
    "zindan_girisi": Question(
        id="zindan_girisi",
        text="Zindanın rutubetli kapısındasın. İçeriden inlemeler geliyor.",
        answer_id=0,
        options=["👹 Goblin bekçileri atlat", "🧟 Zombi geçidinden sız", "↩️ Geri dön"],
        next_questions=["labirent_1", "labirent_1", "kale_yolu"]
    ),
    "zindan_ic": Question(
        id="zindan_ic",
        text="Kuyudan zindanın içine indin ve bir geçide çıktın.",
        answer_id=0,
        options=["🗺️ ***Labirente gir***"],
        next_questions=["labirent_1"],
        reward="🗺️ ***Labirent Haritası***"
    ),
    "kale_kapisi": Question(
        id="kale_kapisi",
        text="Kapı önünde askerler. Bir açık yakalayıp içeri süzüldün.",
        answer_id=0,
        options=["🚪 Labirente açılan salona ilerle"],
        next_questions=["labirent_1"]
    ),

    # ----------------- LABİRENT (kısa zincir) -----------------
    "labirent_1": Question(
        id="labirent_1",
        text="Labirent başlıyor: Fısıldayan taş duvarlar.",
        answer_id=0,
        options=["➡️ Sağ geçit", "⬅️ Sol geçit"],
        next_questions=["labirent_2", "labirent_3"]
    ),
    "labirent_2": Question(
        id="labirent_2",
        text="Bir meşale buldun. Gölge uzuyor.",
        answer_id=0,
        options=["➡️ İleri", "↩️ Geri dön ve diğer yolu dene"],
        next_questions=["labirent_4", "labirent_3"]
    ),
    "labirent_3": Question(
        id="labirent_3",
        text="Döşemede gevşek bir taş. Tuzaktan sıyrıldın.",
        answer_id=0,
        options=["➡️ İleri"],
        next_questions=["labirent_4"]
    ),
    "labirent_4": Question(
        id="labirent_4",
        text="Uzakta bir kapı. Üzerinde prensin mührü.",
        answer_id=0,
        options=["➡️ Devam et"],
        next_questions=["labirent_5"]
    ),
    "labirent_5": Question(
        id="labirent_5",
        text="Son koridor. Nöbetçiler uzaklaştı.",
        answer_id=0,
        options=["👑 Taht odasına yaklaş"],
        next_questions=["throne_room"]
    ),

    # ----------------- TAHT ODASI – FİNAL -----------------
    "throne_room": Question(
        id="throne_room",
        text=(
            "Taht odası! Prens karanlık zırhıyla gülümsüyor:\n"
            "“Boris… sonunda.”\n"
            "Seçimini yap!"
        ),
        answer_id=0,
        options=["⚔️ Saldır", "🛡️ Savun", "🧪 İksiri kullan"],
        next_questions=["ending_victory", "ending_captured", "ending_clutch"]
    ),

    # Sonlar (next_questions = [None] → oyun biter)
    "ending_victory": Question(
        id="ending_victory",
        text="Boris kılıcını indirir. Prensin saltanatı son bulur. Halk özgürleşir.",
        answer_id=0,
        options=["🏁 Bitir"],
        next_questions=[None],
        reward="👑 ***Prensin Mührü***"
    ),
    "ending_captured": Question(
        id="ending_captured",
        text="Boris savunmaya çekilir; askerler odaya dolar. Karanlık demirler kapanır…",
        answer_id=0,
        options=["🏁 Bitir"],
        next_questions=[None]
    ),
    "ending_clutch": Question(
        id="ending_clutch",
        text="İksir damarlarında alev olur. Son hamleyle prensi alt edersin!",
        answer_id=0,
        options=["🏁 Bitir"],
        next_questions=[None],
        reward="🔑 ***Tahtın Anahtarı***"
    ),
}
