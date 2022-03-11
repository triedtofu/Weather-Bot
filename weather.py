import os
import config
import requests

from discord.ext import commands

bot = commands.Bot(command_prefix="$")

@bot.event
async def on_ready():
    print(f"We have logged in as {bot.user}")

@bot.command()
async def weather(ctx, place, country="AU"):
    base_url = "http://api.openweathermap.org/data/2.5/weather?"
    final_url = base_url + "appid=" + config.WEATHER_TOKEN + "&q=" + place + "," + country + "&units=metric"

    weather_data = requests.get(final_url).json()

    code = weather_data['cod']

    if (code != 200):
        await ctx.send(f"{place} is not found")
        return

    temp = weather_data['main']['temp']
    wind_speed = weather_data['wind']['speed']
    description = weather_data['weather'][0]['description']
    country = weather_data['sys']['country']

    # Printing Data
    await ctx.send(f"""
        Temperature: {temp}
        Wind Speed: {wind_speed}
        Description: {description}
        Country: {country}
    """)


@bot.command()
async def forecast(ctx, place, country="AU"):
    base_url = "http://api.openweathermap.org/data/2.5/forecast?"
    final_url = base_url + "q=" + place + "," + country +"&appid=" + config.WEATHER_TOKEN + "&units=metric"

    forecast_data = requests.get(final_url).json()

    code = int(forecast_data['cod'])

    if (code != 200):
        await ctx.send(f"{place} is not found, {code} {type(code)}")
        return

    temp = forecast_data['list'][0]['main']['temp']

    j = 1
    result_string = ""
    for i in forecast_data['list']:
        substring = "15:00:00"
        if i['dt_txt'].find(substring) != -1:
            result_string += f"Day {j} Temperature: {i['main']['temp']}\n"
            j += 1

    await ctx.send(
        result_string
    )


bot.run(config.DISCORD_TOKEN)