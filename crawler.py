from components.downloader import Downloader

class Crawler(object):
  if __name__ == '__main__':
    d = Downloader()
    d.download("https://www.gametrader.sg/profile.php?nick=sirius&platform=PS3")
    d.download("https://carousell.com/p/20557583/")
    d.download("https://carousell.com/")
    d.download("https://www.gametrader.sg/game_pg.php?post_id=140275&title=FIFA+16&platform=PS3&seller=sirius")
    d.download("https://www.gametrader.sg/game_pg.php?post_id=140452&title=Jtag+xbox+360+Slim&platform=Xbox%20360&seller=seechen")
    """
    d.download("www.rakuten.com.sg/shop/shopitree/product/045496741723/?l-id=sg_search_product_2")
    d.download("http://www.rakuten.com.sg/shop/shopitree/category/nintendo3ds/?l-id=sg_product_relatedcategories_1")
    d.download("www.google.com")
    d.download("www.mizukinana.jp")
    d.download("www.facebook.com")
    d.download("www.comp.nus.edu.sg")
    d.download("www.hotmail.com")
    d.download("https://gametrader.sg/index.php")
    """
