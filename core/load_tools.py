from core.tool_registry import register_tool
from tools.web_search import web_search
from tools.browser import read_url
from tools.calculator import calculator
from tools.code_runner import run_python
from tools.notes import save_note, read_note
from tools.file_reader import read_file
from services.crypto_price import get_price


def crypto_price_tool(coin):
    result, error = get_price(coin)
    if error:
        return f"Error: {error}"
    change = result["change_24h"]
    sign = "+" if change >= 0 else ""
    arrow = "📈" if change >= 0 else "📉"
    return (
        f"🪙 {coin.upper()}\n"
        f"💵 ${result['price']:,.4f}\n"
        f"{arrow} 24h: {sign}{change}%"
    )


def load_tools():
    register_tool(
        name="web_search",
        func=web_search,
        description="Cari informasi dari internet. Arg: query pencarian.",
    )
    register_tool(
        name="read_url",
        func=read_url,
        description="Baca isi halaman web dari URL. Arg: URL lengkap.",
    )
    register_tool(
        name="calculator",
        func=calculator,
        description="Hitung ekspresi matematika. Arg: ekspresi (contoh: 15 * 200 + 5000).",
    )
    register_tool(
        name="crypto_price",
        func=crypto_price_tool,
        description="Cek harga crypto terkini. Arg: simbol coin (BTC, ETH, SOL, dll).",
    )
    register_tool(
        name="run_python",
        func=run_python,
        description="Jalankan kode Python. Arg: kode Python yang akan dieksekusi.",
    )
    register_tool(
        name="save_note",
        func=save_note,
        description="Simpan catatan pribadi user. Arg: isi catatan.",
    )
    register_tool(
        name="read_note",
        func=read_note,
        description="Baca semua catatan pribadi user. Arg: all.",
    )
    register_tool(
        name="read_file",
        func=read_file,
        description="Baca isi file dari path. Arg: path file.",
    )
