import asyncio
import logging
from dataclasses import dataclass
from datetime import datetime, timedelta
from zoneinfo import ZoneInfo

from telegram import Bot
from telegram.constants import ParseMode


# Telegram settings
BOT_TOKEN = "8234973225:AAFQu7sXukmfph-sbjpte1iDbE4QL42XaZY"
RAW_CHANNEL_ID = "562953664827933"
CHANNEL_ID = f"-100{RAW_CHANNEL_ID}"

# All wedding times are Singapore time.
SGT = ZoneInfo("Asia/Singapore")
REMINDER_OFFSET = timedelta(minutes=10)

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(message)s",
)
logger = logging.getLogger(__name__)


@dataclass(frozen=True)
class WeddingEvent:
    title: str
    start: datetime
    message: str

    @property
    def reminder_time(self) -> datetime:
        return self.start - REMINDER_OFFSET


EVENTS = [
    WeddingEvent(
        title="Parents Veiling & Shu Tou",
        start=datetime(2026, 7, 3, 21, 0, tzinfo=SGT),
        message=(
            "Tonight begins with Parents Veiling & Shu Tou (父母盖头与上头), a meaningful pre-wedding blessing ritual. "
            "Ann Qi and Yi Long, please make sure the required ritual items are ready, family members have arrived, "
            "and the photographer knows the best positions for blessing and family shots. Bride's parents will veil Ann Qi "
            "and perform Shu Tou, so keep the space calm, tidy, and photo-ready."
        ),
    ),
    WeddingEvent(
        title="Bridal Makeup & Morning Prep",
        start=datetime(2026, 7, 4, 4, 30, tzinfo=SGT),
        message=(
            "Good morning — it is time for Bridal Makeup & Morning Prep. Ann Qi starts makeup now. Bridesmaids arrive at "
            "05:30 to prepare gatecrash games, and the photographer/videographer arrive at 05:45 for setup and blessing shots. "
            "Mee Sua (面线) preparation also begins now. Frankel, please act as house liaison and backup AV, and help confirm "
            "the door area and morning logistics."
        ),
    ),
    WeddingEvent(
        title="Bridesmaids Arrive at Bride's Home",
        start=datetime(2026, 7, 4, 5, 30, tzinfo=SGT),
        message=(
            "Bridesmaids, please arrive at the bride's home now and begin setting up the gatecrash games. Confirm props, "
            "game order, door area, and who will communicate with the groom's side. Keep the setup efficient so the morning "
            "timeline stays on track."
        ),
    ),
    WeddingEvent(
        title="Groom & Groomsmen Arrive / Open the Door",
        start=datetime(2026, 7, 4, 6, 45, tzinfo=SGT),
        message=(
            "Yi Long and groomsmen, you are due to arrive at the bride's home at 06:45. Yi Long, please make sure you have "
            "the bouquet with you. Frankel, please open the door at 06:45 sharp so the gatecrash can start on time."
        ),
    ),
    WeddingEvent(
        title="Gatecrash Begins",
        start=datetime(2026, 7, 4, 6, 45, tzinfo=SGT),
        message=(
            "Gatecrash (接亲) begins soon. Yi Long, be ready for the games and the 10 promises at the door. Bridesmaids, keep "
            "the flow lively but controlled. Photographer and videographer, please capture the key moments clearly. Everyone, "
            "the hard finish target is 07:30. Frankel, please maintain door-to-inside communication, manage crowd flow, and "
            "support backup AV if needed."
        ),
    ),
    WeddingEvent(
        title="Mee Sua Ceremony",
        start=datetime(2026, 7, 4, 7, 40, tzinfo=SGT),
        message=(
            "Mee Sua Ceremony (面线仪式) is coming up. Ann Qi and Yi Long will eat mee sua together and bow to the deities, "
            "parents, and each other. Bride's parents, please prepare your blessing words — this is short but meaningful. "
            "Items needed: mee sua and bridal veil. Photographer, please capture the bowing, blessings, and family photo moments."
        ),
    ),
    WeddingEvent(
        title="Red Umbrella Send-Off — Leave Bride's Home",
        start=datetime(2026, 7, 4, 8, 10, tzinfo=SGT),
        message=(
            "Red Umbrella Send-Off (红伞送嫁) is about to begin. The bride's father will hold the red umbrella and walk Ann Qi "
            "out, with both parents sending her off at the door. Please prepare the red umbrella, fan, portable fan, and vehicles. "
            "Remember to toss the red umbrella as Ann Qi exits. Hard deadline: leave by 08:15 and reach the groom's home by 09:00. "
            "Frankel, please confirm all items are ready and keep the door area clear."
        ),
    ),
    WeddingEvent(
        title="Groom's Family Tang Yuan & Tea Ceremony",
        start=datetime(2026, 7, 4, 9, 0, tzinfo=SGT),
        message=(
            "Please arrive at the groom's home / Ah Gong's house by 09:00 sharp: 536 Bedok North Street 3, #08-874. "
            "Yi Long opens the door for Ann Qi. Sweet soup — tang yuan, longan, red dates, lotus seeds, and egg — will be served, "
            "symbolising a sweet and fruitful marriage. The tea ceremony with Yi Long's immediate family follows."
        ),
    ),
    WeddingEvent(
        title="Return to Bride's Home",
        start=datetime(2026, 7, 4, 9, 40, tzinfo=SGT),
        message=(
            "It is nearly time to return to the bride's home. Before leaving the groom's home, Ann Qi should change into the Kua (褂). "
            "Please make sure the Kua and hair accessories are already at Yi Long's home. Jin Long and Shi Qi, please coordinate transport."
        ),
    ),
    WeddingEvent(
        title="Bride's Family Tea Ceremony",
        start=datetime(2026, 7, 4, 10, 0, tzinfo=SGT),
        message=(
            "Bride's Family Tea Ceremony (新娘家敬茶) begins soon at 178B Rivervale Crescent, #05-431, S542178. AQ relatives will arrive. "
            "Bridal party, please help parents prepare tea and space, pass teacups, collect red packets, and set up food outside. "
            "Ask a senior family member to stand by and call out names in order. Frankel, please coordinate the buffet vendor, ensure food "
            "arrives on time, and act as house liaison and backup AV."
        ),
    ),
    WeddingEvent(
        title="Wedding Party Photo & Lunch",
        start=datetime(2026, 7, 4, 11, 0, tzinfo=SGT),
        message=(
            "Wedding party photos are coming up downstairs / at the playground. After photos, food arrives at the bride's home around 11:30, "
            "followed by lunch and rest from 12:00. Frankel, please continue supporting guest and logistics coordination."
        ),
    ),
    WeddingEvent(
        title="Check-In at Changi Crowne Plaza",
        start=datetime(2026, 7, 4, 12, 30, tzinfo=SGT),
        message=(
            "Hotel check-in is coming up at Changi Crowne Plaza, 75 Airport Blvd., #01-01, Singapore 819664. Couple, please confirm who is "
            "heading to the hotel after lunch. There are 2 VIP parking spots available. Frankel, please assist with family communication and "
            "item handover during the venue transition if needed."
        ),
    ),
    WeddingEvent(
        title="Second Round of Hair & Makeup",
        start=datetime(2026, 7, 4, 13, 45, tzinfo=SGT),
        message=(
            "Second round of hair and makeup is about to start. Ann Qi begins makeup around 13:45–14:00, Yi Long does a light touch-up, "
            "and both mothers should begin makeup in the bridal suite now. Please keep outfits and accessories ready."
        ),
    ),
    WeddingEvent(
        title="Set Up Reception Table & Solemnisation Area",
        start=datetime(2026, 7, 4, 16, 0, tzinfo=SGT),
        message=(
            "Reception table and solemnisation area setup begins soon. Bridal party, please coordinate with the hotel on the solemnisation, "
            "tea ceremony, and reception areas. Hotel provides the easel stand and 1 fish bowl; video guestbook vendor arrives at 17:30. "
            "Frankel, please help Sue Huei, Bei Bei, Shuang Jie, Joyce, Serene, and Jiong Hao with the welcome area setup."
        ),
    ),
    WeddingEvent(
        title="Pre-Banquet Coordinator Briefing",
        start=datetime(2026, 7, 4, 16, 30, tzinfo=SGT),
        message=(
            "Pre-banquet coordinator briefing is coming up. Please confirm parking vouchers, seating, and table placement with the banquet manager. "
            "Prepare photographer/videographer meals and confirm no beef. Frankel, please sync on AV or guest flow if you are involved."
        ),
    ),
    WeddingEvent(
        title="Couple Photoshoot at Changi Crowne",
        start=datetime(2026, 7, 4, 16, 30, tzinfo=SGT),
        message=(
            "Couple photoshoot at Changi Crowne is starting soon. Photographer arrives at 16:30. Get ready for first-look photos with bridesmaids "
            "and mothers, then photos around Changi Crowne Plaza. Please keep the couple's outfits, bouquet, and touch-up items nearby."
        ),
    ),
    WeddingEvent(
        title="Solemnisation Ceremony",
        start=datetime(2026, 7, 4, 17, 10, tzinfo=SGT),
        message=(
            "Solemnisation Ceremony (证婚仪式) is coming up in Hopea Room. Dr William Chung Tang Fong arrives at 17:10 to verify documents; "
            "ceremony begins around 17:20. Please prepare the ROM marriage certificate and original IC/passport for both the couple and both witness fathers. "
            "Ann Qi will walk in with both parents. If possible, arrange visitor parking for the officiant, car plate SJP 80 R."
        ),
    ),
    WeddingEvent(
        title="Groom's Family Tea Ceremony at Hotel",
        start=datetime(2026, 7, 4, 17, 30, tzinfo=SGT),
        message=(
            "Groom's Family Tea Ceremony at the hotel (男方敬茶) begins soon at Chengal Room / hotel tea area. Bridal party, please set up tea equipment; "
            "Joyce, Shuang Jie, and helpers, please assist. Bring disposable teacups. Follow the prepared family order for Yi Long's dad's and mum's sides."
        ),
    ),
    WeddingEvent(
        title="Banquet Guest Reception",
        start=datetime(2026, 7, 4, 18, 0, tzinfo=SGT),
        message=(
            "Banquet guest reception (晚宴迎宾) begins soon. Guests start arriving at 18:00, banquet hall opens at 18:30, and doors close at 19:00. "
            "At 19:00, food/drinks outside stop, the red packet box should be taken upstairs and locked in the safe, room key passed to Sue Huei and Jiong Hao, "
            "and fish bowl kept by AV and emcee. Frankel, please lead reception with Sue Huei, Bei Bei, and Shuang Jie, and help guests find registration, seats, and key contacts."
        ),
    ),
    WeddingEvent(
        title="First Grand Entrance",
        start=datetime(2026, 7, 4, 19, 15, tzinfo=SGT),
        message=(
            "First Grand Entrance (第一次进场) is coming up. Emcee will cue, AV plays the video montage, and the couple enters to Canon in D. Cake cutting follows. "
            "Frankel, please stand by as backup AV and assist Mason if needed."
        ),
    ),
    WeddingEvent(
        title="SDE Screening",
        start=datetime(2026, 7, 4, 20, 35, tzinfo=SGT),
        message=(
            "SDE (Same-Day Edit) screening is coming up. The SDE is expected to be ready about 30 minutes after the first entrance. Couple, please wait outside. "
            "Bridal party should exit mid-SDE to prepare for the second entrance. Backup plan: if SDE is not ready, screen it after Yam Seng. Frankel, please coordinate with the emcee and videographer."
        ),
    ),
    WeddingEvent(
        title="Second Grand Entrance",
        start=datetime(2026, 7, 4, 20, 40, tzinfo=SGT),
        message=(
            "Second Grand Entrance (第二次进场) is about to happen. Bridal party enters to Fireworks music. Paper planes should be tossed throughout, with the full crowd toss "
            "during the couple's dip kiss. Frankel, please sync with music, reel, and emcee cues as backup AV."
        ),
    ),
    WeddingEvent(
        title="Champagne Tower & Yam Seng",
        start=datetime(2026, 7, 4, 20, 50, tzinfo=SGT),
        message=(
            "Champagne Tower & Yam Seng (香槟塔) is next. Couple, please go straight to the stage, pour champagne, do the lover's toast, then Yam Seng. "
            "AV should return to Spotify/loop music after the couple takes the stage. Frankel, continue backup AV support; if SDE was delayed, help schedule it after Yam Seng."
        ),
    ),
    WeddingEvent(
        title="Thank You Speech",
        start=datetime(2026, 7, 4, 21, 0, tzinfo=SGT),
        message=(
            "Thank You Speech (致谢词) is coming up. Ann Qi and Yi Long, please prepare to deliver your speech. VIP table service resumes after the speech. "
            "If doing a live Telegram call for remote feed, Frankel please stand by for live feed or mic-passing support."
        ),
    ),
    WeddingEvent(
        title="Table-by-Table Photo & Lucky Draw",
        start=datetime(2026, 7, 4, 22, 20, tzinfo=SGT),
        message=(
            "Table-by-table photos and lucky draw are coming up. There are about 24 tables, estimated around 1 hour of photos. Bridal party, please notify each table in advance. "
            "Lucky draw starts around 22:30 with $5 and $10 prize rounds. Frankel, please help coordinate family tables."
        ),
    ),
    WeddingEvent(
        title="End of Banquet & Guest Send-Off",
        start=datetime(2026, 7, 4, 22, 30, tzinfo=SGT),
        message=(
            "End of Banquet & Guest Send-Off (晚宴结束与送客) is coming up. Emcee will announce the end of the banquet. Couple and both sets of parents should send guests off together. "
            "Target: dessert served before 22:00. Yi Long's family takes home the reception photo. Frankel, please assist with wrap-up, item handover, and family coordination."
        ),
    ),
]


def format_reminder(event: WeddingEvent) -> str:
    start_text = event.start.strftime("%d %b %Y, %H:%M")
    return (
        f"💍 <b>Wedding Reminder: {event.title}</b>\n\n"
        f"⏰ <b>Starts in 10 minutes:</b> {start_text} SGT\n\n"
        f"{event.message}\n\n"
        "Wishing everyone a smooth, beautiful, and joyful moment ahead."
    )


async def send_reminder(bot: Bot, event: WeddingEvent) -> None:
    try:
        await bot.send_message(
            chat_id=CHANNEL_ID,
            text=format_reminder(event),
            parse_mode=ParseMode.HTML,
            disable_web_page_preview=True,
        )
        logger.info("Sent reminder for '%s' to channel %s", event.title, CHANNEL_ID)
    except Exception:
        logger.exception("Failed to send reminder for '%s'; continuing to next event", event.title)


async def run_scheduler() -> None:
    bot = Bot(token=BOT_TOKEN)
    events = sorted(EVENTS, key=lambda event: event.reminder_time)

    logger.info("Wedding reminder bot started. Timezone: Asia/Singapore. Channel: %s", CHANNEL_ID)
    logger.info("Loaded %d wedding events", len(events))

    async with bot:
        for event in events:
            now = datetime.now(SGT)
            reminder_time = event.reminder_time

            if reminder_time <= now:
                logger.info(
                    "Skipping '%s' because reminder time already passed: %s SGT",
                    event.title,
                    reminder_time.strftime("%Y-%m-%d %H:%M:%S"),
                )
                continue

            wait_seconds = (reminder_time - now).total_seconds()
            logger.info(
                "Next reminder: '%s' at %s SGT. Sleeping for %.0f seconds.",
                event.title,
                reminder_time.strftime("%Y-%m-%d %H:%M:%S"),
                wait_seconds,
            )

            await asyncio.sleep(wait_seconds)
            await send_reminder(bot, event)

    logger.info("All wedding reminders have been processed. Bot exiting.")


if __name__ == "__main__":
    try:
        asyncio.run(run_scheduler())
    except KeyboardInterrupt:
        logger.info("Wedding reminder bot stopped manually.")
