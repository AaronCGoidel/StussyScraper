import scrapy


class ProductSpider(scrapy.Spider):
    name = "products"

    product_base_url = (
        "https://www.stussy.com/collections/mens-new-arrivals?page={0}"
    )

    page_num = 1

    start_urls = [product_base_url.format(page_num)]

    def parse(self, res):
        products = res.css(".collection__product")

        if products:
            for item in products:
                # yield object containing title, price, and img source of current item
                yield {
                    "title": item.css(".product-card__title::text").get(),
                    "price": item.css(".product-card__price::text").get(),
                    "image": item.css("img::attr(src)").get().strip("/"),
                }
            # make request to get next page of products (handle infinite scroll)
            self.page_num += 1
            yield scrapy.Request(self.product_base_url.format(self.page_num))
