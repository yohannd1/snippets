// vim: sw=2

// Another field that could be added here - "wants to work on" for people who want to work on it. IDK i use that for some suggestions i want to implement.
// Also an "associated PR" field thingy. idk. maybe just put that in the description idk
const SUGGESTIONS = [
  {
    name: "sample selection matrix",
    stars: 6,
    url: "https://discord.com/channels/936515318220722197/941448260797747281/1411834801408704662",
    doable: false,
    description: `
      <p>"unfortunately per-sub-song not possible"</p>
    `,
  },

  {
    name: "YM2424 system flac",
    stars: 0,
    url: "https://discord.com/channels/936515318220722197/941448260797747281/1411744219139149834",
    doable: null,
    description: ``,
  },

  {
    name: `"if a channel is muted, gray out the pattern view too?"`,
    stars: 9,
    url: "https://discord.com/channels/936515318220722197/941448260797747281/1411496334447345694",
    doable: null,
    description: ``,
  },

  {
    name: `customisable fading like openmpt`,
    stars: 0,
    url: "https://discord.com/channels/936515318220722197/941448260797747281/1411073411265990858",
    doable: null,
    description: ``,
  },
];

window.addEventListener("load", () => {
  const sg_table = document.querySelector("#suggestion-tables");
  for (const s of SUGGESTIONS) {
    const row = document.createElement("tr");
    row.className = "project-row";

    const td1 = document.createElement("td");
    row.appendChild(td1);

    const a1 = document.createElement("a");
    a1.setAttribute("href", s.url);
    a1.innerText = s.name;
    if (s.stars > 0)
      a1.innerText += ` (${s.stars}×⭐)`;
    td1.appendChild(a1);

    const td2 = document.createElement("td");
    const doablePrefix = (s.doable === false) ? "NOT DOABLE<br>" : "";
    td2.innerHTML = `${doablePrefix}${s.description}`;
    row.appendChild(td2);
    console.log(td2);

    sg_table.appendChild(row);
  }
});
