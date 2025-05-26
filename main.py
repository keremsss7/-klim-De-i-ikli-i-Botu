import discord
import random
import os
import asyncio

intents = discord.Intents.default()
intents.message_content = True

client = discord.Client(intents=intents)

puanlar = {}

sorular = [
    {"soru": "Sera gazlarının en bilineni hangisidir?", "cevap": "karbondioksit"},
    {"soru": "Küresel ısınmanın başlıca nedeni nedir?", "cevap": "fosil yakıtlar"},
    {"soru": "İklim değişikliği en çok hangi kutupta buzulların erimesine yol açar?", "cevap": "arktik"},
    {"soru": "Yenilenebilir enerjiye örnek ver.", "cevap": "güneş"},
    {"soru": "Ağaçlar neden iklim için önemlidir?", "cevap": "karbondioksit emer"},
]

def resim_gonder(klasor_adi):
    try:
        resimler = os.listdir(klasor_adi)
        resimler = [r for r in resimler if r.lower().endswith(('.jpg', '.jpeg', '.png', '.gif'))]
        if not resimler:
            return None
        secilen = random.choice(resimler)
        return os.path.join(klasor_adi, secilen)
    except FileNotFoundError:
        return None

@client.event
async def on_ready():
    print(f"{client.user} olarak giriş yapıldı!")

@client.event
async def on_message(message):
    if message.author == client.user:
        return

    msg = message.content.lower()

    if msg == "hello":
        await message.channel.send(f"Merhaba {message.author.mention}! Ben bir botum!")

    elif msg == "selam":
        await message.channel.send("Merhaba!")

    elif msg == "komutlar":
        await message.channel.send(
            "Komutlar:\n"
            "1- iklim değişikliği nedir\n"
            "2- iklim değişikliği nasıl önlenir\n"
            "3- iklim değişikliği nelere yol açabilir\n"
            "4- konuyla ilgili bir video atar mısın\n"
            "5- motor resmi at\n"
            "6- konuyla ilgili resim at\n"
            "7- soru\n"
            "8- puanım\n"
        )

    elif msg == "iklim değişikliği nedir":
        await message.channel.send(
            "İklim değişikliği, küresel ısınmayı (küresel ortalama sıcaklıkta süregelen artış) "
            "ve bunun Dünya'nın iklim sistemi üzerindeki etkilerini ifade eder."
        )

    elif msg == "iklim değişikliği nasıl önlenir":
        await message.channel.send(
            "– Kullanmadığımız elektrikli aletleri fişten çekelim. Televizyon, bilgisayar veya "
            "telefon şarj aleti gibi elektrikli cihazlar beklemede olsalar bile elektrik kullanırlar. "
            "Bu sebeple fişlerini çekmeyi unutmayalım."
        )

    elif msg == "iklim değişikliği nelere yol açabilir":
        await message.channel.send(
            "İklim değişikliği insanları gıda ve su kıtlığı, artan seller, aşırı sıcaklar, "
            "daha fazla hastalık ve ekonomik kayıplarla tehdit etmektedir. İnsan göçü ve çatışmalar "
            "da bunun bir sonucu olabilir."
        )

    elif msg == "konuyla ilgili bir video atar mısın":
        await message.channel.send("https://www.youtube.com/watch?v=aGYjEyHBUTA&ab_channel=TEMAVakf%C4%B1")

    elif msg == "motor resmi at":
        dosya_yolu = resim_gonder("resimler")
        if dosya_yolu:
            await message.channel.send(file=discord.File(dosya_yolu))
        else:
            await message.channel.send("Resim klasörü bulunamadı veya içinde resim yok!")

    elif msg == "konuyla ilgili resim at":
        dosya_yolu = resim_gonder("iklim değişikliği")
        if dosya_yolu:
            await message.channel.send(file=discord.File(dosya_yolu))
        else:
            await message.channel.send("Resim klasörü bulunamadı veya içinde resim yok!")

    elif msg == "soru":
        soru = random.choice(sorular)
        await message.channel.send(f"Soru: {soru['soru']}")

        def check(m):
            return m.author == message.author and m.channel == message.channel

        try:
            cevap = await client.wait_for("message", timeout=20.0, check=check)
            if soru['cevap'] in cevap.content.lower():
                puanlar[message.author.id] = puanlar.get(message.author.id, 0) + 1
                await message.channel.send(f"✅ Doğru cevap! Puanınız: {puanlar[message.author.id]}")
            else:
                await message.channel.send(f"❌ Yanlış cevap. Doğru cevap: **{soru['cevap']}**")
        except asyncio.TimeoutError:
            await message.channel.send("⏰ Süre doldu! Daha hızlı cevap verin.")

    elif msg == "puanım":
        puan = puanlar.get(message.author.id, 0)
        await message.channel.send(f"{message.author.mention}, puanınız: {puan}")

client.run("MTM2ODk5NjI2NzU4OTM3MDA0Ng.GZgBo8.NeJ1b27Pa-6EJenwTDSOiZZ4yp6r2Xii6Cs-KY")
