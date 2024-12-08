const discord = require("discord.js");
const dotenv = require("dotenv");
const { ButtonBuilder } = require("discord.js");
const axios = require("axios");
dotenv.config();
const GatewayIntentBits = discord.GatewayIntentBits;

// const client = new discord.Client({
//   intents: [
//     GatewayIntentBits.MessageContent,
//     GatewayIntentBits.GuildMessages,
//     GatewayIntentBits.GuildMembers,
//     GatewayIntentBits.DirectMessages,
//     GatewayIntentBits.Guilds,
//   ],
// });

async function getLinks(subject) {
  try {
    const url = "https://ktu-notes-bot.onrender.com/api/data";
    const response = await axios.post(url, subject);
    if (response) {
      return response.data;
    }
  } catch (error) {
    console.log(error);
  }
}
const getButtons = async (subject) => {
  const data = await getLinks(subject);
  const row = new discord.ActionRowBuilder();
  if (row) {
    data.array.forEach((item, index) => {
      const button = new ButtonBuilder()
        .setLabel(index)
        .setURL(item)
        .setStyle(discord.ButtonStyle.Link);
      row.addComponents(button);
    });
  }
  return row;
};

subject = {
  code: "cyt100",
  name: "engineering-chemistry",
};
let row = getButtons(subject);
console.log("loading");
console.log(row);
// client.on("ready", () => {
//   console.log(`${client.user.tag} is online!`);
// });

// client.on("messageCreate", async (msg) => {
//   if (!msg?.author.bot) {
//     msg.author.send({
//       content: "Push my button",
//       components: [row],
//     });
//   }
// });

// client.login(process.env.DISCORD_TOKEN);
