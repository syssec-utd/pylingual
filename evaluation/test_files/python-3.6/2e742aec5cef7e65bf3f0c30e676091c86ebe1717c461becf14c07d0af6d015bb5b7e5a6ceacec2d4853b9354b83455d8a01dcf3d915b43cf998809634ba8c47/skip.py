import discord

def init(client: 'Client'):

    @client.command(['skip', 'next'])
    async def skip(message: discord.Message):
        """
        pass the music of your current Guild

        :param client: Client discord
        :param message: discord.Message
        """
        voice_client: discord.VoiceClient = discord.utils.get(client.voice_clients, guild=message.guild)
        if not voice_client:
            return
        if voice_client.is_paused():
            voice_client.resume()
        if voice_client.is_playing():
            voice_client.stop()