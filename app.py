import streamlit as st

from database import Database
from steam_api import SteamAPI


st.set_page_config(page_title="Steam Wishlist Tracker", page_icon="🎮", layout="wide")

st.title("🎮 Steam Wishlist Tracker (MVP)")
st.caption("Monitore manualmente jogos da sua wishlist e veja quais estão em promoção.")


def parse_appids(raw_text: str):
    appids = []
    for item in raw_text.replace("\n", ",").split(","):
        value = item.strip()
        if not value:
            continue
        if value.isdigit():
            appids.append(int(value))
    return sorted(set(appids))


db = Database()
api = SteamAPI()

saved_appids = db.get_tracked_appids()
default_text = ", ".join(str(appid) for appid in saved_appids)

st.subheader("1) Sua lista manual de AppIDs")
appids_input = st.text_area(
    "Informe os AppIDs separados por vírgula ou quebra de linha",
    value=default_text,
    height=120,
    placeholder="Ex.: 730, 570, 440",
)

col1, col2 = st.columns(2)

with col1:
    if st.button("Salvar lista"):
        appids = parse_appids(appids_input)
        db.save_tracked_appids(appids)
        st.success(f"Lista salva com {len(appids)} AppID(s).")

with col2:
    if st.button("Atualizar agora"):
        appids = parse_appids(appids_input)
        if not appids:
            st.warning("Informe ao menos um AppID válido antes de atualizar.")
        else:
            db.save_tracked_appids(appids)
            with st.spinner("Consultando Steam..."):
                games = api.update_wishlist_games(appids)
            db.upsert_games(games)
            st.success(f"Atualização concluída. {len(games)} jogo(s) consultado(s).")

st.subheader("2) Jogos em promoção")
games = db.get_discounted_games()

if not games:
    st.info("Nenhum jogo em promoção encontrado no banco até agora.")
else:
    rows = [
        {
            "Nome": game.name,
            "Preço atual": f"R$ {game.price_current:,.2f}".replace(",", "X").replace(".", ",").replace("X", "."),
            "Preço original": f"R$ {game.price_original:,.2f}".replace(",", "X").replace(".", ",").replace("X", "."),
            "Desconto": f"{game.discount_percent}%",
            "Última atualização": game.last_updated.strftime("%Y-%m-%d %H:%M:%S"),
        }
        for game in games
    ]
    st.dataframe(rows, use_container_width=True)
