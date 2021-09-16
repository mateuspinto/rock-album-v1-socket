import routes as rt


def router(request, database):
    MW = {
        'login': rt.login,
        'register': rt.register,
        'is_admin': rt.is_admin,
        'op': rt.op,
        'unop': rt.unop,
        'create_giftcard': rt.create_giftcard,
        'retrieve_giftcard': rt.retrieve_giftcard,
        'get_coins': rt.get_coins,
        'create_sticker_model': rt.create_sticker_model,
        'print_stickers': rt.print_stickers,
        'buy_sticker_pack': rt.buy_sticker_pack,
        'paste_sticker': rt.paste_sticker,
        'view_album': rt.view_album,
        'view_free_stickers': rt.view_free_stickers,
        'sell_sticker': rt.sell_sticker,
        'view_stickers_waiting_for_sale': rt.view_stickers_waiting_for_sale,
    }

    return MW[request['method']](request, database)
