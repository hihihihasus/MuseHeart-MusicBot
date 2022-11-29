import datetime
import itertools
from utils.music.models import LavalinkPlayer
import disnake
from utils.music.converters import time_format, fix_characters


class MiniStaticSkin:

    __slots__ = ("name", "preview")

    def __init__(self):
        self.name = "mini_static"
        self.preview = "https://cdn.discordapp.com/attachments/554468640942981147/1047187413702807552/mini_static_skin.png"

    def load(self, player: LavalinkPlayer) -> dict:

        data = {
            "content": None,
            "embeds": [],
        }

        embed_color = player.bot.get_color(player.guild.me)

        embed = disnake.Embed(
            color=embed_color,
            description=f"[`{player.current.single_title}`]({player.current.uri})"
        )
        embed_queue = None
        queue_size = len(player.queue)

        if not player.paused:
            embed.set_author(
                name="Tocando Agora:",
                icon_url="https://media.discordapp.net/attachments/480195401543188483/987633257178882108/Equalizer.gif",
            )

        else:
            embed.set_author(
                name="Em Pausa:",
                icon_url="https://cdn.discordapp.com/attachments/480195401543188483/896013933197013002/pause.png"
            )

        if player.current.track_loops:
            embed.description += f" `[🔂 {player.current.track_loops}]`"

        elif player.loop:
            if player.loop == 'current':
                embed.description += ' `[🔂 música atual]`'
            else:
                embed.description += ' `[🔁 fila]`'

        embed.description += f" `[`<@{player.current.requester}>`]`"

        duration = "🔴 Livestream" if player.current.is_stream else \
            time_format(player.current.duration)

        embed.add_field(name="⏰ **⠂Duração:**", value=f"```ansi\n[34;1m{duration}[0m\n```")
        embed.add_field(name="💠 **⠂Uploader/Artista:**",
                        value=f"```ansi\n[34;1m{fix_characters(player.current.author, 18)}[0m\n```")

        if player.command_log:
            embed.add_field(name=f"{player.command_log_emoji} **⠂Última Interação:**",
                            value=f"{player.command_log}", inline=False)

        player.mini_queue_feature = False

        embed.set_image(url=player.current.thumb or "https://media.discordapp.net/attachments/480195401543188483/987830071815471114/musicequalizer.gif")

        if queue_size:

            queue_txt = "\n".join(
                f"`{(n + 1):02}) [{time_format(t.duration) if not t.is_stream else '🔴 Livestream'}]` [`{fix_characters(t.title, 28)}`]({t.uri})"
                for n, t in (enumerate(itertools.islice(player.queue, 15)))
            )

            embed_queue = disnake.Embed(title=f"Músicas na fila: {len(player.queue)}",
                                        color=player.bot.get_color(player.guild.me),
                                        description=f"\n{queue_txt}")

            if not player.loop:

                queue_duration = 0

                for t in player.queue:
                    if not t.is_stream:
                        queue_duration += t.duration

                embed_queue.description += f"\n`[⌛ As músicas acabam` <t:{int((disnake.utils.utcnow() + datetime.timedelta(milliseconds=(queue_duration + (player.current.duration if not player.current.is_stream else 0)) - player.position)).timestamp())}:R> `⌛]`"

        if player.current_hint:
            embed.set_footer(text=f"💡 Dica: {player.current_hint}")

        player.auto_update = 0

        data["embeds"] = [embed_queue, embed] if embed_queue else [embed]

        return data

def load():
    return MiniStaticSkin()
