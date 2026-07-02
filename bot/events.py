from datetime import datetime
from zoneinfo import ZoneInfo

from .models import WeddingEvent


def build_event(
    timezone: ZoneInfo,
    title: str,
    year: int,
    month: int,
    day: int,
    hour: int,
    minute: int,
    message: str,
) -> WeddingEvent:
    return WeddingEvent(
        title=title,
        start=datetime(year, month, day, hour, minute, tzinfo=timezone),
        message=message,
    )


def get_events(timezone: ZoneInfo) -> list[WeddingEvent]:
    return [
        build_event(
            timezone,
            "Parents Veiling & Shu Tou",
            2026,
            7,
            3,
            21,
            0,
            "Tonight begins with Parents Veiling & Shu Tou (父母盖头与上头), a meaningful pre-wedding blessing ritual. "
            "Ann Qi and Yi Long, please make sure the required ritual items are ready, family members have arrived, "
            "and the photographer knows the best positions for blessing and family shots. Bride's parents will veil Ann Qi "
            "and perform Shu Tou, so keep the space calm, tidy, and photo-ready.",
        ),
        build_event(
            timezone,
            "Bridal Makeup & Morning Prep",
            2026,
            7,
            4,
            4,
            30,
            "Good morning — it is time for Bridal Makeup & Morning Prep. Ann Qi starts makeup now. Bridesmaids arrive at "
            "05:30 to prepare gatecrash games, and the photographer/videographer arrive at 05:45 for setup and blessing shots. "
            "Mee Sua (面线) preparation also begins now. Frankel, please act as house liaison and backup AV, and help confirm "
            "the door area and morning logistics.",
        ),
        build_event(
            timezone,
            "Bridesmaids Arrive at Bride's Home",
            2026,
            7,
            4,
            5,
            30,
            "Bridesmaids, please arrive at the bride's home now and begin setting up the gatecrash games. Confirm props, "
            "game order, door area, and who will communicate with the groom's side. Keep the setup efficient so the morning "
            "timeline stays on track.",
        ),
        build_event(
            timezone,
            "Groom & Groomsmen Arrive / Open the Door",
            2026,
            7,
            4,
            6,
            45,
            "Yi Long and groomsmen, you are due to arrive at the bride's home at 06:45. Yi Long, please make sure you have "
            "the bouquet with you. Frankel, please open the door at 06:45 sharp so the gatecrash can start on time.",
        ),
        build_event(
            timezone,
            "Gatecrash Begins",
            2026,
            7,
            4,
            6,
            45,
            "Gatecrash (接亲) begins soon. Yi Long, be ready for the games and the 10 promises at the door. Bridesmaids, keep "
            "the flow lively but controlled. Photographer and videographer, please capture the key moments clearly. Everyone, "
            "the hard finish target is 07:30. Frankel, please maintain door-to-inside communication, manage crowd flow, and "
            "support backup AV if needed.",
        ),
        build_event(
            timezone,
            "Mee Sua Ceremony",
            2026,
            7,
            4,
            7,
            40,
            "Mee Sua Ceremony (面线仪式) is coming up. Ann Qi and Yi Long will eat mee sua together and bow to the deities, "
            "parents, and each other. Bride's parents, please prepare your blessing words — this is short but meaningful. "
            "Items needed: mee sua and bridal veil. Photographer, please capture the bowing, blessings, and family photo moments.",
        ),
        build_event(
            timezone,
            "Red Umbrella Send-Off — Leave Bride's Home",
            2026,
            7,
            4,
            8,
            10,
            "Red Umbrella Send-Off (红伞送嫁) is about to begin. The bride's father will hold the red umbrella and walk Ann Qi "
            "out, with both parents sending her off at the door. Please prepare the red umbrella, fan, portable fan, and vehicles. "
            "Remember to toss the red umbrella as Ann Qi exits. Hard deadline: leave by 08:15 and reach the groom's home by 09:00. "
            "Frankel, please confirm all items are ready and keep the door area clear.",
        ),
        build_event(
            timezone,
            "Groom's Family Tang Yuan & Tea Ceremony",
            2026,
            7,
            4,
            9,
            0,
            "Please arrive at the groom's home / Ah Gong's house by 09:00 sharp: 536 Bedok North Street 3, #08-874. "
            "Yi Long opens the door for Ann Qi. Sweet soup — tang yuan, longan, red dates, lotus seeds, and egg — will be served, "
            "symbolising a sweet and fruitful marriage. The tea ceremony with Yi Long's immediate family follows.",
        ),
        build_event(
            timezone,
            "Return to Bride's Home",
            2026,
            7,
            4,
            9,
            40,
            "It is nearly time to return to the bride's home. Before leaving the groom's home, Ann Qi should change into the Kua (褂). "
            "Please make sure the Kua and hair accessories are already at Yi Long's home. Jin Long and Shi Qi, please coordinate transport.",
        ),
        build_event(
            timezone,
            "Bride's Family Tea Ceremony",
            2026,
            7,
            4,
            10,
            0,
            "Bride's Family Tea Ceremony (新娘家敬茶) begins soon at 178B Rivervale Crescent, #05-431, S542178. AQ relatives will arrive. "
            "Bridal party, please help parents prepare tea and space, pass teacups, collect red packets, and set up food outside. "
            "Ask a senior family member to stand by and call out names in order. Frankel, please coordinate the buffet vendor, ensure food "
            "arrives on time, and act as house liaison and backup AV.",
        ),
        build_event(
            timezone,
            "Wedding Party Photo & Lunch",
            2026,
            7,
            4,
            11,
            0,
            "Wedding party photos are coming up downstairs / at the playground. After photos, food arrives at the bride's home around 11:30, "
            "followed by lunch and rest from 12:00. Frankel, please continue supporting guest and logistics coordination.",
        ),
        build_event(
            timezone,
            "Check-In at Changi Crowne Plaza",
            2026,
            7,
            4,
            12,
            30,
            "Hotel check-in is coming up at Changi Crowne Plaza, 75 Airport Blvd., #01-01, Singapore 819664. Couple, please confirm who is "
            "heading to the hotel after lunch. There are 2 VIP parking spots available. Frankel, please assist with family communication and "
            "item handover during the venue transition if needed.",
        ),
        build_event(
            timezone,
            "Second Round of Hair & Makeup",
            2026,
            7,
            4,
            13,
            45,
            "Second round of hair and makeup is about to start. Ann Qi begins makeup around 13:45–14:00, Yi Long does a light touch-up, "
            "and both mothers should begin makeup in the bridal suite now. Please keep outfits and accessories ready.",
        ),
        build_event(
            timezone,
            "Set Up Reception Table & Solemnisation Area",
            2026,
            7,
            4,
            16,
            0,
            "Reception table and solemnisation area setup begins soon. Bridal party, please coordinate with the hotel on the solemnisation, "
            "tea ceremony, and reception areas. Hotel provides the easel stand and 1 fish bowl; video guestbook vendor arrives at 17:30. "
            "Frankel, please help Sue Huei, Bei Bei, Shuang Jie, Joyce, Serene, and Jiong Hao with the welcome area setup.",
        ),
        build_event(
            timezone,
            "Pre-Banquet Coordinator Briefing",
            2026,
            7,
            4,
            16,
            30,
            "Pre-banquet coordinator briefing is coming up. Please confirm parking vouchers, seating, and table placement with the banquet manager. "
            "Prepare photographer/videographer meals and confirm no beef. Frankel, please sync on AV or guest flow if you are involved.",
        ),
        build_event(
            timezone,
            "Couple Photoshoot at Changi Crowne",
            2026,
            7,
            4,
            16,
            30,
            "Couple photoshoot at Changi Crowne is starting soon. Photographer arrives at 16:30. Get ready for first-look photos with bridesmaids "
            "and mothers, then photos around Changi Crowne Plaza. Please keep the couple's outfits, bouquet, and touch-up items nearby.",
        ),
        build_event(
            timezone,
            "Solemnisation Ceremony",
            2026,
            7,
            4,
            17,
            10,
            "Solemnisation Ceremony (证婚仪式) is coming up in Hopea Room. Dr William Chung Tang Fong arrives at 17:10 to verify documents; "
            "ceremony begins around 17:20. Please prepare the ROM marriage certificate and original IC/passport for both the couple and both witness fathers. "
            "Ann Qi will walk in with both parents. If possible, arrange visitor parking for the officiant, car plate SJP 80 R.",
        ),
        build_event(
            timezone,
            "Groom's Family Tea Ceremony at Hotel",
            2026,
            7,
            4,
            17,
            30,
            "Groom's Family Tea Ceremony at the hotel (男方敬茶) begins soon at Chengal Room / hotel tea area. Bridal party, please set up tea equipment; "
            "Joyce, Shuang Jie, and helpers, please assist. Bring disposable teacups. Follow the prepared family order for Yi Long's dad's and mum's sides.",
        ),
        build_event(
            timezone,
            "Banquet Guest Reception",
            2026,
            7,
            4,
            18,
            0,
            "Banquet guest reception (晚宴迎宾) begins soon. Guests start arriving at 18:00, banquet hall opens at 18:30, and doors close at 19:00. "
            "At 19:00, food/drinks outside stop, the red packet box should be taken upstairs and locked in the safe, room key passed to Sue Huei and Jiong Hao, "
            "and fish bowl kept by AV and emcee. Frankel, please lead reception with Sue Huei, Bei Bei, and Shuang Jie, and help guests find registration, seats, and key contacts.",
        ),
        build_event(
            timezone,
            "First Grand Entrance",
            2026,
            7,
            4,
            19,
            15,
            "First Grand Entrance (第一次进场) is coming up. Emcee will cue, AV plays the video montage, and the couple enters to Canon in D. Cake cutting follows. "
            "Frankel, please stand by as backup AV and assist Mason if needed.",
        ),
        build_event(
            timezone,
            "SDE Screening",
            2026,
            7,
            4,
            20,
            35,
            "SDE (Same-Day Edit) screening is coming up. The SDE is expected to be ready about 30 minutes after the first entrance. Couple, please wait outside. "
            "Bridal party should exit mid-SDE to prepare for the second entrance. Backup plan: if SDE is not ready, screen it after Yam Seng. Frankel, please coordinate with the emcee and videographer.",
        ),
        build_event(
            timezone,
            "Second Grand Entrance",
            2026,
            7,
            4,
            20,
            40,
            "Second Grand Entrance (第二次进场) is about to happen. Bridal party enters to Fireworks music. Paper planes should be tossed throughout, with the full crowd toss "
            "during the couple's dip kiss. Frankel, please sync with music, reel, and emcee cues as backup AV.",
        ),
        build_event(
            timezone,
            "Champagne Tower & Yam Seng",
            2026,
            7,
            4,
            20,
            50,
            "Champagne Tower & Yam Seng (香槟塔) is next. Couple, please go straight to the stage, pour champagne, do the lover's toast, then Yam Seng. "
            "AV should return to Spotify/loop music after the couple takes the stage. Frankel, continue backup AV support; if SDE was delayed, help schedule it after Yam Seng.",
        ),
        build_event(
            timezone,
            "Thank You Speech",
            2026,
            7,
            4,
            21,
            0,
            "Thank You Speech (致谢词) is coming up. Ann Qi and Yi Long, please prepare to deliver your speech. VIP table service resumes after the speech. "
            "If doing a live Telegram call for remote feed, Frankel please stand by for live feed or mic-passing support.",
        ),
        build_event(
            timezone,
            "Table-by-Table Photo & Lucky Draw",
            2026,
            7,
            4,
            22,
            20,
            "Table-by-table photos and lucky draw are coming up. There are about 24 tables, estimated around 1 hour of photos. Bridal party, please notify each table in advance. "
            "Lucky draw starts around 22:30 with $5 and $10 prize rounds. Frankel, please help coordinate family tables.",
        ),
        build_event(
            timezone,
            "End of Banquet & Guest Send-Off",
            2026,
            7,
            4,
            22,
            30,
            "End of Banquet & Guest Send-Off (晚宴结束与送客) is coming up. Emcee will announce the end of the banquet. Couple and both sets of parents should send guests off together. "
            "Target: dessert served before 22:00. Yi Long's family takes home the reception photo. Frankel, please assist with wrap-up, item handover, and family coordination.",
        ),
    ]
